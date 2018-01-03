from pprint import pformat

from ByteReader import ByteReader

maxBonesPerVertex = 3
extra8bytes = False


class SourceVtxFileData:
    def __init__(self):
        self.version = 0
        self.vertexCacheSize = 0
        self.maxBonesPerStrip = 3
        self.maxBonesPerTri = 3
        self.maxBonesPerVertex = 3
        self.checksum = 0
        self.lodCount = 0
        self.ReplacementListOffset = 0
        self.bodyPartCount = 0
        self.bodyPartOffset = 0
        self.theVtxBodyParts = []

    def read(self, reader: ByteReader):
        self.version = reader.readInt32()
        self.vertexCacheSize = reader.readInt32()
        self.maxBonesPerStrip = reader.readUInt16()
        self.maxBonesPerTri = reader.readUInt16()
        self.maxBonesPerVertex = reader.readInt32()
        self.checksum = reader.readUInt32()
        self.lodCount = reader.readInt32()
        self.materialReplacementListOffset = reader.readInt32()
        self.bodyPartCount = reader.readInt32()
        self.bodyPartOffset = reader.readInt32()
        global maxBonesPerVertex
        maxBonesPerVertex = self.maxBonesPerVertex

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

    def read(self, reader: ByteReader, vtx: SourceVtxFileData):
        entry = reader.tell()
        self.modelCount = reader.readInt32()
        self.modelOffset = reader.readInt32()
        entry2 = reader.tell()
        if self.modelCount > 0 and self.modelOffset != 0:
            reader.seek(entry + self.modelOffset,0)
            for _ in range(self.modelCount):
                SourceVtxModel().read(reader, self)
        reader.seek(entry2)
        vtx.theVtxBodyParts.append(self)


    def __repr__(self):
        return "\n<BodyPart model count:{} models:{}>".format(self.modelCount, self.theVtxModels)


class SourceVtxModel:
    def __init__(self):
        self.lodCount = 0
        self.lodOffset = 0
        self.theVtxModelLods = []

    def read(self, reader: ByteReader, bodypart: SourceVtxBodyPart):
        entry = reader.tell()
        self.lodCount = reader.readInt32()
        self.lodOffset = reader.readInt32()
        entry2 = reader.tell()
        if self.lodCount > 0 and self.lodOffset != 0:
            reader.seek(entry + self.lodOffset)
            for _ in range(self.lodCount):
                SourceVtxModelLod().read(reader, self)
        reader.seek(entry2)
        bodypart.theVtxModels.append(self)


    def __repr__(self):
        return "\n<Model lod count:{} lods:{}>".format(self.lodCount, self.theVtxModelLods)


class SourceVtxModelLod:
    def __init__(self):
        self.lod = 0
        self.meshCount = 0
        self.meshOffset = 0
        self.switchPoint = 0
        self.theVtxMeshes = []
        self.theFirstMeshWithStripGroups = None
        self.theSecondMeshWithStripGroups = None
        self.theStripGroupUsesExtra8Bytes = False
        self.theExpectedStartOfSecondStripGroupList = 0
        self.theFirstMeshWithStripGroupsInputFileStreamPosition = 0
        self.tries = 0

    def read(self, reader: ByteReader, model: SourceVtxModel):
        self.lod = len(model.theVtxModelLods)
        entry = reader.tell()
        self.meshCount = reader.readInt32()
        self.meshOffset = reader.readInt32()
        self.switchPoint = reader.readFloat()
        entry2 = reader.tell()

        reader.seek(entry + self.meshOffset)
        for _ in range(self.meshCount):
            SourceVtxMesh().read(reader, self)
        reader.seek(entry2)
        model.theVtxModelLods.append(self)



    def __repr__(self):
        return "\n<ModelLod mesh count:{} meshes:{}>".format(self.meshCount, self.theVtxMeshes)


class SourceVtxMesh:
    def __init__(self):
        self.stripGroupCount = 0
        self.stripGroupOffset = 0
        self.flags = 0
        self.theVtxStripGroups = []
        self.retry = 0

    def read(self, reader: ByteReader, lod: SourceVtxModelLod):
        entry = reader.tell()
        self.stripGroupCount = reader.readInt32()
        self.stripGroupOffset = reader.readInt32()
        self.flags = reader.readUByte()
        entry2 = reader.tell()
        reader.seek(entry + self.stripGroupOffset)
        for _ in range(self.stripGroupCount):
            SourceVtxStripGroup().read(reader, self)
        reader.seek(entry2)
        lod.theVtxMeshes.append(self)

    def __repr__(self):
        return "\n<Mesh strip group count:{} stripgroup offset:{} stripgroups:{}>".format(self.stripGroupCount,
                                                                                          self.stripGroupOffset,
                                                                                          self.theVtxStripGroups)



class SourceVtxStripGroup:
    extra8bytes = False

    def __init__(self):
        self.vertexCount = 0
        self.vertexOffset = 0
        self.indexCount = 0
        self.indexOffset = 0
        self.stripCount = 0
        self.stripOffset = 0
        self.topologyIndexCount = 0
        self.topologyIndexOffset = 0
        self.theVtxVertexes = []
        self.theVtxIndexes = []
        self.theVtxStrips = []
        self.retry = 0

    def read(self, reader: ByteReader, mesh: SourceVtxMesh):
        entry = reader.tell()
        self.vertexCount = reader.readInt32()
        self.vertexOffset = reader.readInt32()
        self.indexCount = reader.readInt32()
        self.indexOffset = reader.readInt32()
        self.stripCount = reader.readInt32()
        self.stripOffset = reader.readInt32()
        self.vertexCount = reader.readUByte()
        if self.extra8bytes:
            reader.read(8)
        entry2 = reader.tell()
        # try:
        #     reader.seek(entry + self.indexOffset)
        #     for _ in range(self.indexCount):
        #         self.theVtxIndexes.append(reader.readUInt16())
        #     reader.seek(entry+self.vertexOffset)
        #     for _ in range(self.vertexCount):
        #         SourceVtxVertex().read(reader,self)
        #     reader.seek(entry+self.stripOffset)
        #     for _ in range(self.stripCount):
        #         SourceVtxStrip().read(reader,self)
        #     reader.seek(entry2)
        # except:
        #     self.extra8bytes = not self.extra8bytes
        #     reader.seek(entry)
        #     self.retry+=1
        #     if self.retry > 3:
        #         raise Exception("Can't read VTX file")
        #     self.read(reader,mesh)


        reader.seek(entry2)
        mesh.theVtxStripGroups.append(self)

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

    def read(self, reader: ByteReader, stripgroup: SourceVtxStripGroup):
        global maxBonesPerVertex
        self.boneWeightIndex = [reader.readUByte() for _ in range(maxBonesPerVertex)]
        self.boneCount = reader.readUByte()
        self.originalMeshVertexIndex = reader.readUInt16()
        self.boneId = [reader.readUByte() for _ in range(maxBonesPerVertex)]
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

    def read(self, reader: ByteReader, stripgroup: SourceVtxStripGroup):
        self.indexCount = reader.readInt32()
        self.indexMeshIndex = reader.readInt32()
        self.vertexCount = reader.readInt32()
        self.vertexMeshIndex = reader.readInt32()
        self.boneCount = reader.readInt16()
        self.flags = reader.readUByte()
        self.boneStateChangeCount = reader.readInt32()
        self.boneStateChangeOffset = reader.readInt32()
        stripgroup.theVtxStrips.append(self)
