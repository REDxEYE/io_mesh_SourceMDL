from pprint import pformat
try:
    from .ByteIO import ByteIO
except:
    from ByteIO import ByteIO

maxBonesPerVertex = 3


class SourceVtxFileData:
    def __init__(self):
        self.version = 0
        self.vertexCacheSize = 0
        self.maxBonesPerStrip = 3
        self.maxBonesPerTri = 3
        self.maxBonesPerVertex = 3
        self.checksum = 0
        self.lodCount = 0
        self.materialReplacementListOffset = 0
        self.bodyPartCount = 0
        self.bodyPartOffset = 0
        self.theVtxBodyParts = []

    def read(self, reader: ByteIO):
        self.version = reader.read_uint32()
        self.vertexCacheSize = reader.read_uint32()
        self.maxBonesPerStrip = reader.read_uint16()
        self.maxBonesPerTri = reader.read_uint16()
        self.maxBonesPerVertex = reader.read_uint32()
        self.checksum = reader.read_uint32()
        self.lodCount = reader.read_uint32()
        self.materialReplacementListOffset = reader.read_uint32()
        self.bodyPartCount = reader.read_uint32()
        self.bodyPartOffset = reader.read_uint32()
        global maxBonesPerVertex
        maxBonesPerVertex = self.maxBonesPerVertex
        if self.bodyPartOffset>0:
            for _ in range(self.bodyPartCount):
                self.theVtxBodyParts.append(SourceVtxBodyPart().read(reader))

    def __repr__(self):
        return "<FileData version:{} lod count:{} body part count:{} \nbodyparts:{}>\n".format(self.version,
                                                                                               self.lodCount,
                                                                                               self.bodyPartCount,
                                                                                               self.theVtxBodyParts)


class SourceVtxBodyPart:
    def __init__(self):
        self.modelCount = 0
        self.modelOffset = 0
        self.theVtxModels = []

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.modelCount = reader.read_uint32()
        self.modelOffset = reader.read_uint32()
        with reader.save_current_pos():
            reader.seek(entry+self.modelOffset)
            for _ in range(self.modelCount):
                self.theVtxModels.append(SourceVtxModel().read(reader))
        return self



    def __repr__(self):
        return "\n<BodyPart model count:{} models:{}>".format(self.modelCount, self.theVtxModels)


class SourceVtxModel:
    def __init__(self):
        self.lodCount = 0
        self.lodOffset = 0
        self.theVtxModelLods = []

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.lodCount = reader.read_uint32()
        self.lodOffset = reader.read_uint32()
        with reader.save_current_pos():
            if self.lodCount > 0 and self.lodOffset != 0:
                reader.seek(entry + self.lodOffset)
                for _ in range(self.lodCount):
                    self.theVtxModelLods.append(SourceVtxModelLod().read(reader,self))
        return self


    def __repr__(self):
        return "\n<Model  lod count:{} lods:{}>".format(self.lodCount, self.theVtxModelLods)


class SourceVtxModelLod:
    def __init__(self):
        self.lod = 0
        self.meshCount = 0
        self.meshOffset = 0
        self.switchPoint = 0
        self.theVtxMeshes = []
        self.first_strip_end = 0
        self.second_strip_end = 0
        self.extra_8_bytes = False
        self.tries = 0

    def read(self, reader: ByteIO, model: SourceVtxModel):
        entry = reader.tell()
        self.lod = len(model.theVtxModelLods)
        self.meshCount = reader.read_uint32()
        self.meshOffset = reader.read_uint32()
        self.switchPoint = reader.read_float()
        with reader.save_current_pos():
            if self.meshOffset>0:
                reader.seek(entry + self.meshOffset)
                # analyze
                for _ in range(self.meshCount):
                    SourceVtxMesh().read(reader,self,analyze=True)
                # actually read
                reader.seek(entry + self.meshOffset)
                for _ in range(self.meshCount):
                    self.theVtxMeshes.append(SourceVtxMesh().read(reader, self,analyze=False))
        return self



    def __repr__(self):
        return "\n<ModelLod mesh count:{} meshes:{}>".format(self.meshCount, self.theVtxMeshes)


class SourceVtxMesh:
    extra_8 = True
    final = False
    @classmethod
    def set_extra_8(cls,extra_8):
        cls.extra_8 = extra_8
    @classmethod
    def set_final(cls,final):
        cls.final = final

    def __init__(self):
        self.stripGroupCount = 0
        self.stripGroupOffset = 0
        self.flags = 0
        self.theVtxStripGroups = []

    def read(self, reader: ByteIO,lod:SourceVtxModelLod,analyze = False):
        entry = reader.tell()
        self.stripGroupCount = reader.read_uint32()
        self.stripGroupOffset = reader.read_uint32()
        self.flags = reader.read_uint8()
        if analyze:
            if self.stripGroupCount>0 and self.stripGroupOffset!=0:
                if lod.first_strip_end == 0:
                    with reader.save_current_pos():
                        reader.seek(entry+self.stripGroupOffset)
                        for _ in range(self.stripGroupCount):
                            SourceVtxStripGroup().read(reader,self.extra_8,read_other=False)
                        lod.first_strip_end = reader.tell()

                        return
                elif lod.second_strip_end == 0:
                    SourceVtxStripGroup().read(reader, self.extra_8, read_other=False)
                    lod.second_strip_end = reader.tell()
                    with reader.save_current_pos():
                        if lod.first_strip_end == entry + self.stripGroupOffset:
                            pass
                        else:
                            if not self.final:
                                self.set_extra_8(not self.extra_8)
                                #self.set_final(not self.extra_8)
                        reader.seek(entry+self.stripGroupOffset)


        if not analyze:
            #print('extra 8', self.extra_8)
            with reader.save_current_pos():
                if self.stripGroupOffset>0:
                    reader.seek(entry + self.stripGroupOffset)
                    for _ in range(self.stripGroupCount):
                        self.theVtxStripGroups.append(SourceVtxStripGroup().read(reader,self.extra_8,read_other=True))
        return self

    def __repr__(self):
        return "\n<Mesh strip group count:{} stripgroup offset:{} stripgroups:{}>".format(self.stripGroupCount,
                                                                                          self.stripGroupOffset,
                                                                                          self.theVtxStripGroups)



class SourceVtxStripGroup:

    def __init__(self):
        self.vertexCount = 0
        self.vertexOffset = 0
        self.indexCount = 0
        self.indexOffset = 0
        self.stripCount = 0
        self.stripOffset = 0
        self.flags = 0
        self.topologyIndexCount = 0
        self.topologyIndexOffset = 0
        self.theVtxVertexes = []
        self.theVtxIndexes = []
        self.theVtxStrips = []
        self.retry = 0

    def read(self, reader: ByteIO,extra_8 = True,read_other = True):

        entry = reader.tell()
        self.vertexCount = reader.read_uint32()
        self.vertexOffset = reader.read_uint32()
        self.indexCount = reader.read_uint32()
        self.indexOffset = reader.read_uint32()
        self.stripCount = reader.read_uint32()
        self.stripOffset = reader.read_uint32()
        self.flags = reader.read_uint8()
        if extra_8:
            reader.skip(8)
        if read_other:
            with reader.save_current_pos():
                reader.seek(entry + self.indexOffset)
                for _ in range(self.indexCount):
                    self.theVtxIndexes.append(reader.read_uint16())
                reader.seek(entry+self.vertexOffset)
                for _ in range(self.vertexCount):
                    SourceVtxVertex().read(reader,self)
                reader.seek(entry+self.stripOffset)
                for _ in range(self.stripCount):
                    SourceVtxStrip().read(reader,self)


        return self

    def __repr__(self):
        return "<StripGroup Vertex count:{} Index count:{} Strip count:{}>".format(self.vertexCount, self.indexCount,
                                                                                   self.stripCount)

    def ___repr__(self):
        return pformat(self.__dict__)


class SourceVtxVertex:
    def __init__(self):
        self.boneWeightIndex = []
        self.boneCount = b'\x00'
        self.originalMeshVertexIndex = 0
        self.boneId = []

    def read(self, reader: ByteIO, stripgroup: SourceVtxStripGroup):
        global maxBonesPerVertex
        self.boneWeightIndex = [reader.read_uint8() for _ in range(maxBonesPerVertex)]
        self.boneCount = reader.read_uint8()
        self.originalMeshVertexIndex = reader.read_uint16()
        self.boneId = [reader.read_uint8() for _ in range(maxBonesPerVertex)]
        stripgroup.theVtxVertexes.append(self)

    def __repr__(self):
        return "<Vertex bone:{} total bone count:{}>".format(self.boneId, self.boneCount)


class SourceVtxStrip:
    def __init__(self):
        self.indexCount = 0
        self.indexOffset = 0
        self.indexMeshIndex = 0
        self.vertexCount = 0
        self.vertexMeshIndex = 0

        self.boneCount = 0
        self.flags = b'\x00'
        self.boneStateChangeCount = 0
        self.boneStateChangeOffset = 0
        self.theVtxIndexes = []
        self.theVtxBoneStateChanges = []

    def read(self, reader: ByteIO, stripgroup: SourceVtxStripGroup):
        self.indexCount = reader.read_uint32()
        self.indexMeshIndex = reader.read_uint32()
        self.vertexCount = reader.read_uint32()
        self.vertexMeshIndex = reader.read_uint32()
        self.boneCount = reader.read_uint16()
        self.flags = reader.read_uint8()
        self.boneStateChangeCount = reader.read_uint32()
        self.boneStateChangeOffset = reader.read_uint32()
        stripgroup.theVtxStrips.append(self)
