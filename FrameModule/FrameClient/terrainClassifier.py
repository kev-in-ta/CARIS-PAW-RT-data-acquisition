
"""
Author:         Kevin Ta
Date:           2019 August 8th
Purpose:        This Python script should autostart when the Raspberry Pi is first powered.
                This script will run the real-time terrain classification algorithms
                on the IMU data.
"""

# IMPORTED LIBRARIES

import smbus
import math
import time
import datetime
import os
import sys
import socket

import pickle as pkl
import numpy as np
from scipy import signal, stats
import pandas as pd
import sklearn
from sklearn.preprocessing import scale
import pickle as pkl
from joblib import load, dump

from cobs import cobs
from multiprocessing import Process, Queue
from threading import Thread

# LOCALLY IMPORTED LIBRARIES
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(dir_path, 'libraries'))

from mpu6050 import mpu6050
from mpu9250 import mpu9250
from fusion import Fusion

from WheelModuleLib import *
from featuresLib import *
from IMUSensorLib import *
from USSSensorLib import *
from PiCamSensorLib import *

# DEFINITIONS

#~ HOST = '206.12.32.200' # Variable for UBCVisitor
HOST = '192.168.0.100' # Set for portable router
#~ HOST = '192.168.0.102' # Set for portable router
PORT = 65432

# Sensor list to activate
SENSOR_LIST = ['IMU_9', 'IMU_6', 'USS_DOWN', 'USS_FORW', 'PI_CAM', 'LEFT', 'RIGHT']

#Active sensors
ACTIVE_SENSORS = [1]

# Direction Vectors
STD_COLUMNS = ['X Accel', 'Y Accel', 'Z Accel', 'X Gyro', 'Y Gyro', 'Z Gyro', 'Run Time', 'Epoch Time']
DATA_COLUMNS =  ['X Accel', 'Y Accel', 'Z Accel', 'X Gyro', 'Y Gyro', 'Z Gyro']

EPSILON = 0.00001 # For small float values

FRAME_MODULE = {'wLength': 300, 'fSamp': 300, 'fLow': 55, 'fHigh': 1}
WHEEL_MODULE = {'wLength': 333, 'fSamp': 333.3, 'fLow': 60, 'fHigh': 1}

PAD_LENGTH = 15 # pad length to let filtering be better
N_BINS_OVER_CUTOFF = 5 # Collect some information from attenuated frequencies bins

# DICTIONARIES

# Time domain feature functions and names
TIME_FEATURES = {'Mean': np.mean, 'Std': np.std,  'Norm': l2norm, 'AC': autocorr, 
                 'Max': np.amax, 'Min' : np.amin, 'RMS': rms, 'ZCR': zcr, 
                 'Skew': stats.skew, 'EK': stats.kurtosis}

TIME_FEATURES_NAMES = ['Mean', 'Std', 'Norm', 'AC', 'Max', 'Min', 'RMS', 'ZCR', 'Skew', 'EK']

# Time domain feature functions and names           
FREQ_FEATURES = freq_features = {'MSF': msf, 'RMSF': rmsf, 'FC': fc, 'VF': vf, 'RVF': rvf}

FREQ_FEATURES_NAMES = ['MSF', 'RMSF', 'FC', 'VF', 'RVF']

TERRAINS = ['Concrete', 'Carpet', 'Linoleum', 'Asphalt', 'Sidewalk', 'Grass', 'Gravel']

# CLASSES

class ClTerrainClassifier:
	"""
	Class for establishing wireless communications.
	"""
	
	def __init__(self, protocol = 'TCP'):
		"""
		Purpose:	Initialize various sensors and class variables
		Passed: 	Nothing
		"""
		
		# Middle
		self.placement = 'Middle'
		self.sensorParam = FRAME_MODULE

		# Left
		#~ self.placement = 'Left'
		#~ self.sensorParam = WHEEL_MODULE
		
		#~ # Right
		#~ self.placement = 'Right'
		#~ self.sensorParam = WHEEL_MODULE
		
		# Calculates the number of bins available
		nbins = int(self.sensorParam['wLength'] / self.sensorParam['fSamp'] *self.sensorParam['fLow'] + N_BINS_OVER_CUTOFF)
			
		print('unpickling')
		
		#~ randomForestTime = pkl.load(open(os.path.join(dir_path, 'models', 'RandomForest_Middle_TimeFeats.pkl'), 'rb'))
		#~ self.SVMTime = load('models/SupportVectorMachine_Middle_TimeFeats.joblib')
		#~ self.SVMFreq = load('models/SupportVectorMachine_Middle_FreqFeats.joblib')
		#~ self.SVMPSD = load('models/SupportVectorMachine_Middle_PSDLogs.joblib')

		self.RFTime = load('models/RandomForest_Middle_TimeFeats.joblib')
		self.RFFreq = load('models/RandomForest_Middle_FreqFeats.joblib')
		self.RFPSD = load('models/RandomForest_Middle_PSDLogs.joblib')

		self.timeScaler = load('scalers/Middle_TimeFeats_Scaler.joblib')
		self.freqScaler = load('scalers/Middle_FreqFeats_Scaler.joblib')
		self.psdlScaler = load('scalers/Middle_PSDLogs_Scaler.joblib')

		# Prepopulate pandas dataframe
		EFTimeColumnNames = ['{} {} {}'.format(featName, direction, self.placement) for direction in DATA_COLUMNS for featName in TIME_FEATURES_NAMES]
		self.EFTimeColumnedFeatures = pd.DataFrame(data = np.zeros((1,len(EFTimeColumnNames))), columns = EFTimeColumnNames)
		EFFreqColumnNames = ['{} {} {}'.format(featName, direction, self.placement) for direction in DATA_COLUMNS for featName in FREQ_FEATURES_NAMES]
		self.EFFreqColumnedFeatures = pd.DataFrame(data = np.zeros((1,len(EFFreqColumnNames))), columns = EFFreqColumnNames)
		self.protocol = protocol
		
		
		if self.protocol == 'TCP':
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.settimeout(10)
			self.socket.connect((HOST, PORT))
			print('Connected.')
		
		# Initialize data queue and marker to pass for separate prcoesses
		self.dataQueue = Queue()
		self.runMarker= Queue()
		
		# Create class variables
		self.windowIMUraw = np.zeros((self.sensorParam['wLength'] + 2 * PAD_LENGTH, 6))
		self.windowIMUfiltered = np.zeros((self.sensorParam['wLength'], 6))
		self.windowIMUPSD = np.zeros([])
		self.windowIMULogPSD = np.zeros([])
		self.windowIMULogPSDFeatures = np.zeros([])
				
		# Create dictionary to house various active sensors and acivate specified sensors
		self.instDAQLoop = {} 
		
		for sensor in ACTIVE_SENSORS:
			if sensor == 0:
				self.instDAQLoop[SENSOR_LIST[sensor]] = ClMpu9250DAQ(self.dataQueue, self.runMarker)
			elif sensor == 1:
				self.instDAQLoop[SENSOR_LIST[sensor]] = ClMpu6050DAQ(self.dataQueue, self.runMarker)
			elif sensor == 2:
				self.instDAQLoop[SENSOR_LIST[sensor]] = ClProximitySensorDAQ(self.dataQueue, self.runMarker)
			elif sensor == 4:
				self.instDAQLoop[SENSOR_LIST[sensor]] = ClPiCameraDAQ(self.dataQueue, self.runMarker)
			elif sensor == 5:
				self.instDAQLoop[SENSOR_LIST[sensor]] = ClWheelDataParsing(Left, self.dataQueue, self.runMarker)
			elif sensor == 6:
				self.instDAQLoop[SENSOR_LIST[sensor]] = ClWheelDataParsing(Right, self.dataQueue, self.runMarker)
				

	def fnStart(self, frequency):
		"""
		Purpose:	Intialize all active sensors in separate processed and collects data from the Queue
		Passed:		Frequency for 6-axis IMU to operate at
		"""

		print('Start Process.')
		
		# Start terrain classification in separate thread
		terrain = Thread(target=self.fnTerrainClassification, args = (0.5, ))
		terrain.start()
		
		timeStart = time.time()
		
		# Create dictionary to store processes
		processes = {}

		# Start various data collection sensors
		for sensor in ACTIVE_SENSORS:
			processes[SENSOR_LIST[sensor]] = Process(target=self.instDAQLoop[SENSOR_LIST[sensor]].fnRun, args = (frequency, ))
			processes[SENSOR_LIST[sensor]].start()

		#Keep collecting data and updating rolling window
		while True:

			transmissionData = self.dataQueue.get()

			if transmissionData[0] in ['IMU_6', 'WHEEL']:
				self.windowIMUraw = np.roll(self.windowIMUraw, -1, axis=0)
				self.windowIMUraw[-1, :] = np.multiply(np.subtract(transmissionData[2:8], [0, 0, 9.8, 0, 0, 0]), [1, 1, 1, math.pi/180, math.pi/180, math.pi/180]) 
			elif transmissionData[0] in ['USS_DOWN', 'USS_FORW']:
				pass
			elif transmissionData[0] in ['PI_CAM']:
				pass

	def fnTerrainClassification(self, waitTime):
		"""
		Purpose:	Class method for running terrain classification
		Passed:		Time in between runs
		"""
		
		index = 0
		
		# Keep running until run marker tells to terminate
		while self.runMarker:
			
			print(time.perf_counter())
			
			# Filter window
			self.fnFilterButter(self.windowIMUraw)
			
			# Build extracted feature vector
			self.fnBuildTimeFeatures(TIME_FEATURES_NAMES)
			
			# Build PSD and PSD features
			self.fnBuildPSD(self.windowIMUfiltered)
			self.fnBuildFreqFeatures(FREQ_FEATURES_NAMES)
			
			#~ terrainTypeSVMTime = self.SVMTime.predict(self.EFTimeColumnedFeatures)
			#~ terrainTypeSVMFreq = self.SVMFreq.predict(self.EFFreqColumnedFeatures)
			#~ terrainTypeSVMPSD = self.SVMPSD.predict(self.windowIMULogPSDFeatures)
			
			#~ self.socket.sendall('Time: {0:>8s} \nFreq: {1:>8s} \nPSD:  {2:>8s}'.format(TERRAINS[terrainTypeSVMTime[0]], TERRAINS[terrainTypeSVMFreq[0]], TERRAINS[terrainTypeSVMPSD[0]]).encode())
			
			terrainTypeRFTime = self.RFTime.predict(self.EFTimeColumnedFeatures)
			terrainTypeRFFreq = self.RFFreq.predict(self.EFFreqColumnedFeatures)
			terrainTypeRFPSD = self.RFPSD.predict(self.windowIMULogPSDFeatures)
			try:
				self.socket.sendall('Time: {0:>8s}     Freq: {1:>8s}     PSD:  {2:>8s}'.format(TERRAINS[terrainTypeRFTime[0]], TERRAINS[terrainTypeRFFreq[0]], TERRAINS[terrainTypeRFPSD[0]]).encode())
			except Exception as e:
				print(e)
				break
			
			#~ self.socket.sendall('Time (RF):  {0:>8s} \nTime (SVM): {1:>8s}'.format(TERRAINS[terrainTypeRFTime[0]], TERRAINS[terrainTypeSVMTime[0]]).encode())
			
			#~ print('Time: {0:>8s} \nFreq: {1:>8s} \nPSD:  {2:>8s} \n'.format(TERRAINS[terrainTypeSVMTime[0]], TERRAINS[terrainTypeSVMFreq[0]], TERRAINS[terrainTypeSVMPSD[0]]))
			#~ print('Time: {0:>8s} \nFreq: {1:>8s} \nPSD:  {2:>8s} \n'.format(TERRAINS[terrainTypeRFTime[0]], TERRAINS[terrainTypeRFFreq[0]], TERRAINS[terrainTypeRFPSD[0]]))
			
			#~ print('Time: {}'.format(TERRAINS[terrainTypeSVMTime[0]]))
			#~ print('Freq: {}'.format(TERRAINS[terrainTypeSVMFreq[0]]))
			#~ print('PSD:  {}'.format(TERRAINS[terrainTypeSVMPSD[0]]))
			
			time.sleep(waitTime - (time.perf_counter() % waitTime))
		
	def fnShutDown(self):
		
		print('Closing Socket')
		self.socket.close()
		try:
			self.sock.close()
		except Exception as e:
			print(e)

	def fnFilterButter(self, dataWindow):
		"""
		Purpose:	Low pass butterworth filter onto rolling window and 
					stores in filtered class variable
		Passed:		Rolling raw IMU data
		"""
		
		# Get normalized frequencies
		w_low = self.sensorParam['fLow'] / (self.sensorParam['fSamp'] / 2) 
		w_high = self.sensorParam['fHigh'] / (self.sensorParam['fSamp'] / 2)

		# Get Butterworth filter parameters
		b_butter, a_butter = signal.butter(N=4, Wn=w_low, btype='low')
		
		dataSet = np.copy(dataWindow)
		
		# Filter all the data columns
		for i in range(6):
			self.windowIMUfiltered[:, i] = signal.filtfilt(b_butter, a_butter, dataSet[:, i])[PAD_LENGTH:self.sensorParam['wLength']+PAD_LENGTH]
		
		print('filtered!')
			
	def fnBuildPSD(self, dataWindow):
		"""
		Purpose:	Builds power spectrum densities for each direction
		Passed:		Filtered IMU data
		"""
		
		# Only include frequency bins up to and a little bit past the cutoff frequency
		# Everything past that is useless because its the same on all terrains
		n_bins = int(self.sensorParam['wLength'] / self.sensorParam['fSamp'] * self.sensorParam['fLow']) + N_BINS_OVER_CUTOFF
		windowIMUPSD = np.zeros((n_bins, 6))
		windowIMULogPSD = np.zeros((n_bins, 6))

		# Calculate PSD for each axes
		for i in range(6):
			# Normalized PSD - Returns frequencies and power density
			freq, Pxx = signal.periodogram(dataWindow[:, i], self.sensorParam['fSamp'])
			windowIMUPSD[:, i] = np.resize(Pxx[1:], n_bins)
			
			# Calculate log10 of PSD, replacing points where PSD = 0 with 0 to avoid division by 0
			for j in range(len(windowIMUPSD[:, i])):
				if (windowIMUPSD[j, i] == 0):
					windowIMULogPSD[j, i] = 0
				else:
					windowIMULogPSD[j, i] = np.log10(windowIMUPSD[j, i])
			
		# Append freq column
		freq_col = np.transpose([np.resize(freq[:-1], n_bins)])
		self.windowIMUPSD = np.append(windowIMUPSD, freq_col, axis=1)
		self.windowIMULogPSD = np.append(windowIMULogPSD, freq_col, axis=1)
		
		colNames = ['{} {} Hz {} {}'.format('PSDLog', round(freq[0]), direction, self.placement) for direction in DATA_COLUMNS for freq in freq_col]	
		psdLogData = [self.windowIMULogPSD[i, j] for j in range(len(self.windowIMULogPSD[0, :])-1) for i in range(len(self.windowIMULogPSD[:, 0]))]
		#~ psdLogData = np.divide(np.subtract(psdLogData, self.PSDMean), self.PSDScale)
		psdLogData = self.psdlScaler.transform(np.array(psdLogData).reshape(1,-1))[0]
		self.windowIMULogPSDFeatures = pd.DataFrame(data=[psdLogData], columns=colNames)
		
		print('PSD!')
   	
	def fnBuildTimeFeatures(self, features):
		"""
		Purpose:	Perform all time domain feature extraction on filtered data, 
					then columns the data and standardized based on mean and std
		Passed:		Feature dictionary to perform
		"""
		dataList = [TIME_FEATURES[featName](self.windowIMUfiltered[:, i]) for i, direction in enumerate(DATA_COLUMNS) for featName in features]
		#~ dataList = np.divide(np.subtract(dataList, self.TimeMean), self.TimeScale)
		dataList = self.timeScaler.transform(np.array(dataList).reshape(1,-1))[0]
		dataNames = ['{} {} {}'.format(featName, direction, self.placement) for direction in DATA_COLUMNS for featName in features]
		self.EFTimeColumnedFeatures = pd.DataFrame(data=[dataList], columns=dataNames)

	def fnBuildFreqFeatures(self, features):
		"""
		Purpose:	Perform all frequency domain feature extraction on filtered data, 
					then columns the data and standardized based on mean and std
		Passed:		Feature dictionary to perform
		"""
		dataList = [FREQ_FEATURES[featName](self.windowIMUPSD[:, -1], self.windowIMUPSD[:, i]) for i, direction in enumerate(DATA_COLUMNS) for featName in features]
		#~ dataList = np.divide(np.subtract(dataList, self.FreqMean), self.FreqScale)
		dataList = self.freqScaler.transform(np.array(dataList).reshape(1, -1))[0]
		dataNames = ['{} {} {}'.format(featName, direction, self.placement) for direction in DATA_COLUMNS for featName in features]
		self.EFFreqColumnedFeatures = pd.DataFrame(data=[dataList], columns=dataNames)



# MAIN PROGRAM

if __name__=="__main__":
	
	connectedStatus = False

	dummyQueue = Queue
	dummyMarker = Queue

	#~ instMpu9250DAQ = ClMpu9250DAQ(dummyQueue, dummyMarker)
	#~ instMpu9250DAQ.fnCalibrate()
	instMpu6050DAQ = ClMpu6050DAQ(dummyQueue, dummyMarker)
	instMpu6050DAQ.fnCalibrate()

	processStatus = False

	while True:
		try:
			instTerrainClassifier = ClTerrainClassifier(protocol = 'TCP')
			processStatus = True
			instTerrainClassifier.fnStart(300)
		except Exception as e:
			time.sleep(1)
			if processStatus:
				instTerrainClassifier.runMarker.put(False)
				instTransferClient.fnShutDown()
				instTerrainClassifier.runMarker.close()
				instTerrainClassifier.dataQueue.close()
				connectedStatus = False
			print(e)
