# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: frameUnitMsg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='frameUnitMsg.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x12\x66rameUnitMsg.proto\"\x95\x03\n\tframeUnit\x12\x12\n\ntime_stamp\x18\x01 \x01(\x02\x12\x12\n\nacc_x_6050\x18\x02 \x01(\x02\x12\x12\n\nacc_y_6050\x18\x03 \x01(\x02\x12\x12\n\nacc_z_6050\x18\x04 \x01(\x02\x12\x16\n\x0e\x61ngular_x_6050\x18\x05 \x01(\x02\x12\x16\n\x0e\x61ngular_y_6050\x18\x06 \x01(\x02\x12\x16\n\x0e\x61ngular_z_6050\x18\x07 \x01(\x02\x12\x12\n\nacc_x_9250\x18\x08 \x01(\x02\x12\x12\n\nacc_y_9250\x18\t \x01(\x02\x12\x12\n\nacc_z_9250\x18\n \x01(\x02\x12\x16\n\x0e\x61ngular_x_9250\x18\x0b \x01(\x02\x12\x16\n\x0e\x61ngular_y_9250\x18\x0c \x01(\x02\x12\x16\n\x0e\x61ngular_z_9250\x18\r \x01(\x02\x12\x16\n\x0eUSensorForward\x18\x0e \x01(\x02\x12\x17\n\x0fUSensorDownward\x18\x0f \x01(\x02\x12\x12\n\npiCamImage\x18\x10 \x01(\x0c\x12\x13\n\x0bimageHeight\x18\x11 \x01(\x05\x12\x12\n\nimageWidth\x18\x12 \x01(\x05')
)




_FRAMEUNIT = _descriptor.Descriptor(
  name='frameUnit',
  full_name='frameUnit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time_stamp', full_name='frameUnit.time_stamp', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acc_x_6050', full_name='frameUnit.acc_x_6050', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acc_y_6050', full_name='frameUnit.acc_y_6050', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acc_z_6050', full_name='frameUnit.acc_z_6050', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angular_x_6050', full_name='frameUnit.angular_x_6050', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angular_y_6050', full_name='frameUnit.angular_y_6050', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angular_z_6050', full_name='frameUnit.angular_z_6050', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acc_x_9250', full_name='frameUnit.acc_x_9250', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acc_y_9250', full_name='frameUnit.acc_y_9250', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acc_z_9250', full_name='frameUnit.acc_z_9250', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angular_x_9250', full_name='frameUnit.angular_x_9250', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angular_y_9250', full_name='frameUnit.angular_y_9250', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='angular_z_9250', full_name='frameUnit.angular_z_9250', index=12,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='USensorForward', full_name='frameUnit.USensorForward', index=13,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='USensorDownward', full_name='frameUnit.USensorDownward', index=14,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='piCamImage', full_name='frameUnit.piCamImage', index=15,
      number=16, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='imageHeight', full_name='frameUnit.imageHeight', index=16,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='imageWidth', full_name='frameUnit.imageWidth', index=17,
      number=18, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=428,
)

DESCRIPTOR.message_types_by_name['frameUnit'] = _FRAMEUNIT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

frameUnit = _reflection.GeneratedProtocolMessageType('frameUnit', (_message.Message,), dict(
  DESCRIPTOR = _FRAMEUNIT,
  __module__ = 'frameUnitMsg_pb2'
  # @@protoc_insertion_point(class_scope:frameUnit)
  ))
_sym_db.RegisterMessage(frameUnit)


# @@protoc_insertion_point(module_scope)
