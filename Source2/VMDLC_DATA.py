# from typing import List
#
# from ByteIO import ByteIO
# from GLOBALS import SourceVector
# from Source2.Blocks.Dummy import Dummy
#
#
# class VmdlcDATABlock(Dummy):
#
#     def __init__(self):
#         self.model_name_offset = 0
#         self.model_info = ModelInfo()
#
#     def read(self, reader: ByteIO):
#         entry = reader.tell()
#         self.model_name_offset = reader.read_int32()
#         self.model_name = ''
#         if self.model_name_offset:
#             self.model_name = reader.read_from_offset(entry+self.model_name_offset, reader.read_ascii_string)
#         self.model_info.read(reader)
#
#     def __repr__(self):
#         return '<DataBlock model_path name:"{}">'.format(self.model_name)
#
#
# class ModelInfo(Dummy):
#
#     def __init__(self):
#         self.flags = 0
#         self.h_min = SourceVector()
#         self.h_max = SourceVector()
#         self.v_min = SourceVector()
#         self.v_max = SourceVector()
#         self.mass = 0.0
#         self.eye_pos = SourceVector()
#         self.max_eye_deflection = 0
#         self.surface_prop_offset = 0
#         self.surface_prop = ''
#         self.key_value_offset = 0
#         self.key_value = ''
#     def __repr__(self):
#         return '<ModelInfo>'
#
#     def read(self, reader: ByteIO):
#         self.flags = reader.read_int32()
#         self.h_min.read(reader)
#         self.h_max.read(reader)
#         self.v_min.read(reader)
#         self.v_max.read(reader)
#         self.mass = reader.read_float()
#         self.eye_pos.read(reader)
#         self.max_eye_deflection = reader.read_float()
#         entry = reader.tell()
#         if self.surface_prop_offset:
#             self.surface_prop = reader.read_from_offset(entry+self.surface_prop_offset, reader.read_ascii_string)
#         self.surface_prop_offset = reader.read_int32()
#         entry = reader.tell()
#         self.key_value_offset = reader.read_int32()
#         if self.key_value_offset:
#             self.key_value = reader.read_from_offset(entry+self.key_value_offset, reader.read_ascii_string)
#
#
