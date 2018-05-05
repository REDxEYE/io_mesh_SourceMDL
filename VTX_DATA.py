from pprint import pformat
from typing import List

try:
    from .ByteIO import ByteIO
except ImportError:
    from ByteIO import ByteIO

max_bones_per_vertex = 3


class SourceVtxFileData:
    def __init__(self):
        self.version = 0
        self.vertex_cache_size = 0
        self.max_bones_per_strip = 3
        self.max_bones_per_tri = 3
        self.max_bones_per_vertex = 3
        self.checksum = 0
        self.lodCount = 0
        self.material_replacement_list_offset = 0
        self.bodyPartCount = 0
        self.bodyPartOffset = 0
        self.vtx_body_parts = []  # type: List[SourceVtxBodyPart]

    def read(self, reader: ByteIO):
        self.version = reader.read_uint32()
        self.vertex_cache_size = reader.read_uint32()
        self.max_bones_per_strip = reader.read_uint16()
        self.max_bones_per_tri = reader.read_uint16()
        self.max_bones_per_vertex = reader.read_uint32()
        self.checksum = reader.read_uint32()
        self.lodCount = reader.read_uint32()
        self.material_replacement_list_offset = reader.read_uint32()
        self.bodyPartCount = reader.read_uint32()
        self.bodyPartOffset = reader.read_uint32()
        global max_bones_per_vertex
        max_bones_per_vertex = self.max_bones_per_vertex
        if self.bodyPartOffset > 0:
            for _ in range(self.bodyPartCount):
                self.vtx_body_parts.append(SourceVtxBodyPart().read(reader))
        # print(self.max_bones_per_vertex)

    def __repr__(self):
        return "<FileData version:{} lod count:{} body part count:{} \nbodyparts:{}>\n".format(self.version,
                                                                                               self.lodCount,
                                                                                               self.bodyPartCount,
                                                                                               self.vtx_body_parts)


class SourceVtxBodyPart:
    def __init__(self):
        self.model_count = 0
        self.model_offset = 0
        self.vtx_models = []

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.model_count = reader.read_uint32()
        self.model_offset = reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(entry + self.model_offset)
            for _ in range(self.model_count):
                self.vtx_models.append(SourceVtxModel().read(reader))
        return self

    def __repr__(self):
        return "<BodyPart model_path count:{} models:{}>".format(self.model_count, self.vtx_models)


class SourceVtxModel:
    def __init__(self):
        self.lodCount = 0
        self.lodOffset = 0
        self.vtx_model_lods = []  # type: List[SourceVtxModelLod]

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.lodCount = reader.read_uint32()
        self.lodOffset = reader.read_uint32()
        with reader.save_current_pos():
            if self.lodCount > 0 and self.lodOffset != 0:
                reader.seek(entry + self.lodOffset)
                for _ in range(self.lodCount):
                    self.vtx_model_lods.append(SourceVtxModelLod().read(reader, self))
        return self

    def __repr__(self):
        return "<Model  lod count:{} lods:{}>".format(self.lodCount, self.vtx_model_lods)


class SourceVtxModelLod:
    def __init__(self):
        self.lod = 0
        self.meshCount = 0
        self.meshOffset = 0
        self.switchPoint = 0
        self.vtx_meshes = []
        self.first_strip_end = 0
        self.second_strip_end = 0
        self.extra_8_bytes = False
        self.tries = 0

    def read(self, reader: ByteIO, model: SourceVtxModel):
        entry = reader.tell()
        self.lod = len(model.vtx_model_lods)
        self.meshCount = reader.read_uint32()
        self.meshOffset = reader.read_uint32()
        self.switchPoint = reader.read_float()
        with reader.save_current_pos():
            if self.meshOffset > 0:
                reader.seek(entry + self.meshOffset)
                # analyze
                for _ in range(self.meshCount):
                    SourceVtxMesh().read(reader, self, analyze=True)
                # actually read
                reader.seek(entry + self.meshOffset)
                for _ in range(self.meshCount):
                    self.vtx_meshes.append(SourceVtxMesh().read(reader, self, analyze=False))
        return self

    def __repr__(self):
        return "<ModelLod mesh count:{} meshes:{}>".format(self.meshCount, self.vtx_meshes)


class SourceVtxMesh:
    extra_8 = True
    final = False

    @classmethod
    def set_extra_8(cls, extra_8):
        cls.extra_8 = extra_8

    @classmethod
    def set_final(cls, final):
        cls.final = final

    def __init__(self):
        self.strip_group_count = 0
        self.strip_group_offset = 0
        self.flags = 0
        self.vtx_strip_groups = []

    def read(self, reader: ByteIO, lod: SourceVtxModelLod, analyze=False):
        entry = reader.tell()
        self.strip_group_count = reader.read_uint32()
        self.strip_group_offset = reader.read_uint32()
        self.flags = reader.read_uint8()
        if analyze:
            if self.strip_group_count > 0 and self.strip_group_offset != 0:
                if lod.first_strip_end == 0:
                    with reader.save_current_pos():
                        reader.seek(entry + self.strip_group_offset)
                        for _ in range(self.strip_group_count):
                            SourceVtxStripGroup().read(reader, self.extra_8, read_other=False)
                        lod.first_strip_end = reader.tell()

                        return
                elif lod.second_strip_end == 0:
                    SourceVtxStripGroup().read(reader, self.extra_8, read_other=False)
                    lod.second_strip_end = reader.tell()
                    with reader.save_current_pos():
                        if lod.first_strip_end == entry + self.strip_group_offset:
                            pass
                        else:
                            if not self.final:
                                self.set_extra_8(not self.extra_8)
                                # self.set_final(not self.extra_8)
                        reader.seek(entry + self.strip_group_offset)

        if not analyze:
            # print('extra 8', self.extra_8)
            with reader.save_current_pos():
                if self.strip_group_offset > 0:
                    reader.seek(entry + self.strip_group_offset)
                    for _ in range(self.strip_group_count):
                        self.vtx_strip_groups.append(SourceVtxStripGroup().read(reader, self.extra_8, read_other=True))
        return self

    def __repr__(self):
        return "<Mesh strip group count:{} stripgroup offset:{} stripgroups:{}>".format(self.strip_group_count,
                                                                                          self.strip_group_offset,
                                                                                          self.vtx_strip_groups)


class SourceVtxStripGroup:

    def __init__(self):
        self.vertex_count = 0
        self.vertex_offset = 0
        self.index_count = 0
        self.index_offset = 0
        self.strip_count = 0
        self.strip_offset = 0
        self.flags = 0
        self.topology_index_count = 0
        self.topology_index_offset = 0
        self.vtx_vertexes = []
        self.vtx_indexes = []
        self.vtx_strips = []
        self.retry = 0

    def read(self, reader: ByteIO, extra_8=True, read_other=True):

        entry = reader.tell()
        self.vertex_count = reader.read_uint32()
        self.vertex_offset = reader.read_uint32()
        self.index_count = reader.read_uint32()
        self.index_offset = reader.read_uint32()
        self.strip_count = reader.read_uint32()
        self.strip_offset = reader.read_uint32()
        self.flags = reader.read_uint8()
        if extra_8:
            reader.skip(8)
        if read_other:
            with reader.save_current_pos():
                reader.seek(entry + self.index_offset)
                for _ in range(self.index_count):
                    self.vtx_indexes.append(reader.read_uint16())
                reader.seek(entry + self.vertex_offset)
                for _ in range(self.vertex_count):
                    SourceVtxVertex().read(reader, self)
                reader.seek(entry + self.strip_offset)
                for _ in range(self.strip_count):
                    SourceVtxStrip().read(reader, self)

        return self

    def __repr__(self):
        return "<StripGroup Vertex count:{} Index count:{} Strip count:{}>".format(self.vertex_count, self.index_count,
                                                                                   self.strip_count)

    def ___repr__(self):
        return pformat(self.__dict__)


class SourceVtxVertex:
    def __init__(self):
        self.bone_weight_index = []
        self.bone_count = 0
        self.original_mesh_vertex_index = 0
        self.bone_id = []

    def read(self, reader: ByteIO, stripgroup: SourceVtxStripGroup):
        global max_bones_per_vertex
        self.bone_weight_index = [reader.read_uint8() for _ in range(max_bones_per_vertex)]
        self.bone_count = reader.read_uint8()
        self.original_mesh_vertex_index = reader.read_uint16()
        self.bone_id = [reader.read_uint8() for _ in range(max_bones_per_vertex)]
        stripgroup.vtx_vertexes.append(self)

    def __repr__(self):
        return "<Vertex bone:{} total bone count:{}>".format(self.bone_id, self.bone_count)


class SourceVtxStrip:
    def __init__(self):
        self.index_count = 0
        self.index_offset = 0
        self.index_mesh_index = 0
        self.vertex_count = 0
        self.vertex_mesh_index = 0

        self.bone_count = 0
        self.flags = 0
        self.bone_state_change_count = 0
        self.bone_state_change_offset = 0
        self.vtx_indexes = []
        self.vtx_bone_state_changes = []

    def read(self, reader: ByteIO, stripgroup: SourceVtxStripGroup):
        self.index_count = reader.read_uint32()
        self.index_mesh_index = reader.read_uint32()
        self.vertex_count = reader.read_uint32()
        self.vertex_mesh_index = reader.read_uint32()
        self.bone_count = reader.read_uint16()
        self.flags = reader.read_uint8()
        self.bone_state_change_count = reader.read_uint32()
        self.bone_state_change_offset = reader.read_uint32()
        stripgroup.vtx_strips.append(self)
