import random
from pprint import pformat

import sys

from ByteReader import ByteReader
from rewrite.GLOBALS import SourceVector, SourceQuaternion, SourceFloat16bits


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
        self.eyePositionX = 0.1
        self.eyePositionY = 0.1
        self.eyePositionZ = 0.1
        self.illuminationPositionX = 0
        self.illuminationPositionY = 0
        self.illuminationPositionZ = 0
        self.hullMinPositionX = 0
        self.hullMinPositionY = 0
        self.hullMinPositionZ = 0
        self.hullMaxPositionX = 0
        self.hullMaxPositionY = 0
        self.hullMaxPositionZ = 0
        self.viewBoundingBoxMinPositionX = 0
        self.viewBoundingBoxMinPositionY = 0
        self.viewBoundingBoxMinPositionZ = 0
        self.viewBoundingBoxMaxPositionX = 0
        self.viewBoundingBoxMaxPositionY = 0
        self.viewBoundingBoxMaxPositionZ = 0
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
        self.nameOffset = 0

    def read(self, reader: ByteReader):
        self.readHeader00(reader)
        self.readHeader01(reader)
        self.ReadHeader02(reader)

    def readHeader00(self, reader: ByteReader):
        self.id = ''.join(list([chr(reader.readUByte()) for _ in range(4)]))
        self.version = reader.readInt32()
        self.checksum = reader.readInt32()
        self.name = reader.clean_string(reader.readASCII(64))
        self.fileSize = reader.readInt32()

    def readHeader01(self, reader: ByteReader):
        self.eyePositionX = reader.readFloat()
        self.eyePositionY = reader.readFloat()
        self.eyePositionZ = reader.readFloat()

        self.illuminationPositionX = reader.readFloat()
        self.illuminationPositionY = reader.readFloat()
        self.illuminationPositionZ = reader.readFloat()

        self.hullMinPositionX = reader.readFloat()
        self.hullMinPositionY = reader.readFloat()
        self.hullMinPositionZ = reader.readFloat()

        self.hullMaxPositionX = reader.readFloat()
        self.hullMaxPositionY = reader.readFloat()
        self.hullMaxPositionZ = reader.readFloat()

        self.viewBoundingBoxMinPositionX = reader.readFloat()
        self.viewBoundingBoxMinPositionY = reader.readFloat()
        self.viewBoundingBoxMinPositionZ = reader.readFloat()

        self.viewBoundingBoxMaxPositionX = reader.readFloat()
        self.viewBoundingBoxMaxPositionY = reader.readFloat()
        self.viewBoundingBoxMaxPositionZ = reader.readFloat()

        self.flags = reader.readInt32()

        self.boneCount = reader.readInt32()
        self.boneOffset = reader.readInt32()

        self.boneControllerCount = reader.readInt32()
        self.boneControllerOffset = reader.readInt32()

        self.hitboxSetCount = reader.readInt32()
        self.hitboxSetOffset = reader.readInt32()

        self.localAnimationCount = reader.readInt32()
        self.localAnimationOffset = reader.readInt32()

        self.localSequenceCount = reader.readInt32()
        self.localSequenceOffset = reader.readInt32()

        self.activityListVersion = reader.readInt32()
        self.eventsIndexed = reader.readInt32()

        self.textureCount = reader.readInt32()
        self.textureOffset = reader.readInt32()
        self.texturePathCount = reader.readInt32()
        self.texturePathOffset = reader.readInt32()

        self.skinReferenceCount = reader.readInt32()
        self.skinFamilyCount = reader.readInt32()
        self.skinFamilyOffset = reader.readInt32()

        self.bodyPartCount = reader.readInt32()
        self.bodyPartOffset = reader.readInt32()

        self.localAttachmentCount = reader.readInt32()
        self.localAttachmentOffset = reader.readInt32()

        self.localNodeCount = reader.readInt32()
        self.localNodeOffset = reader.readInt32()
        self.localNodeNameOffset = reader.readInt32()

        self.flexDescCount = reader.readInt32()
        self.flexDescOffset = reader.readInt32()

        self.flexControllerCount = reader.readInt32()
        self.flexControllerOffset = reader.readInt32()

        self.flexRuleCount = reader.readInt32()
        self.flexRuleOffset = reader.readInt32()

        self.ikChainCount = reader.readInt32()
        self.ikChainOffset = reader.readInt32()

        self.mouthCount = reader.readInt32()
        self.mouthOffset = reader.readInt32()

        self.localPoseParamaterCount = reader.readInt32()
        self.localPoseParameterOffset = reader.readInt32()

        self.surfacePropOffset = reader.readInt32()

        if self.surfacePropOffset > 0:
            self.theSurfacePropName = reader.get_name_from_offset(0, self.surfacePropOffset)

        self.keyValueOffset = reader.readInt32()
        self.keyValueSize = reader.readInt32()

        self.localIkAutoPlayLockOffset = reader.readInt32()
        self.localIkAutoPlayLockCount = reader.readInt32()

        self.mass = reader.readFloat()
        self.contents = reader.readInt32()

        self.includeModelCount = reader.readInt32()
        self.includeModelOffset = reader.readInt32()

        self.virtualModelP = reader.readInt32()

        self.animBlockNameOffset = reader.readInt32()
        self.animBlockCount = reader.readInt32()
        self.animBlockOffset = reader.readInt32()
        self.animBlockModelP = reader.readInt32()

        if self.animBlockCount > 0:
            if self.animBlockNameOffset > 0:
                self.theAnimBlockRelativePathFileName = reader.get_name_from_offset(reader.tell(),
                                                                                    self.animBlockNameOffset)

        if self.animBlockOffset > 0:
            backpos = reader.tell()
            reader.seek(self.animBlockOffset, 0)
            for offset in range(self.animBlockCount):
                anAnimBlock = SourceMdlAnimBlock()
                anAnimBlock.read(reader)
                self.theAnimBlocks.append(anAnimBlock)
            reader.seek(backpos, 0)

        self.boneTableByNameOffset = reader.readInt32()

        self.vertexBaseP = reader.readInt32()
        self.indexBaseP = reader.readInt32()

        self.directionalLightDot = reader.readUByte()

        self.rootLod = reader.readUByte()

        self.allowedRootLodCount = reader.readUByte()

        self.unused = reader.readUByte()

        self.unused4 = reader.readInt32()

        self.flexControllerUiCount = reader.readInt32()
        self.flexControllerUiOffset = reader.readInt32()

        self.vertAnimFixedPointScale = reader.readFloat()
        self.surfacePropOffset = reader.readInt32()

        self.studioHeader2Offset = reader.readInt32()

        self.unused2 = reader.readInt32()

        if self.bodyPartCount == 0 and self.localSequenceCount > 0:
            self.theMdlFileOnlyHasAnimations = True

    def ReadHeader02(self, reader: ByteReader):

        self.sourceBoneTransformCount = reader.readInt32()
        self.sourceBoneTransformOffset = reader.readInt32()
        self.illumPositionAttachmentIndex = reader.readInt32()
        self.maxEyeDeflection = reader.readFloat()
        self.linearBoneOffset = reader.readInt32()

        self.nameOffset = reader.readInt32()
        self.boneFlexDriverCount = reader.readInt32()
        self.boneTableByNameOffset = reader.readInt32()
        self.reserved = list([reader.readInt32() for _ in range(56)])

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)


class SourceMdlBone:
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

    def read(self, reader: ByteReader, mdl: SourceMdlFileData):
        self.boneOffset = reader.tell()
        if mdl.version == 10:
            self.name = reader.readASCII(32)
            pass
        else:
            self.nameOffset = reader.readInt32()
            self.parentBoneIndex = reader.readInt32()
            self.boneControllerIndex = [reader.readInt32() for _ in range(6)]
            self.position.read(reader)
            self.quat.read(reader)
            self.rotation.read(reader)
            self.positionScale.read(reader)
            self.rotationScale.read(reader)

            x0, x1, x2, x3 = reader.readFloat(), reader.readFloat(), reader.readFloat(), reader.readFloat()
            y0, y1, y2, y3 = reader.readFloat(), reader.readFloat(), reader.readFloat(), reader.readFloat()
            z0, z1, z2, z3 = reader.readFloat(), reader.readFloat(), reader.readFloat(), reader.readFloat()
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

            self.flags = reader.readInt32()
            self.qAlignment.read(reader)
            self.proceduralRuleType = reader.readInt32()
            self.proceduralRuleOffset = reader.readInt32()
            self.physicsBoneIndex = reader.readInt32()
            self.surfacePropNameOffset = reader.readInt32()
            self.contents = reader.readInt32()
            self.unused = [reader.readInt32() for _ in range(8)]
        inputFileStreamPosition = reader.tell()
        if self.nameOffset != 0:
            self.name = reader.get_name_from_offset(self.boneOffset, self.nameOffset)
        if self.proceduralRuleType != 0:
            if self.proceduralRuleType == self.STUDIO_PROC_AXISINTERP:
                reader.seek(self.boneOffset + self.proceduralRuleOffset)
                self.theAxisInterpBone = SourceMdlAxisInterpBone()
                self.theAxisInterpBone.read(reader)
            if self.proceduralRuleType == self.STUDIO_PROC_QUATINTERP:
                pass
                # self.ReadQuatInterpBone(self.boneOffset, reader)
            if self.proceduralRuleType == self.STUDIO_PROC_JIGGLE:
                pass
                # self.ReadJiggleBone(self.boneOffset, reader)
        if self.surfacePropNameOffset != 0:
            reader.seek(self.boneOffset, 0)
            self.theSurfacePropName = reader.get_name_from_offset(reader.tell(), self.surfacePropNameOffset)

        reader.seek(inputFileStreamPosition, 0)
        mdl.theBones.append(self)



    def __repr__(self):
        return "<Bone {} pos:{} rot: {}>".format(self.name, self.position.as_string, self.rotation.as_string)


class SourceMdlAxisInterpBone:
    def __init__(self):
        self.control = 0
        self.axis = 0
        self.pos = []
        self.quat = []

    def read(self, reader: ByteReader):
        self.control = reader.readInt32()
        self.pos = [SourceVector() for _ in range(6)]
        [v.read(reader) for v in self.pos]
        self.quat = [SourceQuaternion() for _ in range(6)]
        [q.read(reader) for q in self.quat]

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

    def read(self, reader: ByteReader):
        self.controlBoneIndex = reader.readInt32()
        self.triggerCount = reader.readInt32()
        self.triggerOffset = reader.readInt32()
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

    def read(self, reader: ByteReader):
        self.inverseToleranceAngle = reader.readFloat()
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

    def read(self, reader: ByteReader, mdl: SourceMdlFileData):
        self.boneIndex = reader.readInt32()
        self.type = reader.readInt32()
        self.startBlah = reader.readInt32()
        self.endBlah = reader.readInt32()
        self.restIndex = reader.readInt32()
        self.inputField = reader.readInt32()
        if mdl.version > 10:
            self.unused = [reader.readInt32() for _ in range(8)]
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

    def read(self, reader: ByteReader):
        entry = reader.tell()
        self.nameOffset = reader.readInt32()
        if self.nameOffset != 0:
            self.theName = reader.get_name_from_offset(entry, self.nameOffset)
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

    def read(self, reader: ByteReader, mdl: SourceMdlFileData):
        entry = reader.tell()
        self.typeOffset = reader.readInt32()
        self.nameOffset = reader.readInt32()
        self.localToGlobal = reader.readInt32()
        self.min = reader.readFloat()
        self.max = reader.readFloat()
        if self.typeOffset != 0:
            self.theType = reader.get_name_from_offset(entry, self.typeOffset)
        else:
            self.theType = ''
        if self.nameOffset != 0:
            self.theName = reader.get_name_from_offset(entry, self.nameOffset)
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

    def read(self, reader: ByteReader, mdl: SourceMdlFileData):
        entry = reader.tell()
        self.flexIndex = reader.readInt32()
        self.opCount = reader.readInt32()
        self.opOffset = reader.readInt32()
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

    def read(self, reader: ByteReader, mdl: SourceMdlFileData):
        self.op = reader.readInt32()
        if self.op == SourceMdlFlexOp.STUDIO_CONST:
            self.value = reader.readFloat()
        else:
            self.index = reader.readInt32()
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

    def read(self, reader: ByteReader, mdl: SourceMdlFileData):
        entry = reader.tell()
        if mdl.version == 10:
            self.name = reader.readASCII(64)
        else:
            self.nameOffset = reader.readInt32()
            self.name = reader.get_name_from_offset(self.nameOffset, entry)
            self.flags = reader.readInt32()
            self.localBoneIndex = reader.readInt32()
            self.localM11 = reader.readFloat()
            self.localM12 = reader.readFloat()
            self.localM13 = reader.readFloat()
            self.localM14 = reader.readFloat()
            self.localM21 = reader.readFloat()
            self.localM22 = reader.readFloat()
            self.localM23 = reader.readFloat()
            self.localM24 = reader.readFloat()
            self.localM31 = reader.readFloat()
            self.localM32 = reader.readFloat()
            self.localM33 = reader.readFloat()
            self.localM34 = reader.readFloat()
            self.unused = [reader.readInt32() for _ in range(8)]
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

    def read(self, reader: ByteReader, mdl: SourceMdlFileData):
        entry = reader.tell()
        self.nameOffset = reader.readInt32()
        self.theName = reader.get_name_from_offset(entry,
                                                   self.nameOffset) if self.nameOffset != 0 else "no-name{}".format(
            len(mdl.theBodyParts))
        self.modelCount = reader.readInt32()
        self.base = reader.readInt32()
        self.modelOffset = reader.readInt32()
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

    def read(self, reader: ByteReader, body_part: SourceMdlBodyPart):
        entry = reader.tell()
        self.name = reader.clean_string(reader.readASCII(64))
        if not self.name:
            self.name = "no-name-{}".format(len(body_part.theModels))
        self.type = reader.readInt32()
        self.boundingRadius = reader.readFloat()
        self.meshCount = reader.readInt32()
        self.meshOffset = reader.readInt32()
        self.vertexCount = reader.readInt32()
        self.vertexOffset = reader.readInt32()
        self.tangentOffset = reader.readInt32()
        self.attachmentCount = reader.readInt32()
        self.attachmentOffset = reader.readInt32()
        self.eyeballCount = reader.readInt32()
        self.eyeballOffset = reader.readInt32()
        self.vertexData.read(reader)
        self.unused = [reader.readInt32() for _ in range(8)]
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

    def read(self, reader: ByteReader):
        self.vertexDataP = reader.readInt32()
        self.tangentDataP = reader.readInt32()

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

    def read(self, reader: ByteReader, model: SourceMdlModel):
        entry = reader.tell()
        self.nameOffset = reader.readInt32()
        self.theName = reader.get_name_from_offset(entry, self.nameOffset)
        self.boneIndex = reader.readInt32()
        self.org.read(reader)
        self.zOffset = reader.readFloat()
        self.radius = reader.readFloat()
        self.up.read(reader)
        self.forward.read(reader)
        self.unused1 = reader.readInt32()
        self.irisScale = reader.readFloat()
        self.unused2 = reader.readInt32()
        self.upperFlexDesc = [reader.readInt32() for _ in range(3)]
        self.lowerFlexDesc = [reader.readInt32() for _ in range(3)]
        self.upperTarget = [reader.readFloat() for _ in range(3)]
        self.lowerTarget = [reader.readFloat() for _ in range(3)]
        self.upperLidFlexDesc = reader.readInt32()
        self.lowerLidFlexDesc = reader.readInt32()
        self.unused = [reader.readFloat() for _ in range(4)]
        self.eyeballIsNonFacs = reader.readUByte()
        self.unused3 = reader.readASCII(3)
        self.unused4 = [reader.readInt32() for _ in range(7)]
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

    def read(self, reader: ByteReader, model: SourceMdlModel):
        entry = reader.tell()
        self.materialIndex = reader.readInt32()
        self.modelOffset = reader.readInt32()
        self.vertexCount = reader.readInt32()
        self.vertexIndexStart = reader.readInt32()
        self.flexCount = reader.readInt32()
        self.flexOffset = reader.readInt32()
        self.materialType = reader.readInt32()
        self.materialParam = reader.readInt32()
        self.id = reader.readInt32()
        self.centerX = reader.readFloat()
        self.centerY = reader.readFloat()
        self.centerZ = reader.readFloat()
        self.vertexData.read(reader)
        self.unused = [reader.readInt32() for _ in range(8)]
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

    def read(self, reader: ByteReader):
        self.modelVertexDataP = reader.readInt32()
        self.lodVertexCount = [reader.readInt32() for _ in range(8)]

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

    def read(self,reader:ByteReader,mesh:SourceMdlMesh):
        entry = reader.tell()
        self.flexDescIndex = reader.readInt32()
        self.target0 = reader.readFloat()
        self.target1 = reader.readFloat()
        self.target2 = reader.readFloat()
        self.target3 = reader.readFloat()

        self.vertCount = reader.readInt32()
        self.vertOffset = reader.readInt32()

        self.flexDescPartnerIndex = reader.readInt32()
        self.vertAnimType = reader.readUByte()

        self.unusedChar = [reader.readUByte() for _ in range(3)]
        self.unused = [reader.readInt32() for _ in range(6)]
        entry2 = reader.tell()

        if self.vertCount>0 | self.vertOffset !=0:
            if self.vertAnimType == self.STUDIO_VERT_ANIM_WRINKLE:
                self.theVertAnims.append(SourceMdlVertAnimWrinkle().read(reader,self))
            else:
                self.theVertAnims.append(SourceMdlVertAnim().read(reader,self))
        reader.seek(entry2)
        mesh.theFlexes.append(self)

    def __str__(self):
        return "<Flex Desc index:{} anim type:{}>".format(self.flexDescIndex,self.vertAnimType)

    def __repr__(self):
        return "<Flex Desc index:{} anim type:{}>".format(self.flexDescIndex, self.vertAnimType)

class SourceMdlVertAnim:
    VertAnimFixedPointScale = 1/4096

    def __init__(self):
        self.index = 0
        self.speed = 0
        self.side = 0
        self.theDelta = []  # 3
        self.theNDelta = []  # 3

    def read(self,reader:ByteReader,flex:SourceMdlFlex):
        self.index = reader.readUInt16()
        self.speed = reader.readUByte()
        self.side = reader.readUByte()
        self.theDelta = [SourceFloat16bits().read(reader).TheFloatValue for _ in range(3)]
        self.theNDelta = [SourceFloat16bits().read(reader).TheFloatValue for _ in range(3)]
        return  self

    def __str__(self):
        return "<VertAnim index:{} speed:{} side:{}>".format(self.index,self.speed,self.side)

    def __repr__(self):
        return "<VertAnim index:{} speed:{} side:{}>".format(self.index, self.speed, self.side)

class SourceMdlVertAnimWrinkle(SourceMdlVertAnim):
    def __init__(self):
        super().__init__()
        self.wrinkleDelta = 0

    def read(self,reader:ByteReader,flex:SourceMdlFlex):
        super().read(reader,flex)
        self.wrinkleDelta = reader.readInt16()
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

    def read(self,reader:ByteReader,mdl:SourceMdlFileData):
        entry = reader.tell()
        self.nameOffset = reader.readInt32()
        self.flags = reader.readInt32()
        self.used = reader.readInt32()
        self.unused1 = reader.readInt32()
        self.materialP = reader.readInt32()
        self.clientMaterialP = reader.readInt32()
        self.unused = [reader.readInt32() for _ in range(10)]
        entry2 = reader.tell()
        if self.nameOffset!=0:
            self.thePathFileName = reader.get_name_from_offset(entry,self.nameOffset)
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

    def read(self, reader: ByteReader):
        self.dataStart = reader.readInt32()
        self.dataEnd = reader.readInt32()

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
