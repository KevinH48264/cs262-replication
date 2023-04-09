# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\"\x1a\n\x07Request\x12\x0f\n\x07request\x18\x01 \x01(\t\"\x1c\n\x08Response\x12\x10\n\x08response\x18\x01 \x01(\t\"5\n\rAccountUpdate\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x12\n\nconnection\x18\x02 \x01(\t\"1\n\x0bQueueUpdate\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08messages\x18\x02 \x03(\t2\xbc\x02\n\x0b\x43hatService\x12&\n\rCreateAccount\x12\x08.Request\x1a\t.Response\"\x00\x12\x1e\n\x05LogIn\x12\x08.Request\x1a\t.Response\"\x00\x12$\n\x0bSendMessage\x12\x08.Request\x1a\t.Response\"\x00\x12%\n\x0cShowAccounts\x12\x08.Request\x1a\t.Response\"\x00\x12&\n\rDeleteAccount\x12\x08.Request\x1a\t.Response\"\x00\x12\'\n\x0eReceiveMessage\x12\x08.Request\x1a\t.Response\"\x00\x12\x1f\n\x06LogOut\x12\x08.Request\x1a\t.Response\"\x00\x12&\n\rSendHeartbeat\x12\x08.Request\x1a\t.Response\"\x00\x32l\n\x12ReplicationService\x12,\n\rUpdateAccount\x12\x0e.AccountUpdate\x1a\t.Response\"\x00\x12(\n\x0bUpdateQueue\x12\x0c.QueueUpdate\x1a\t.Response\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=14
  _REQUEST._serialized_end=40
  _RESPONSE._serialized_start=42
  _RESPONSE._serialized_end=70
  _ACCOUNTUPDATE._serialized_start=72
  _ACCOUNTUPDATE._serialized_end=125
  _QUEUEUPDATE._serialized_start=127
  _QUEUEUPDATE._serialized_end=176
  _CHATSERVICE._serialized_start=179
  _CHATSERVICE._serialized_end=495
  _REPLICATIONSERVICE._serialized_start=497
  _REPLICATIONSERVICE._serialized_end=605
# @@protoc_insertion_point(module_scope)
