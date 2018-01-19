import random
from pprint import pformat, pprint

import sys
from typing import List

import io



try:
    from .ByteIO import ByteIO
    from .GLOBALS import SourceVector, SourceQuaternion, SourceFloat16bits
    from . import VTX,VVD

except:
    from ByteIO import ByteIO
    from GLOBALS import SourceVector, SourceQuaternion, SourceFloat16bits
    import VTX,VVD

class SourceMdlAnimationDesc:
    def __init__(self):
        self.theName = ''


class SourceMdlFileData:
    def __init__(self):
        self.id = []
        self.version = 0
        self.checksum = 0
        self.name = []
        self.nameForVtmb = []
        self.fileSize = 0
        self.eyePosition = SourceVector()
        self.illuminationPosition = SourceVector()
        self.hullMinPosition = SourceVector()

        self.hullMaxPosition = SourceVector()

        self.viewBoundingBoxMinPosition = SourceVector()

        self.viewBoundingBoxMaxPosition = SourceVector()

        self.flags = 0
        self.boneCount = 0
        self.boneOffset = 0
        self.boneControllerCount = 0
        self.boneControllerOffset = 0
        self.hitboxSetCount = 0
        self.hitboxSetOffset = 0
        self.localAnimationCount = 0
        self.localAnimationOffset = 0
        self.localSequenceCount = 0
        self.localSequenceOffset = 0
        self.sequenceGroupCount = 0
        self.sequenceGroupOffset = 0
        self.activityListVersion = 0
        self.eventsIndexed = 0
        self.textureCount = 0
        self.textureOffset = 0
        self.texturePathCount = 0
        self.texturePathOffset = 0
        self.skinReferenceCount = 0
        self.skinFamilyCount = 0
        self.skinFamilyOffset = 0
        self.bodyPartCount = 0
        self.bodyPartOffset = 0
        self.localAttachmentCount = 0
        self.localAttachmentOffset = 0
        self.soundtable = 0
        self.soundindex = 0
        self.soundgroups = 0
        self.soundgroupindex = 0
        self.localNodeCount = 0
        self.localNodeOffset = 0
        self.localNodeNameOffset = 0
        self.flexDescCount = 0
        self.flexDescOffset = 0
        self.flexControllerCount = 0
        self.flexControllerOffset = 0
        self.flexRuleCount = 0
        self.flexRuleOffset = 0
        self.ikChainCount = 0
        self.ikChainOffset = 0
        self.mouthCount = 0
        self.mouthOffset = 0
        self.localPoseParamaterCount = 0
        self.localPoseParameterOffset = 0
        self.surfacePropOffset = 0
        self.keyValueOffset = 0
        self.keyValueSize = 0
        self.localIkAutoPlayLockCount = 0
        self.localIkAutoPlayLockOffset = 0
        self.mass = 0.0
        self.contents = 0
        self.includeModelCount = 0
        self.includeModelOffset = 0
        self.virtualModelP = 0
        self.animBlockNameOffset = 0
        self.animBlockCount = 0
        self.animBlockOffset = 0
        self.animBlockModelP = 0
        self.boneTableByNameOffset = 0
        self.vertexBaseP = 0
        self.indexBaseP = 0
        self.directionalLightDot = b'\x00'
        self.rootLod = b'\x00'
        self.allowedRootLodCount = b'\x00'
        self.unused = b'\x00'
        self.zeroframecacheindex_VERSION44_47 = 0
        self.unused4 = 0
        self.flexControllerUiCount = 0
        self.flexControllerUiOffset = 0
        self.vertAnimFixedPointScale = 0
        self.surfacePropLookup = 0
        self.unused3 = []
        self.studioHeader2Offset = 0
        self.boneFlexDriverCount = 0
        self.unused2 = 0
        self.sourceBoneTransformCount = 0
        self.sourceBoneTransformOffset = 0
        self.boneFlexDriverOffset = 0
        self.illumPositionAttachmentIndex = 0
        self.maxEyeDeflection = 0
        self.linearBoneOffset = 0
        self.reserved = [None] * 56
        self.theID = ""
        self.theName = ""
        self.theAnimationDescs = []
        self.theAnimBlocks = []
        self.theAnimBlockRelativePathFileName = ""
        self.theAttachments = []
        self.theBodyParts = []
        self.theBones = [] #type: List[SourceMdlBone]
        self.theBoneControllers = []
        self.theBoneTableByName = []
        self.theFlexDescs = [] #type: List[SourceMdlFlexDesc]
        self.theFlexControllers = []
        self.theFlexControllerUis = []
        self.theFlexRules = []
        self.theHitboxSets = []
        self.theIkChains = []
        self.theIkLocks = []
        self.theKeyValuesText = ""
        self.theLocalNodeNames = []
        self.theModelGroups = []
        self.theMouths = []
        self.thePoseParamDescs = []
        self.theSequenceDescs = []
        self.theSkinFamilies = []
        self.theSurfacePropName = ""
        self.theTexturePaths = []
        self.theTextures = [] #type: List[SourceMdlTexture]
        self.theSectionFrameCount = 0
        self.theSectionFrameMinFrameCount = 0
        self.theActualFileSize = 0
        self.theModelCommandIsUsed = False
        self.theFlexFrames = []
        self.theEyelidFlexFrameIndexes = []
        self.theFirstAnimationDesc = None
        self.theFirstAnimationDescFrameLines = {}
        self.theMdlFileOnlyHasAnimations = False
        self.theProceduralBonesCommandIsUsed = False
        self.theWeightLists = []
        self.nameOffset = 0

    def read(self, reader: ByteIO):
        self.readHeader00(reader)
        self.readHeader01(reader)
        self.ReadHeader02(reader)

    def readHeader00(self, reader: ByteIO):
        self.id = ''.join(list([chr(reader.read_uint8()) for _ in range(4)]))
        self.version = reader.read_uint32()
        self.checksum = reader.read_uint32()
        self.name = reader.read_ascii_string(64)
        self.fileSize = reader.read_uint32()

    def readHeader01(self, reader: ByteIO):
        self.eyePosition.read(reader)

        self.illuminationPosition.read(reader)

        self.hullMinPosition.read(reader)

        self.hullMaxPosition.read(reader)

        self.viewBoundingBoxMinPosition.read(reader)

        self.viewBoundingBoxMaxPosition.read(reader)

        self.flags = reader.read_uint32()

        self.boneCount = reader.read_uint32()
        self.boneOffset = reader.read_uint32()

        self.boneControllerCount = reader.read_uint32()
        self.boneControllerOffset = reader.read_uint32()

        self.hitboxSetCount = reader.read_uint32()
        self.hitboxSetOffset = reader.read_uint32()

        self.localAnimationCount = reader.read_uint32()
        self.localAnimationOffset = reader.read_uint32()

        self.localSequenceCount = reader.read_uint32()
        self.localSequenceOffset = reader.read_uint32()

        self.activityListVersion = reader.read_uint32()
        self.eventsIndexed = reader.read_uint32()

        self.textureCount = reader.read_uint32()
        self.textureOffset = reader.read_uint32()
        self.texturePathCount = reader.read_uint32()
        self.texturePathOffset = reader.read_uint32()

        self.skinReferenceCount = reader.read_uint32()
        self.skinFamilyCount = reader.read_uint32()
        self.skinFamilyOffset = reader.read_uint32()

        self.bodyPartCount = reader.read_uint32()
        self.bodyPartOffset = reader.read_uint32()

        self.localAttachmentCount = reader.read_uint32()
        self.localAttachmentOffset = reader.read_uint32()

        self.localNodeCount = reader.read_uint32()
        self.localNodeOffset = reader.read_uint32()
        self.localNodeNameOffset = reader.read_uint32()

        self.flexDescCount = reader.read_uint32()
        self.flexDescOffset = reader.read_uint32()

        self.flexControllerCount = reader.read_uint32()
        self.flexControllerOffset = reader.read_uint32()

        self.flexRuleCount = reader.read_uint32()
        self.flexRuleOffset = reader.read_uint32()

        self.ikChainCount = reader.read_uint32()
        self.ikChainOffset = reader.read_uint32()

        self.mouthCount = reader.read_uint32()
        self.mouthOffset = reader.read_uint32()

        self.localPoseParamaterCount = reader.read_uint32()
        self.localPoseParameterOffset = reader.read_uint32()

        self.surfacePropOffset = reader.read_uint32()

        if self.surfacePropOffset > 0:
            self.theSurfacePropName = reader.read_from_offset(self.surfacePropOffset,reader.read_ascii_string)

        self.keyValueOffset = reader.read_uint32()
        self.keyValueSize = reader.read_uint32()

        self.localIkAutoPlayLockOffset = reader.read_uint32()
        self.localIkAutoPlayLockCount = reader.read_uint32()

        self.mass = reader.read_float()
        self.contents = reader.read_uint32()

        self.includeModelCount = reader.read_uint32()
        self.includeModelOffset = reader.read_uint32()

        self.virtualModelP = reader.read_uint32()

        self.animBlockNameOffset = reader.read_uint32()
        self.animBlockCount = reader.read_uint32()
        self.animBlockOffset = reader.read_uint32()
        self.animBlockModelP = reader.read_uint32()

        if self.animBlockCount > 0:
            if self.animBlockNameOffset > 0:
                self.theAnimBlockRelativePathFileName = reader.read_from_offset(reader.tell()+self.animBlockNameOffset,reader.read_ascii_string)

        if self.animBlockOffset > 0:
            backpos = reader.tell()
            reader.seek(self.animBlockOffset, 0)
            for offset in range(self.animBlockCount):
                anAnimBlock = SourceMdlAnimBlock()
                anAnimBlock.read(reader)
                self.theAnimBlocks.append(anAnimBlock)
            reader.seek(backpos, 0)

        self.boneTableByNameOffset = reader.read_uint32()

        self.vertexBaseP = reader.read_uint32()
        self.indexBaseP = reader.read_uint32()

        self.directionalLightDot = reader.read_uint8()

        self.rootLod = reader.read_uint8()

        self.allowedRootLodCount = reader.read_uint8()

        self.unused = reader.read_uint8()

        self.unused4 = reader.read_uint32()

        self.flexControllerUiCount = reader.read_uint32()
        self.flexControllerUiOffset = reader.read_uint32()

        self.vertAnimFixedPointScale = reader.read_float()
        self.surfacePropOffset = reader.read_uint32()

        self.studioHeader2Offset = reader.read_uint32()

        self.unused2 = reader.read_uint32()

        if self.bodyPartCount == 0 and self.localSequenceCount > 0:
            self.theMdlFileOnlyHasAnimations = True

    def ReadHeader02(self, reader: ByteIO):

        self.sourceBoneTransformCount = reader.read_uint32()
        self.sourceBoneTransformOffset = reader.read_uint32()
        self.illumPositionAttachmentIndex = reader.read_uint32()
        self.maxEyeDeflection = reader.read_float()
        self.linearBoneOffset = reader.read_uint32()

        self.nameOffset = reader.read_uint32()
        self.boneFlexDriverCount = reader.read_uint32()
        self.boneTableByNameOffset = reader.read_uint32()
        self.reserved = list([reader.read_uint32() for _ in range(56)])

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)


class SourceMdlFileDataV53:
    def __init__(self):
        self.id = []
        self.version = 0
        self.checksum = 0
        self.nameCopyOffset = 0
        self.name = []
        self.fileSize = 0
        self.eyePosition = SourceVector()
        self.illuminationPosition = SourceVector()
        self.hullMinPosition = SourceVector()
        self.hullMaxPosition = SourceVector()
        self.viewBoundingBoxMinPosition = SourceVector()
        self.viewBoundingBoxMaxPosition = SourceVector()
        self.flags = 0
        self.boneCount = 0
        self.boneOffset = 0
        self.boneControllerCount = 0
        self.boneControllerOffset = 0
        self.hitboxSetCount = 0
        self.hitboxSetOffset = 0
        self.localAnimationCount = 0
        self.localAnimationOffset = 0
        self.localSequenceCount = 0
        self.localSequenceOffset = 0
        self.sequenceGroupCount = 0
        self.sequenceGroupOffset = 0
        self.activityListVersion = 0
        self.eventsIndexed = 0
        self.textureCount = 0
        self.textureOffset = 0
        self.texturePathCount = 0
        self.texturePathOffset = 0
        self.skinReferenceCount = 0
        self.skinFamilyCount = 0
        self.skinFamilyOffset = 0
        self.bodyPartCount = 0
        self.bodyPartOffset = 0
        self.localAttachmentCount = 0
        self.localAttachmentOffset = 0
        self.soundtable = 0
        self.soundindex = 0
        self.soundgroups = 0
        self.soundgroupindex = 0
        self.localNodeCount = 0
        self.localNodeOffset = 0
        self.localNodeNameOffset = 0
        self.flexDescCount = 0
        self.flexDescOffset = 0
        self.flexControllerCount = 0
        self.flexControllerOffset = 0
        self.flexRuleCount = 0
        self.flexRuleOffset = 0
        self.ikChainCount = 0
        self.ikChainOffset = 0
        self.mouthCount = 0
        self.mouthOffset = 0
        self.localPoseParamaterCount = 0
        self.localPoseParameterOffset = 0
        self.surfacePropOffset = 0
        self.keyValueOffset = 0
        self.keyValueSize = 0
        self.localIkAutoPlayLockCount = 0
        self.localIkAutoPlayLockOffset = 0
        self.mass = 0.0
        self.contents = 0
        self.includeModelCount = 0
        self.includeModelOffset = 0
        self.virtualModelP = 0
        self.animBlockNameOffset = 0
        self.animBlockCount = 0
        self.animBlockOffset = 0
        self.animBlockModelP = 0
        self.boneTableByNameOffset = 0
        self.vertexBaseP = 0
        self.indexBaseP = 0
        self.directionalLightDot = b'\x00'
        self.rootLod = b'\x00'
        self.allowedRootLodCount = b'\x00'
        self.unused = b'\x00'
        self.zeroframecacheindex_VERSION44_47 = 0
        self.unused4 = 0
        self.flexControllerUiCount = 0
        self.flexControllerUiOffset = 0
        self.vertAnimFixedPointScale = 0
        self.surfacePropLookup = 0
        self.unused3 = []
        self.studioHeader2Offset = 0
        self.boneFlexDriverCount = 0
        self.unused2 = 0
        self.sourceBoneTransformCount = 0
        self.sourceBoneTransformOffset = 0
        self.boneFlexDriverOffset = 0
        self.illumPositionAttachmentIndex = 0
        self.maxEyeDeflection = 0
        self.linearBoneOffset = 0
        self.reserved = [None]*53
        self.theID = ""
        self.theName = ""
        self.theAnimationDescs = []
        self.theAnimBlocks = []
        self.theAnimBlockRelativePathFileName = ""
        self.theAttachments = []
        self.theBodyParts = []
        self.theBones = []
        self.theBoneControllers = []
        self.theBoneTableByName = []
        self.theFlexDescs = []
        self.theFlexControllers = []
        self.theFlexControllerUis = []
        self.theFlexRules = []
        self.theHitboxSets = []
        self.theIkChains = []
        self.theIkLocks = []
        self.theKeyValuesText = ""
        self.theLocalNodeNames = []
        self.theModelGroups = []
        self.theMouths = []
        self.thePoseParamDescs = []
        self.theSequenceDescs = []
        self.theSkinFamilies = []
        self.theSurfacePropName = ""
        self.theTexturePaths = []
        self.theTextures = []
        self.theSectionFrameCount = 0
        self.theSectionFrameMinFrameCount = 0
        self.theActualFileSize = 0
        self.theModelCommandIsUsed = False
        self.theFlexFrames = []
        self.theEyelidFlexFrameIndexes = []
        self.theFirstAnimationDesc = None
        self.theFirstAnimationDescFrameLines = {}
        self.theMdlFileOnlyHasAnimations = False
        self.theProceduralBonesCommandIsUsed = False
        self.theWeightLists = []

    def read(self, reader: ByteIO):
        self.readHeader00(reader)
        self.readHeader01(reader)
        self.ReadHeader02(reader)

    def readHeader00(self, reader: ByteIO):
        self.id = ''.join(list([chr(reader.read_uint8()) for _ in range(4)]))
        self.version = reader.read_uint32()
        self.checksum = reader.read_uint32()

        self.nameCopyOffset = reader.read_uint32()

        self.name = reader.read_ascii_string(64)
        self.fileSize = reader.read_uint32()

    def readHeader01(self, reader: ByteIO):
        self.eyePosition.read(reader)

        self.illuminationPosition.read(reader)

        self.hullMinPosition.read(reader)

        self.hullMaxPosition.read(reader)

        self.viewBoundingBoxMinPosition.read(reader)

        self.viewBoundingBoxMaxPosition.read(reader)

        self.flags = reader.read_uint32()

        self.boneCount = reader.read_uint32()
        self.boneOffset = reader.read_uint32()

        self.boneControllerCount = reader.read_uint32()
        self.boneControllerOffset = reader.read_uint32()

        self.hitboxSetCount = reader.read_uint32()
        self.hitboxSetOffset = reader.read_uint32()

        self.localAnimationCount = reader.read_uint32()
        self.localAnimationOffset = reader.read_uint32()

        self.localSequenceCount = reader.read_uint32()
        self.localSequenceOffset = reader.read_uint32()

        self.activityListVersion = reader.read_uint32()
        self.eventsIndexed = reader.read_uint32()

        self.textureCount = reader.read_uint32()
        self.textureOffset = reader.read_uint32()
        self.texturePathCount = reader.read_uint32()
        self.texturePathOffset = reader.read_uint32()

        self.skinReferenceCount = reader.read_uint32()
        self.skinFamilyCount = reader.read_uint32()
        self.skinFamilyOffset = reader.read_uint32()

        self.bodyPartCount = reader.read_uint32()
        self.bodyPartOffset = reader.read_uint32()

        self.localAttachmentCount = reader.read_uint32()
        self.localAttachmentOffset = reader.read_uint32()

        self.localNodeCount = reader.read_uint32()
        self.localNodeOffset = reader.read_uint32()

        self.localNodeNameOffset = reader.read_uint32()

        self.flexDescCount = reader.read_uint32()
        self.flexDescOffset = reader.read_uint32()

        self.flexControllerCount = reader.read_uint32()
        self.flexControllerOffset = reader.read_uint32()

        self.flexRuleCount = reader.read_uint32()
        self.flexRuleOffset = reader.read_uint32()

        self.ikChainCount = reader.read_uint32()
        self.ikChainOffset = reader.read_uint32()

        self.mouthCount = reader.read_uint32()
        self.mouthOffset = reader.read_uint32()

        self.localPoseParamaterCount = reader.read_uint32()
        self.localPoseParameterOffset = reader.read_uint32()

        self.surfacePropOffset = reader.read_uint32()

        if self.surfacePropOffset > 0:
            self.theSurfacePropName = reader.read_from_offset(self.surfacePropOffset,reader.read_ascii_string)

        self.keyValueOffset = reader.read_uint32()
        self.keyValueSize = reader.read_uint32()

        self.localIkAutoPlayLockOffset = reader.read_uint32()
        self.localIkAutoPlayLockCount = reader.read_uint32()

        self.mass = reader.read_float()
        self.contents = reader.read_uint32()

        self.includeModelCount = reader.read_uint32()
        self.includeModelOffset = reader.read_uint32()

        self.virtualModelP = reader.read_uint32()

        self.animBlockNameOffset = reader.read_uint32()
        self.animBlockCount = reader.read_uint32()
        self.animBlockOffset = reader.read_uint32()
        self.animBlockModelP = reader.read_uint32()

        if self.animBlockCount > 0:
            if self.animBlockNameOffset > 0:
                self.theAnimBlockRelativePathFileName = reader.read_from_offset(reader.tell()+self.animBlockNameOffset,reader.read_ascii_string)

        if self.animBlockOffset > 0:
            backpos = reader.tell()
            reader.seek(self.animBlockOffset, 0)
            for offset in range(self.animBlockCount):
                anAnimBlock = SourceMdlAnimBlock()
                anAnimBlock.read(reader)
                self.theAnimBlocks.append(anAnimBlock)
            reader.seek(backpos, 0)

        self.boneTableByNameOffset = reader.read_uint32()

        self.vertexBaseP = reader.read_uint32()
        self.indexBaseP = reader.read_uint32()

        self.directionalLightDot = reader.read_uint8()

        self.rootLod = reader.read_uint8()

        self.allowedRootLodCount = reader.read_uint8()

        self.unused = reader.read_uint8()

        self.unused4 = reader.read_uint32()

        self.flexControllerUiCount = reader.read_uint32()
        self.flexControllerUiOffset = reader.read_uint32()

        self.vertAnimFixedPointScale = reader.read_float()
        self.surfacePropOffset = reader.read_uint32()

        self.studioHeader2Offset = reader.read_uint32()

        self.unused2 = reader.read_uint32()

        print('DANGER', reader.tell())
        reader.skip(16)
        self.VTXoffset = reader.read_uint32()
        self.VVDoffset = reader.read_uint32()
        print('Found VTX:{} and VVD:{}'.format(self.VTXoffset, self.VVDoffset))
        if self.VVDoffset != 0 and self.VTXoffset != 0:
            start = reader.tell()
            reader.seek(self.VTXoffset)
            self.VTX = VTX.SourceVtxFile49(file = ByteIO(byte_object = reader._read(-1)))
            reader.seek(self.VVDoffset)
            self.VVD = VVD.SourceVvdFile49(file = ByteIO(byte_object = reader._read(-1)))
            reader.seek(start)

        if self.bodyPartCount == 0 and self.localSequenceCount > 0:
            self.theMdlFileOnlyHasAnimations = True

    def ReadHeader02(self, reader: ByteIO):

        self.sourceBoneTransformCount = reader.read_uint32()
        self.sourceBoneTransformOffset = reader.read_uint32()
        self.illumPositionAttachmentIndex = reader.read_uint32()
        self.maxEyeDeflection = reader.read_float()
        self.linearBoneOffset = reader.read_uint32()

        self.nameOffset = reader.read_uint32()
        self.boneFlexDriverCount = reader.read_uint32()
        self.boneTableByNameOffset = reader.read_uint32()
        self.reserved = list([reader.read_uint32() for _ in range(56)])




class SourceMdlBone:
    BONE_SCREEN_ALIGN_SPHERE = 0x8
    BONE_SCREEN_ALIGN_CYLINDER = 0x10
    BONE_USED_BY_VERTEX_LOD0 = 0x400
    BONE_USED_BY_VERTEX_LOD1 = 0x800
    BONE_USED_BY_VERTEX_LOD2 = 0x1000
    BONE_USED_BY_VERTEX_LOD3 = 0x2000
    BONE_USED_BY_VERTEX_LOD4 = 0x4000
    BONE_USED_BY_VERTEX_LOD5 = 0x8000
    BONE_USED_BY_VERTEX_LOD6 = 0x10000
    BONE_USED_BY_VERTEX_LOD7 = 0x20000
    BONE_USED_BY_BONE_MERGE = 0x40000
    BONE_FIXED_ALIGNMENT = 0x100000
    BONE_HAS_SAVEFRAME_POS = 0x200000
    BONE_HAS_SAVEFRAME_ROT = 0x400000
    def __init__(self):

        self.boneOffset = 0
        self.name = []
        self.boneControllerIndex = []
        self.nameOffset = 0
        self.parentBoneIndex = 0
        self.scale = 0
        self.position = SourceVector()
        self.quat = SourceQuaternion()
        self.animChannels = 0
        self.rotation = SourceVector()
        self.positionScale = SourceVector()
        self.rotationScale = SourceVector()
        self.poseToBoneColumn0 = SourceVector()
        self.poseToBoneColumn1 = SourceVector()
        self.poseToBoneColumn2 = SourceVector()
        self.poseToBoneColumn3 = SourceVector()
        self.qAlignment = SourceQuaternion()
        self.flags = 0
        self.proceduralRuleType = 0
        self.proceduralRuleOffset = 0
        self.physicsBoneIndex = 0
        self.surfacePropNameOffset = 0
        self.contents = 0
        self.unused = []
        self.theName = ""
        self.theAxisInterpBone = None  # type: SourceMdlAxisInterpBone
        self.theQuatInterpBone = None  # type: SourceMdlQuatInterpBone
        self.theJiggleBone = None  # type: SourceMdlJiggleBone
        self.theSurfacePropName = ''
        self.STUDIO_PROC_AXISINTERP = 1
        self.STUDIO_PROC_QUATINTERP = 2
        self.STUDIO_PROC_AIMATBONE = 3
        self.STUDIO_PROC_AIMATATTACH = 4
        self.STUDIO_PROC_JIGGLE = 5

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.boneOffset = reader.tell()
        self.nameOffset = reader.read_uint32()
        self.parentBoneIndex = reader.read_int32()
        self.boneControllerIndex = [reader.read_int32() for _ in range(6)]
        self.position.read(reader)
        self.quat.read(reader)
        self.rotation.read(reader)
        self.positionScale.read(reader)
        self.rotationScale.read(reader)

        x0, x1, x2, x3 = reader.read_float(), reader.read_float(), reader.read_float(), reader.read_float()
        y0, y1, y2, y3 = reader.read_float(), reader.read_float(), reader.read_float(), reader.read_float()
        z0, z1, z2, z3 = reader.read_float(), reader.read_float(), reader.read_float(), reader.read_float()
        self.poseToBoneColumn0.x = x0
        self.poseToBoneColumn0.y = y0
        self.poseToBoneColumn0.z = z0
        self.poseToBoneColumn1.x = x1
        self.poseToBoneColumn1.y = y1
        self.poseToBoneColumn1.z = z1
        self.poseToBoneColumn2.x = x2
        self.poseToBoneColumn2.y = y2
        self.poseToBoneColumn2.z = z2
        self.poseToBoneColumn3.x = x3
        self.poseToBoneColumn3.y = y3
        self.poseToBoneColumn3.z = z3

        self.flags = reader.read_uint32()
        self.qAlignment.read(reader)
        self.proceduralRuleType = reader.read_uint32()
        self.proceduralRuleOffset = reader.read_uint32()
        self.physicsBoneIndex = reader.read_uint32()
        self.surfacePropNameOffset = reader.read_uint32()
        self.contents = reader.read_uint32()
        self.unused = [reader.read_uint32() for _ in range(8)]
        # unused = [reader.read_uint32() for _ in range(9)]
        if self.nameOffset != 0:
            self.name = reader.read_from_offset(self.boneOffset + self.nameOffset,reader.read_ascii_string)
        if self.proceduralRuleType != 0:
            if self.proceduralRuleType == self.STUDIO_PROC_AXISINTERP:
                with reader.save_current_pos():
                    reader.seek(self.boneOffset + self.proceduralRuleOffset)
                    self.theAxisInterpBone = SourceMdlAxisInterpBone().read(reader)
            if self.proceduralRuleType == self.STUDIO_PROC_QUATINTERP:
                with reader.save_current_pos():
                    reader.seek(self.boneOffset + self.proceduralRuleOffset)
                    self.theQuatInterpBone = SourceMdlQuatInterpBone().read(reader)
            if self.proceduralRuleType == self.STUDIO_PROC_JIGGLE:
                with reader.save_current_pos():
                    reader.seek(self.boneOffset + self.proceduralRuleOffset)
                    self.theJiggleBone = SourceMdlJiggleBone().read(reader)
        # print(self.surfacePropNameOffset)
        if self.surfacePropNameOffset != 0:
            self.theSurfacePropName = reader.read_from_offset(self.boneOffset + self.surfacePropNameOffset,reader.read_ascii_string)
        mdl.theBones.append(self)




    def __repr__(self):
        return "<Bone {} pos:{} rot: {} parent index: {}>".format(self.name, self.position.as_string, self.rotation.as_string,self.parentBoneIndex)

class SourceMdlJiggleBone:
    def __init__(self):
        self.flags = 0

        self.length = 0.0

        self.tipMass = 0.0

        self.yawStiffness = 0.0
        self.yawDamping = 0.0

        self.pitchStiffness = 0.0
        self.pitchDamping = 0.0

        self.alongStiffness = 0.0
        self.alongDamping = 0.0
        self.angleLimit = 0.0

        self.minYaw = 0.0
        self.maxYaw = 0.0

        self.yawFriction = 0.0
        self.yawBounce = 0.0

        self.minPitch = 0.0
        self.maxPitch = 0.0

        self.pitchBounce = 0.0
        self.pitchFriction = 0.0

        self.baseMass = 0.0

        self.baseStiffness = 0.0

        self.baseDamping = 0.0

        self.baseMinLeft = 0.0
        self.baseMaxLeft = 0.0

        self.baseLeftFriction = 0.0

        self.baseMinUp = 0.0
        self.baseMaxUp = 0.0

        self.baseUpFriction = 0.0
        self.baseMinForward = 0.0
        self.baseMaxForward = 0.0
        self.baseForwardFriction = 0.0

    def read(self,reader:ByteIO):
        self.flags = reader.read_int32()
        self.length = reader.read_float()
        self.tipMass = reader.read_float()
        self.yawStiffness = reader.read_float()
        self.yawDamping = reader.read_float()
        self.pitchStiffness = reader.read_float()
        self.pitchDamping = reader.read_float()
        self.alongStiffness = reader.read_float()
        self.alongDamping = reader.read_float()
        self.angleLimit = reader.read_float()
        self.minYaw = reader.read_float()
        self.maxYaw = reader.read_float()
        self.yawFriction = reader.read_float()
        self.yawBounce = reader.read_float()
        self.minPitch = reader.read_float()
        self.maxPitch = reader.read_float()
        self.pitchFriction = reader.read_float()
        self.pitchBounce = reader.read_float()
        self.baseMass = reader.read_float()
        self.baseMinLeft = reader.read_float()
        self.baseMaxLeft = reader.read_float()
        self.baseLeftFriction = reader.read_float()
        self.baseMinUp = reader.read_float()
        self.baseMaxUp = reader.read_float()
        self.baseUpFriction = reader.read_float()
        self.baseMinForward = reader.read_float()
        self.baseMaxForward = reader.read_float()
        self.baseForwardFriction = reader.read_float()


    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)


class SourceMdlAxisInterpBone:
    def __init__(self):
        self.control = 0
        self.axis = 0
        self.pos = []
        self.quat = []

    def read(self, reader: ByteIO):
        self.control = reader.read_uint32()
        self.pos = [SourceVector().read(reader) for _ in range(6)]
        self.quat = [SourceQuaternion().read(reader) for _ in range(6)]
        return  self

    def __str__(self):
        return "<AxisInterpBone control:{}>".format(self.control)

    def __repr__(self):
        return "<AxisInterpBone control:{}>".format(self.control)


class SourceMdlQuatInterpBone:
    def __init__(self):
        self.controlBoneIndex = 0
        self.triggerCount = 0
        self.triggerOffset = 0
        self.theTriggers = []

    def read(self, reader: ByteIO):
        self.controlBoneIndex = reader.read_uint32()
        self.triggerCount = reader.read_uint32()
        self.triggerOffset = reader.read_uint32()
        if self.triggerCount > 0 and self.triggerOffset != 0:
            self.theTriggers = [SourceMdlQuatInterpBoneInfo() for _ in range(self.triggerCount)]
            [t.read(reader) for t in self.theTriggers]

    def __str__(self):
        return "<QuatInterpBone control bone index:{}>".format(self.controlBoneIndex)

    def __repr__(self):
        return "<QuatInterpBone control index:{}>".format(self.controlBoneIndex)


class SourceMdlQuatInterpBoneInfo:
    def __init__(self):
        self.inverseToleranceAngle = 0
        self.trigger = SourceQuaternion()
        self.pos = SourceVector()
        self.quat = SourceQuaternion()

    def read(self, reader: ByteIO):
        self.inverseToleranceAngle = reader.read_float()
        self.trigger.read(reader)
        self.pos.read(reader)
        self.quat.read(reader)


class SourceMdlBoneController:
    def __init__(self):
        self.boneIndex = 0
        self.type = 0
        self.startBlah = 0
        self.endBlah = 0
        self.restIndex = 0
        self.inputField = 0
        self.unused = []

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.boneIndex = reader.read_uint32()
        self.type = reader.read_uint32()
        self.startBlah = reader.read_uint32()
        self.endBlah = reader.read_uint32()
        self.restIndex = reader.read_uint32()
        self.inputField = reader.read_uint32()
        if mdl.version > 10:
            self.unused = [reader.read_uint32() for _ in range(8)]
        mdl.theBoneControllers.append(self)

    def __str__(self):
        return "<BoneController bone index:{}>".format(self.boneIndex)

    def __repr__(self):
        return "<BoneController bone index:{}>".format(self.boneIndex)


class SourceMdlFlexDesc:
    def __init__(self):
        self.nameOffset = 0
        self.theName = ''
        self.theDescIsUsedByFlex = False
        self.theDescIsUsedByFlexRule = False
        self.theDescIsUsedByEyelid = False

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.nameOffset = reader.read_uint32()
        if self.nameOffset != 0:
            self.theName = reader.read_from_offset(entry+self.nameOffset,reader.read_ascii_string)
        pass

    def __str__(self):
        return "<FlexDesc name:{}>".format(self.theName)

    def __repr__(self):
        return "<FlexDesc name:{}>".format(self.theName)


class SourceMdlFlexController:
    def __init__(self):
        self.typeOffset = 0
        self.nameOffset = 0
        self.localToGlobal = 0
        self.min = 0.0
        self.max = 0.0
        self.theName = ''
        self.theType = ''

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        entry = reader.tell()
        self.typeOffset = reader.read_uint32()
        self.nameOffset = reader.read_uint32()
        self.localToGlobal = reader.read_uint32()
        self.min = reader.read_float()
        self.max = reader.read_float()
        if self.typeOffset != 0:
            self.theType = reader.read_from_offset(entry+self.typeOffset,reader.read_ascii_string)
        else:
            self.theType = ''
        if self.nameOffset != 0:
            self.theName = reader.read_from_offset(entry+self.nameOffset,reader.read_ascii_string)
        else:
            self.theName = 'blank_name_' + str(len(mdl.theFlexDescs))

        if mdl.theFlexControllers.__len__() > 0:
            mdl.theModelCommandIsUsed = True
        mdl.theFlexControllers.append(self)

    def __str__(self):
        return "<FlexController name:{} type:{}>".format(self.theName, self.theType)

    def __repr__(self):
        return "<FlexController name:{} type:{}>".format(self.theName, self.theType)


class SourceMdlFlexRule:
    def __init__(self):
        self.flexIndex = 0
        self.opCount = 0
        self.opOffset = 0
        self.theFlexOps = []

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        entry = reader.tell()
        self.flexIndex = reader.read_uint32()
        self.opCount = reader.read_uint32()
        self.opOffset = reader.read_uint32()
        opEntry = reader.tell()
        if self.opCount > 0 and self.opOffset != 0:
            for _ in range(self.opCount):
                reader.seek(entry + self.opOffset)
                flexOP = SourceMdlFlexOp()
                flexOP.read(reader, mdl)
                self.theFlexOps.append(flexOP)
        mdl.theFlexDescs[self.flexIndex].theDescIsUsedByFlexRule = True
        mdl.theFlexRules.append(self)
        reader.seek(opEntry, 0)

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)


class SourceMdlFlexOp:
    STUDIO_CONST = 1
    STUDIO_FETCH1 = 2
    STUDIO_FETCH2 = 3
    STUDIO_ADD = 4
    STUDIO_SUB = 5
    STUDIO_MUL = 6
    STUDIO_DIV = 7
    STUDIO_NEG = 8
    STUDIO_EXP = 9
    STUDIO_OPEN = 10
    STUDIO_CLOSE = 11
    STUDIO_COMMA = 12
    STUDIO_MAX = 13
    STUDIO_MIN = 14
    STUDIO_2WAY_0 = 15
    STUDIO_2WAY_1 = 16
    STUDIO_NWAY = 17
    STUDIO_COMBO = 18
    STUDIO_DOMINATE = 19
    STUDIO_DME_LOWER_EYELID = 20
    STUDIO_DME_UPPER_EYELID = 21

    def __init__(self):
        self.op = 0
        self.index = 0
        self.value = 0

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        self.op = reader.read_uint32()
        if self.op == SourceMdlFlexOp.STUDIO_CONST:
            self.value = reader.read_float()
        else:
            self.index = reader.read_uint32()
            if self.op == SourceMdlFlexOp.STUDIO_FETCH2:
                mdl.theFlexDescs[self.index].theDescIsUsedByFlexRule = True

    def __str__(self):
        return "<FlexOp op:{}>".format(self.op)

    def __repr__(self):
        return "<FlexOp op:{}>".format(self.op)


class SourceMdlAttachment:
    def __init__(self):
        self.name = ""
        self.type = 0
        self.bone = 0
        self.attachmentPoint = SourceVector
        self.vectors = []
        self.nameOffset = 0
        self.flags = 0
        self.localBoneIndex = 0
        self.localM11 = 0.0
        self.localM12 = 0.0
        self.localM13 = 0.0
        self.localM14 = 0.0
        self.localM21 = 0.0
        self.localM22 = 0.0
        self.localM23 = 0.0
        self.localM24 = 0.0
        self.localM31 = 0.0
        self.localM32 = 0.0
        self.localM33 = 0.0
        self.localM34 = 0.0
        self.unused = []

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        entry = reader.tell()
        if mdl.version == 10:
            self.name = reader.read_ascii_string(64)
        else:
            self.nameOffset = reader.read_uint32()
            self.name = reader.read_from_offset(self.nameOffset+entry,reader.read_ascii_string)
            self.flags = reader.read_uint32()
            self.localBoneIndex = reader.read_uint32()
            self.localM11 = reader.read_float()
            self.localM12 = reader.read_float()
            self.localM13 = reader.read_float()
            self.localM14 = reader.read_float()
            self.localM21 = reader.read_float()
            self.localM22 = reader.read_float()
            self.localM23 = reader.read_float()
            self.localM24 = reader.read_float()
            self.localM31 = reader.read_float()
            self.localM32 = reader.read_float()
            self.localM33 = reader.read_float()
            self.localM34 = reader.read_float()
            self.unused = [reader.read_uint32() for _ in range(8)]
        mdl.theAttachments.append(self)

    def __str__(self):
        return "<Attachment name:{} parent bone: {}>".format(self.name, self.localBoneIndex)

    def __repr__(self):
        return "<Attachment name:{} parent bone: {}>".format(self.name, self.localBoneIndex)


class SourceMdlBodyPart:
    def __init__(self):
        self.nameOffset = 0
        self.modelCount = 0
        self.base = 0
        self.modelOffset = 0
        self.theName = ""
        self.theModels = []

    def read(self, reader: ByteIO, mdl: SourceMdlFileData):
        entry = reader.tell()
        self.nameOffset = reader.read_uint32()
        self.theName = reader.read_from_offset(entry+self.nameOffset,reader.read_ascii_string) if self.nameOffset != 0 else "no-name{}".format(
            len(mdl.theBodyParts))
        self.modelCount = reader.read_uint32()
        self.base = reader.read_uint32()
        self.modelOffset = reader.read_uint32()
        entry2 = reader.tell()
        if self.modelCount > 0:
            reader.seek(entry + self.modelOffset)
            for _ in range(self.modelCount):
                SourceMdlModel().read(reader, self)
        reader.seek(entry2)
        mdl.theBodyParts.append(self)


    def __repr__(self):
        return "<BodyPart name:{} model count:{} models:{}>".format(self.theName, self.modelCount, self.theModels)


class SourceMdlModel:
    def __init__(self):
        self.name = ''
        self.type = 0
        self.boundingRadius = 0.0
        self.meshCount = 0
        self.meshOffset = 0
        self.vertexCount = 0
        self.vertexOffset = 0
        self.tangentOffset = 0
        self.attachmentCount = 0
        self.attachmentOffset = 0
        self.eyeballCount = 0
        self.eyeballOffset = 0
        self.vertexData = SourceMdlModelVertexData()
        self.unused = []
        self.theMeshes = []
        self.theEyeballs = []

    def read(self, reader: ByteIO, body_part: SourceMdlBodyPart):
        entry = reader.tell()
        self.name = reader.read_ascii_string(64)
        if not self.name:
            self.name = "no-name-{}".format(len(body_part.theModels))
        self.type = reader.read_uint32()
        self.boundingRadius = reader.read_float()
        self.meshCount = reader.read_uint32()
        self.meshOffset = reader.read_uint32()
        self.vertexCount = reader.read_uint32()
        self.vertexOffset = reader.read_uint32()
        self.tangentOffset = reader.read_uint32()
        self.attachmentCount = reader.read_uint32()
        self.attachmentOffset = reader.read_uint32()
        self.eyeballCount = reader.read_uint32()
        self.eyeballOffset = reader.read_uint32()
        self.vertexData.read(reader)
        self.unused = [reader.read_uint32() for _ in range(8)]
        entry2 = reader.tell()
        reader.seek(entry + self.eyeballOffset, 0)
        for _ in range(self.eyeballCount):
            SourceMdlEyeball().read(reader, self)
        reader.seek(entry + self.meshOffset, 0)
        for _ in range(self.meshCount):
            SourceMdlMesh().read(reader, self)

        reader.seek(entry2, 0)
        body_part.theModels.append(self)


        def __repr__(self):
            return "<Model name:{} type:{} mesh count:{} meshes:{} eyeballs:{}>".format(self.name, self.type,
                                                                                    self.meshCount,
                                                                                    self.theMeshes, self.theEyeballs)


class SourceMdlModelVertexData:
    def __init__(self):
        self.vertexDataP = 0
        self.tangentDataP = 0

    def read(self, reader: ByteIO):
        self.vertexDataP = reader.read_uint32()
        self.tangentDataP = reader.read_uint32()

    def __str__(self):
        return "<ModelVertexData vertex pointer:{} tangent pointer:{}>".format(self.vertexDataP, self.tangentDataP)

    def __repr__(self):
        return "<ModelVertexData vertex pointer:{} tangent pointer:{}>".format(self.vertexDataP, self.tangentDataP)


class SourceMdlEyeball:
    def __init__(self):
        self.nameOffset = 0
        self.boneIndex = 0
        self.org = SourceVector()
        self.zOffset = 0.0
        self.radius = 0.0
        self.up = SourceVector()
        self.forward = SourceVector()
        self.texture = 0

        self.unused1 = 0
        self.irisScale = 0.0
        self.unused2 = 0
        self.upperFlexDesc = []
        self.lowerFlexDesc = []
        self.upperTarget = []
        self.lowerTarget = []

        self.upperLidFlexDesc = 0
        self.lowerLidFlexDesc = 0
        self.unused = []
        self.eyeballIsNonFacs = b'\x00'
        self.unused3 = ''
        self.unused4 = []

        self.theName = ''
        self.theTextureIndex = 0

    def read(self, reader: ByteIO, model: SourceMdlModel):
        entry = reader.tell()
        self.nameOffset = reader.read_uint32()
        self.theName = reader.read_from_offset(entry+self.nameOffset,reader.read_ascii_string)
        self.boneIndex = reader.read_uint32()
        self.org.read(reader)
        self.zOffset = reader.read_float()
        self.radius = reader.read_float()
        self.up.read(reader)
        self.forward.read(reader)
        self.unused1 = reader.read_uint32()
        self.irisScale = reader.read_float()
        self.unused2 = reader.read_uint32()
        self.upperFlexDesc = [reader.read_uint32() for _ in range(3)]
        self.lowerFlexDesc = [reader.read_uint32() for _ in range(3)]
        self.upperTarget = [reader.read_float() for _ in range(3)]
        self.lowerTarget = [reader.read_float() for _ in range(3)]
        self.upperLidFlexDesc = reader.read_uint32()
        self.lowerLidFlexDesc = reader.read_uint32()
        self.unused = [reader.read_float() for _ in range(4)]
        self.eyeballIsNonFacs = reader.read_uint8()
        self.unused3 = reader.read_ascii_string(3)
        self.unused4 = [reader.read_uint32() for _ in range(7)]
        model.theEyeballs.append(self)

    def __str__(self):
        return "<Eyeball name:{} bone:{} xyz:{}>".format(self.theName, self.boneIndex, self.org.as_string)

    def __repr__(self):
        return "<Eyeball name:{} bone:{} xyz:{}>".format(self.theName, self.boneIndex, self.org.as_string)


class SourceMdlMesh:
    def __init__(self):
        self.materialIndex = 0
        self.modelOffset = 0
        self.vertexCount = 0
        self.vertexIndexStart = 0
        self.flexCount = 0
        self.flexOffset = 0
        self.materialType = 0
        self.materialParam = 0
        self.id = 0
        self.centerX = 0.0
        self.centerY = 0.0
        self.centerZ = 0.0
        self.vertexData = SourceMdlMeshVertexData()
        self.unused = []  # 8
        self.theFlexes = []

    def read(self, reader: ByteIO, model: SourceMdlModel):
        entry = reader.tell()
        self.materialIndex = reader.read_uint32()
        self.modelOffset = reader.read_uint32()
        self.vertexCount = reader.read_uint32()
        self.vertexIndexStart = reader.read_uint32()
        self.flexCount = reader.read_uint32()
        self.flexOffset = reader.read_uint32()
        self.materialType = reader.read_uint32()
        self.materialParam = reader.read_uint32()
        self.id = reader.read_uint32()
        self.centerX = reader.read_float()
        self.centerY = reader.read_float()
        self.centerZ = reader.read_float()
        self.vertexData.read(reader)
        self.unused = [reader.read_uint32() for _ in range(8)]
        if self.materialType == 1:
            model.theEyeballs[self.materialParam].theTextureIndex = self.materialIndex
        entry2 = reader.tell()
        if self.flexCount > 0 and self.flexOffset != 0:
            reader.seek(entry + self.flexOffset, 0)
            for _ in range(self.flexCount):
                SourceMdlFlex().read(reader,self)
        reader.seek(entry2, 0)
        model.theMeshes.append(self)


    def __repr__(self):
        return "<Mesh material inxes:{} vertex count:{} flex count:{} flexes:{}>".format(self.materialIndex,
                                                                                         self.vertexCount,
                                                                                         self.flexCount, self.theFlexes)


class SourceMdlMeshVertexData:
    def __init__(self):
        self.modelVertexDataP = 0
        self.lodVertexCount = []

    def read(self, reader: ByteIO):
        self.modelVertexDataP = reader.read_uint32()
        self.lodVertexCount = [reader.read_uint32() for _ in range(8)]

    def __str__(self):
        return "<MeshVertexData vertex pointer:{}, LODs vertex count:{}>".format(self.modelVertexDataP,
                                                                                 self.lodVertexCount)

    def __repr__(self):
        return "<MeshVertexData vertex pointer:{}, LODs vertex count:{}>".format(self.modelVertexDataP,
                                                                                 self.lodVertexCount)
class SourceMdlFlex:
    def __init__(self):
        self.flexDescIndex = 0
        self.target0 = 0.0
        self.target1 = 0.0
        self.target2 = 0.0
        self.target3 = 0.0
        self.vertCount = 0
        self.vertOffset = 0
        self.flexDescPartnerIndex = 0
        self.vertAnimType = b'\x00'
        self.unusedChar = []  # 3
        self.unused = []  # 6
        self.theVertAnims = []
        self.STUDIO_VERT_ANIM_NORMAL = 0
        self.STUDIO_VERT_ANIM_WRINKLE = 1

    def read(self,reader:ByteIO,mesh:SourceMdlMesh):
        entry = reader.tell()
        self.flexDescIndex = reader.read_uint32()
        self.target0 = reader.read_float()
        self.target1 = reader.read_float()
        self.target2 = reader.read_float()
        self.target3 = reader.read_float()

        self.vertCount = reader.read_uint32()
        self.vertOffset = reader.read_uint32()

        self.flexDescPartnerIndex = reader.read_uint32()
        self.vertAnimType = reader.read_uint8()

        self.unusedChar = [reader.read_uint8() for _ in range(3)]
        self.unused = [reader.read_uint32() for _ in range(6)]
        entry2 = reader.tell()

        if self.vertCount>0 and self.vertOffset !=0:
            with reader.save_current_pos():
                reader.seek(entry+self.vertOffset)
                for _ in range(self.vertCount):
                    if self.vertAnimType == self.STUDIO_VERT_ANIM_WRINKLE:
                        self.theVertAnims.append(SourceMdlVertAnimWrinkle().read(reader,self))
                    else:
                        self.theVertAnims.append(SourceMdlVertAnim().read(reader,self))
        mesh.theFlexes.append(self)

    def __repr__(self):
        return "<Flex Desc index:{} anim type:{}, vertex count:{} vertex offset:{}>".format(self.flexDescIndex, self.vertAnimType,self.vertCount,self.vertOffset)

class SourceMdlVertAnim:
    VertAnimFixedPointScale = 1/4096

    def __init__(self):
        self.index = 0
        self.speed = 0
        self.side = 0
        self.theDelta = []  # 3
        self.theNDelta = []  # 3

    def read(self,reader:ByteIO,flex:SourceMdlFlex):
        self.index = reader.read_uint16()
        self.speed = reader.read_uint8()
        self.side = reader.read_uint8()
        self.theDelta = [SourceFloat16bits().read(reader).TheFloatValue for _ in range(3)]
        self.theNDelta = [SourceFloat16bits().read(reader).TheFloatValue for _ in range(3)]
        return self



    def __repr__(self):
        return "<VertAnim index:{} speed:{} side:{} delta:{}>".format(self.index, self.speed, self.side,self.theDelta)

class SourceMdlVertAnimWrinkle(SourceMdlVertAnim):
    def __init__(self):
        super().__init__()
        self.wrinkleDelta = 0

    def read(self,reader:ByteIO,flex:SourceMdlFlex):
        super().read(reader,flex)
        self.wrinkleDelta = reader.read_uint16()
        return self

class SourceMdlTexture:
    def __init__(self):
        self.nameOffset = 0
        self.flags = 0
        self.used = 0
        self.unused1 = 0
        self.materialP = 0
        self.clientMaterialP = 0
        self.unused = []  # len 10
        self.thePathFileName = 'texture' + pformat(random.randint(0, 256))

    def read(self,reader:ByteIO,mdl:SourceMdlFileData):
        entry = reader.tell()
        self.nameOffset = reader.read_uint32()
        self.flags = reader.read_uint32()
        self.used = reader.read_uint32()
        self.unused1 = reader.read_uint32()
        self.materialP = reader.read_uint32()
        self.clientMaterialP = reader.read_uint32()
        self.unused = [reader.read_uint32() for _ in range(10 if mdl.version<53 else 5)]
        entry2 = reader.tell()
        if self.nameOffset!=0:
            self.thePathFileName = reader.read_from_offset(entry+self.nameOffset,reader.read_ascii_string)
        reader.seek(entry2)
        mdl.theTextures.append(self)

    def __str__(self):
        return "<Texture name:{}>".format(self.thePathFileName)

    def __repr__(self):
        return "<Texture name:{}>".format(self.thePathFileName)


class SourceMdlAnimBlock:
    """FROM: SourceEngineXXXX_source\public\studio.h
    // used for piecewise loading of animation data
    struct mstudioanimblock_t
    {
       DECLARE_BYTESWAP_DATADESC();
       int					datastart;
       int					dataend;
    };"""

    def __init__(self):
        self.dataStart = 0
        self.dataEnd = 0

    def read(self, reader: ByteIO):
        self.dataStart = reader.read_uint32()
        self.dataEnd = reader.read_uint32()

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
