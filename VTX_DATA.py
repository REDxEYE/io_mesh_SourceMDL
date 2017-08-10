from pprint import pformat


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

class SourceVtxBodyPart:
    def __init__(self):
        self.modelCount = 0
        self.modelOffset = 0
        self.theVtxModels = []
    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceVtxModel:
    def __init__(self):
        self.lodCount  = 0
        self.lodOffset = 0
        self.theVtxModelLods = []
    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceVtxModelLod:
    def __init__(self):
        self.lod = 0
        self.meshCount =0
        self.meshOffset =0
        self.switchPoint =0
        self.theVtxMeshes = []
    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceVtxMesh:
    def __init__(self):
        self.stripGroupCount = 0
        self.stripGroupOffset = 0
        self.flags = b'\x00'
        self.theVtxStripGroups = []
    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceVtxStripGroup:
    def __init__(self):
        self.vertexCount = 0
        self.vertexOffset = 0
        self.indexCount = 0
        self.indexOffset = 0
        self.stripCount = 0
        self.stripOffset = 0
        self.flags = b'\x00'
        self.topologyIndexCount = 0
        self.topologyIndexOffset = 0
        self.theVtxVertexes = []
        self.theVtxIndexes = []
        self.theVtxStrips = []

class SourceVtxVertex:
    def __init__(self):
        self.boneWeightIndex = []
        self.boneCount = b'\x00'
        self.originalMeshVertexIndex = 0
        self.boneId = []

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

class SourceVtxBoneStateChange:
    def __init__(self):
        self.hardwareId = 0
        self.newBoneId = 0



