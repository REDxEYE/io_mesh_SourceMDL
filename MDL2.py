import math
from pprint import pprint

import sys

import MDL_DATA
DEBUG = False
try:
    from .MDL_DATA import *
except:
    from MDL_DATA import *

listTypes = {
    "unsigned int": {"type": "I", "len": 4},
    "float": {"type": "f", "len": 4},
    "unsigned char": {"type": "B", "len": 1},
    "unsigned short": {"type": "H", "len": 2},
    "char": {"type": "c", "len": 1},
    "byte": {"type": "B", "len": 1},
    "int": {"type": "i", "len": 4},
    "long": {"type": "l", "len": 4},
    "char*": {"type": "I", "len": 4},

}
Types = {
    "f": 4,
    "B": 1,
    "H": 2,
    "h": 2,
    "c": 1,
    "i": 4,
    "l": 4,
    "I": 4}


class SourceMdlFile49:
    @staticmethod
    def GetNameFromOffset(data, base, offset):
        orig = data.tell()

        data.seek(base + offset, 0)
        # print(base,offset)
        name = ""
        bb = ""
        while bb != b'\x00':
            bb = data.read(1)
            if bb == b'\x00':
                break
            name += chr(struct.unpack('B', bb)[0])
        data.seek(orig, 0)
        return name

    @staticmethod
    def get_name_from_list_bytes(byte_list: list):
        # print(byte_list)
        name = ''
        for b in byte_list:  # type: bytes
            if b:
                name += b.decode(errors='ignore')

        return name

    @staticmethod
    def GetName(data_):
        # print(data_)
        name = ""
        for C in data_:

            if C == b'\x00':
                break
            name += chr(int().from_bytes(C, 'little'))
        return name

    def __init__(self, filepath):
        if isinstance(filepath, str):
            fp = open(filepath, "rb")
        else :
            fp = filepath
        self.data = fp
        self.theMdlFileData = SourceMdlFileData()
        self.ReadMdlHeader00()
        self.ReadMdlHeader01()
        self.ReadMdlHeader02()
        self.ReadBones()
        self.ReadBoneControllers()

        self.ReadFlexDescs()
        self.ReadFlexControllers()
        self.ReadFlexRules()

        self.ReadAttachments()
        self.ReadHitboxSets()
        self.ReadBoneTableByName()
        self.ReadBodyParts()
        self.ReadTextures()
        self.ReadTexturePaths()
        self.CreateFlexFrameList()
        #self.ReadLocalAnimationDescs()
        fp.close()
    def readASCII(self, len_):
        return ''.join([self.readACSIIChar() for _ in range(len_)])

    def readByte(self):
        type_ = 'b'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readBytes(self, len_):
        type_ = 'b'
        return [struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0] for _ in range(len_)]

    def readUByte(self):
        type_ = 'B'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readInt32(self):
        type_ = 'i'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readUInt32(self):
        type_ = 'I'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readInt16(self):
        type_ = 'h'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readUInt16(self):
        type_ = 'H'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readFloat(self):
        type_ = 'f'
        return struct.unpack(type_, self.data.read(struct.calcsize(type_)))[0]

    def readACSIIChar(self):
        a = self.readUByte()
        return chr(a)

    def ReadBytes(self, t):
        data = self.data.read(Types[t])
        return struct.unpack(t, data)[0]

    def ReadInt32(self):
        return self.readInt32()

    def ReadShort(self):
        return self.readInt16()

    def ReadFloat(self):
        return self.readFloat()

    def ReadByte(self):
        return self.readUByte()

    def ReadMdlHeader00(self):
        start = self.data.tell()
        self.theMdlFileData.id = ''.join(list([chr(self.readUByte()) for a in range(4)]))
        self.theMdlFileData.version = self.readInt32()
        self.theMdlFileData.checksum = self.readInt32()
        self.theMdlFileData.name = ''.join(list([chr(self.readUByte()) for a in range(64)]))
        self.theMdlFileData.fileSize = self.readInt32()

        # self.theMdlFileData.theActualFileSize =

    def ReadMdlHeader01(self):
        start = self.data.tell()
        self.theMdlFileData.eyePositionX = self.readFloat()
        self.theMdlFileData.eyePositionY = self.readFloat()
        self.theMdlFileData.eyePositionZ = self.readFloat()

        self.theMdlFileData.illuminationPositionX = self.readFloat()
        self.theMdlFileData.illuminationPositionY = self.readFloat()
        self.theMdlFileData.illuminationPositionZ = self.readFloat()

        self.theMdlFileData.hullMinPositionX = self.readFloat()
        self.theMdlFileData.hullMinPositionY = self.readFloat()
        self.theMdlFileData.hullMinPositionZ = self.readFloat()

        self.theMdlFileData.hullMaxPositionX = self.readFloat()
        self.theMdlFileData.hullMaxPositionY = self.readFloat()
        self.theMdlFileData.hullMaxPositionZ = self.readFloat()

        self.theMdlFileData.viewBoundingBoxMinPositionX = self.readFloat()
        self.theMdlFileData.viewBoundingBoxMinPositionY = self.readFloat()
        self.theMdlFileData.viewBoundingBoxMinPositionZ = self.readFloat()

        self.theMdlFileData.viewBoundingBoxMaxPositionX = self.readFloat()
        self.theMdlFileData.viewBoundingBoxMaxPositionY = self.readFloat()
        self.theMdlFileData.viewBoundingBoxMaxPositionZ = self.readFloat()

        self.theMdlFileData.flags = self.readInt32()

        self.theMdlFileData.boneCount = self.readInt32()
        self.theMdlFileData.boneOffset = self.readInt32()

        self.theMdlFileData.boneControllerCount = self.readInt32()
        self.theMdlFileData.boneControllerOffset = self.readInt32()

        self.theMdlFileData.hitboxSetCount = self.readInt32()
        self.theMdlFileData.hitboxSetOffset = self.readInt32()

        self.theMdlFileData.localAnimationCount = self.readInt32()
        self.theMdlFileData.localAnimationOffset = self.readInt32()

        self.theMdlFileData.localSequenceCount = self.readInt32()
        self.theMdlFileData.localSequenceOffset = self.readInt32()

        self.theMdlFileData.activityListVersion = self.readInt32()
        self.theMdlFileData.eventsIndexed = self.readInt32()

        self.theMdlFileData.textureCount = self.readInt32()
        self.theMdlFileData.textureOffset = self.readInt32()

        self.theMdlFileData.texturePathCount = self.readInt32()
        self.theMdlFileData.texturePathOffset = self.readInt32()

        self.theMdlFileData.skinReferenceCount = self.readInt32()
        self.theMdlFileData.skinFamilyCount = self.readInt32()
        self.theMdlFileData.skinFamilyOffset = self.readInt32()

        self.theMdlFileData.bodyPartCount = self.readInt32()
        self.theMdlFileData.bodyPartOffset = self.readInt32()

        self.theMdlFileData.localAttachmentCount = self.readInt32()
        self.theMdlFileData.localAttachmentOffset = self.readInt32()

        self.theMdlFileData.localNodeCount = self.readInt32()
        self.theMdlFileData.localNodeOffset = self.readInt32()

        self.theMdlFileData.localNodeNameOffset = self.readInt32()

        self.theMdlFileData.flexDescCount = self.readInt32()
        self.theMdlFileData.flexDescOffset = self.readInt32()

        self.theMdlFileData.flexControllerCount = self.readInt32()
        self.theMdlFileData.flexControllerOffset = self.readInt32()

        self.theMdlFileData.flexRuleCount = self.readInt32()
        self.theMdlFileData.flexRuleOffset = self.readInt32()

        self.theMdlFileData.ikChainCount = self.readInt32()
        self.theMdlFileData.ikChainOffset = self.readInt32()

        self.theMdlFileData.mouthCount = self.readInt32()
        self.theMdlFileData.mouthOffset = self.readInt32()

        self.theMdlFileData.localPoseParamaterCount = self.readInt32()
        self.theMdlFileData.localPoseParameterOffset = self.readInt32()

        self.theMdlFileData.surfacePropOffset = self.readInt32()
        # TODO: Same as some lines below. Move to a separate function.
        if self.theMdlFileData.surfacePropOffset > 0:
            inputFileStreamPosition = self.data.tell()
            self.theMdlFileData.theSurfacePropName = self.GetNameFromOffset(self.data, 0,
                                                                            self.theMdlFileData.surfacePropOffset)
            self.data.seek(inputFileStreamPosition, 0)
        self.theMdlFileData.keyValueOffset = self.readInt32()
        self.theMdlFileData.keyValueSize = self.readInt32()

        self.theMdlFileData.localIkAutoPlayLockCount = self.readInt32()
        self.theMdlFileData.localIkAutoPlayLockOffset = self.readInt32()

        self.theMdlFileData.mass = self.readFloat()
        self.theMdlFileData.contents = self.readInt32()

        self.theMdlFileData.includeModelCount = self.readInt32()
        self.theMdlFileData.includeModelOffset = self.readInt32()

        self.theMdlFileData.virtualModelP = self.readInt32()

        self.theMdlFileData.animBlockNameOffset = self.readInt32()
        self.theMdlFileData.animBlockCount = self.readInt32()
        self.theMdlFileData.animBlockOffset = self.readInt32()
        self.theMdlFileData.animBlockModelP = self.readInt32()

        if self.theMdlFileData.animBlockCount > 0:
            if self.theMdlFileData.animBlockNameOffset > 0:
                self.theMdlFileData.theAnimBlockRelativePathFileName = self.GetNameFromOffset(self.data,
                                                                                              self.data.tell(),
                                                                                              self.theMdlFileData.animBlockNameOffset)

        if self.theMdlFileData.animBlockOffset > 0:
            inputFileStreamPosition = self.data.tell()
            self.data.seek(self.theMdlFileData.animBlockOffset, 0)

            for offset in range(self.theMdlFileData.animBlockCount):
                anAnimBlock = SourceMdlAnimBlock()
                anAnimBlock.dataStart = self.readInt32()
                anAnimBlock.dataEnd = self.readInt32()
                self.theMdlFileData.theAnimBlocks.append(anAnimBlock)
            self.data.seek(inputFileStreamPosition, 0)

        self.theMdlFileData.boneTableByNameOffset = self.readInt32()

        self.theMdlFileData.vertexBaseP = self.readInt32()
        self.theMdlFileData.indexBaseP = self.readInt32()

        self.theMdlFileData.directionalLightDot = self.readUByte()

        self.theMdlFileData.rootLod = self.readUByte()

        self.theMdlFileData.allowedRootLodCount = self.readUByte()

        self.theMdlFileData.unused = self.readUByte()

        self.theMdlFileData.unused4 = self.readInt32()

        self.theMdlFileData.flexControllerUiCount = self.readInt32()
        self.theMdlFileData.flexControllerUiOffset = self.readInt32()

        self.theMdlFileData.vertAnimFixedPointScale = self.readFloat()
        self.theMdlFileData.surfacePropLookup = self.readInt32()

        self.theMdlFileData.studioHeader2Offset = self.readInt32()

        self.theMdlFileData.unused2 = self.readInt32()

        if self.theMdlFileData.bodyPartCount == 0 and self.theMdlFileData.localSequenceCount > 0:
            self.theMdlFileData.theMdlFileOnlyHasAnimations = True

    def ReadMdlHeader02(self):
        start = self.data.tell()
        self.theMdlFileData.sourceBoneTransformCount = self.readInt32()
        self.theMdlFileData.sourceBoneTransformOffset = self.readInt32()
        self.theMdlFileData.illumPositionAttachmentIndex = self.readInt32()
        self.theMdlFileData.maxEyeDeflection = self.readFloat()
        self.theMdlFileData.linearBoneOffset = self.readInt32()

        self.theMdlFileData.name = self.readInt32()
        self.theMdlFileData.boneFlexDriverCount = self.readInt32()
        self.theMdlFileData.boneFlexDriverOffset = self.readInt32()
        self.theMdlFileData.reserved = []
        for i in range(56):
            self.theMdlFileData.reserved.append(self.readInt32())

    def ReadQuaternion(self, data: SourceQuaternion):
        data.x = self.readFloat()
        data.y = self.readFloat()
        data.z = self.readFloat()
        data.w = self.readFloat()

    def ReadBones(self):

        if self.theMdlFileData.boneCount > 0:
            self.data.seek(self.theMdlFileData.boneOffset, 0)

            for i in range(self.theMdlFileData.boneCount):
                start = self.data.tell()
                boneInputFileStreamPosition = self.data.tell()
                aBone = SourceMdlBone()
                aBone.boneOffset = self.data.tell()
                if self.theMdlFileData.version == 10:

                    aBone.name = list([self.data.read(1) for i in range(32)])
                    aBone.name = self.GetName(aBone.name)
                    # TODO:
                    # do this thing
                    pass
                else:
                    aBone.nameOffset = self.readInt32()
                    aBone.parentBoneIndex = self.readInt32()
                    aBone.boneControllerIndex = []
                    for j in range(6):
                        aBone.boneControllerIndex.append(self.readInt32())

                    aBone.position = SourceVector(self.data)

                    aBone.quat = SourceQuaternion(self.data)

                    aBone.rotation = SourceVector(self.data)

                    aBone.positionScale = SourceVector(self.data)

                    aBone.rotationScale = SourceVector(self.data)
                    x0, x1, x2, x3 = self.readFloat(), self.readFloat(), self.readFloat(), self.readFloat()
                    y0, y1, y2, y3 = self.readFloat(), self.readFloat(), self.readFloat(), self.readFloat()
                    z0, z1, z2, z3 = self.readFloat(), self.readFloat(), self.readFloat(), self.readFloat()
                    aBone.poseToBoneColumn0.x = x0
                    aBone.poseToBoneColumn0.y = y0
                    aBone.poseToBoneColumn0.z = z0
                    aBone.poseToBoneColumn1.x = x1
                    aBone.poseToBoneColumn1.y = y1
                    aBone.poseToBoneColumn1.z = z1
                    aBone.poseToBoneColumn2.x = x2
                    aBone.poseToBoneColumn2.y = y2
                    aBone.poseToBoneColumn2.z = z2
                    aBone.poseToBoneColumn3.x = x3
                    aBone.poseToBoneColumn3.y = y3
                    aBone.poseToBoneColumn3.z = z3

                    aBone.flags = self.readInt32()
                    aBone.qAlignment = SourceQuaternion(self.data)
                    aBone.proceduralRuleType = self.readInt32()
                    aBone.proceduralRuleOffset = self.readInt32()
                    aBone.physicsBoneIndex = self.readInt32()
                    aBone.surfacePropNameOffset = self.readInt32()
                    aBone.contents = self.readInt32()
                    aBone.unused = []
                    for i in range(8):
                        aBone.unused.append(self.readInt32())

                inputFileStreamPosition = self.data.tell()
                if aBone.nameOffset != 0:
                    aBone.name = self.GetNameFromOffset(self.data, boneInputFileStreamPosition, aBone.nameOffset)
                if aBone.proceduralRuleType != 0:
                    if aBone.proceduralRuleType == aBone.STUDIO_PROC_AXISINTERP:
                        self.ReadAxisInterpBone(boneInputFileStreamPosition, aBone)
                    if aBone.proceduralRuleType == aBone.STUDIO_PROC_QUATINTERP:
                        self.ReadQuatInterpBone(boneInputFileStreamPosition, aBone)
                    if aBone.proceduralRuleType == aBone.STUDIO_PROC_JIGGLE:
                        self.ReadJiggleBone(boneInputFileStreamPosition, aBone)
                if aBone.surfacePropNameOffset != 0:
                    self.data.seek(boneInputFileStreamPosition, 0)
                    aBone.theSurfacePropName = self.GetNameFromOffset(self.data, self.data.tell(),
                                                                      aBone.surfacePropNameOffset)
                    self.data.seek(inputFileStreamPosition, 0)
                self.theMdlFileData.theBones.append(aBone)

    def ReadAxisInterpBone(self, boneInputFileStreamPosition, aBone: SourceMdlBone):
        self.data.seek(boneInputFileStreamPosition + aBone.proceduralRuleOffset)
        axisInterpBoneInputFileStreamPosition = self.data.tell()
        aBone.theAxisInterpBone = SourceMdlAxisInterpBone()
        aBone.theAxisInterpBone.control = self.readInt32()
        aBone.theAxisInterpBone.pos = []
        for i in range(6):
            aBone.theAxisInterpBone.pos.append(SourceVector(self.data))
        aBone.theAxisInterpBone.quat = []
        for i in range(6):
            aBone.theAxisInterpBone.quat.append(SourceQuaternion(self.data))
        inputFileStreamPosition = self.data.tell()
        self.data.seek(inputFileStreamPosition, 0)

    def ReadQuatInterpBone(self, boneInputFileStreamPosition, aBone: SourceMdlBone):
        self.data.seek(boneInputFileStreamPosition + aBone.proceduralRuleOffset)
        quatInterpBoneInputFileStreamPosition = self.data.tell()
        aBone.theQuatInterpBone = SourceMdlQuatInterpBone()
        aBone.theQuatInterpBone.controlBoneIndex = self.readInt32()
        aBone.theQuatInterpBone.triggerCount = self.readInt32()
        aBone.theQuatInterpBone.triggerOffset = self.readInt32()
        inputFileStreamPosition = self.data.tell()
        if aBone.theQuatInterpBone.triggerCount > 0 and aBone.theQuatInterpBone.triggerOffset != 0:
            self.ReadTriggers(quatInterpBoneInputFileStreamPosition, aBone.theQuatInterpBone)
        self.data.seek(inputFileStreamPosition, 0)

    def ReadJiggleBone(self, boneInputFileStreamPosition, aBone: SourceMdlBone):

        self.data.seek(boneInputFileStreamPosition + aBone.proceduralRuleOffset)
        start = self.data.tell()

        aBone.theJiggleBone = SourceMdlJiggleBone()
        aBone.theJiggleBone.flag_offset = self.data.tell()
        aBone.theJiggleBone.flags = self.readInt32()
        aBone.theJiggleBone.length_offset = self.data.tell()
        aBone.theJiggleBone.length = self.readFloat()
        aBone.theJiggleBone.tipMass_offset = self.data.tell()
        aBone.theJiggleBone.tipMass = self.readFloat()
        aBone.theJiggleBone.yawStiffness_offset = self.data.tell()
        aBone.theJiggleBone.yawStiffness = self.readFloat()
        aBone.theJiggleBone.jawDamping_offset = self.data.tell()
        aBone.theJiggleBone.yawDamping = self.readFloat()
        aBone.theJiggleBone.pitchStiffness_offset = self.data.tell()
        aBone.theJiggleBone.pitchStiffness = self.readFloat()
        aBone.theJiggleBone.pitchDamping_offset = self.data.tell()
        aBone.theJiggleBone.pitchDamping = self.readFloat()
        aBone.theJiggleBone.alongStiffness_offset = self.data.tell()
        aBone.theJiggleBone.alongStiffness = self.readFloat()
        aBone.theJiggleBone.alongDamping_offset = self.data.tell()
        aBone.theJiggleBone.alongDamping = self.readFloat()
        aBone.theJiggleBone.angleLimit_offset = self.data.tell()
        aBone.theJiggleBone.angleLimit = self.readFloat()
        aBone.theJiggleBone.minYaw_offset = self.data.tell()
        aBone.theJiggleBone.minYaw = self.readFloat()
        aBone.theJiggleBone.maxYaw_offset = self.data.tell()
        aBone.theJiggleBone.maxYaw = self.readFloat()
        aBone.theJiggleBone.yawFriction_offset = self.data.tell()
        aBone.theJiggleBone.yawFriction = self.readFloat()
        aBone.theJiggleBone.yawBounce_offset = self.data.tell()
        aBone.theJiggleBone.yawBounce = self.readFloat()
        aBone.theJiggleBone.minPitch_offset = self.data.tell()
        aBone.theJiggleBone.minPitch = self.readFloat()
        aBone.theJiggleBone.maxPitch_offset = self.data.tell()
        aBone.theJiggleBone.maxPitch = self.readFloat()
        aBone.theJiggleBone.pitchFriction_offset = self.data.tell()
        aBone.theJiggleBone.pitchFriction = self.readFloat()
        aBone.theJiggleBone.pitchBounce_offset = self.data.tell()
        aBone.theJiggleBone.pitchBounce = self.readFloat()
        aBone.theJiggleBone.baseMass_offset = self.data.tell()
        aBone.theJiggleBone.baseMass = self.readFloat()
        aBone.theJiggleBone.baseStiffness_offset = self.data.tell()
        aBone.theJiggleBone.baseStiffness = self.readFloat()
        aBone.theJiggleBone.baseDamping_offset = self.data.tell()
        aBone.theJiggleBone.baseDamping = self.readFloat()
        aBone.theJiggleBone.baseMinLeft_offset = self.data.tell()
        aBone.theJiggleBone.baseMinLeft = self.readFloat()
        aBone.theJiggleBone.baseMaxLeft_offset = self.data.tell()
        aBone.theJiggleBone.baseMaxLeft = self.readFloat()
        aBone.theJiggleBone.baseLeftFriction_offset = self.data.tell()
        aBone.theJiggleBone.baseLeftFriction = self.readFloat()
        aBone.theJiggleBone.baseMinUp_offset = self.data.tell()
        aBone.theJiggleBone.baseMinUp = self.readFloat()
        aBone.theJiggleBone.baseMaxUp_offset = self.data.tell()
        aBone.theJiggleBone.baseMaxUp = self.readFloat()
        aBone.theJiggleBone.baseUpFriction_offset = self.data.tell()
        aBone.theJiggleBone.baseUpFriction = self.readFloat()
        aBone.theJiggleBone.baseMinForward_offset = self.data.tell()
        aBone.theJiggleBone.baseMinForward = self.readFloat()
        aBone.theJiggleBone.baseMaxForward_offset = self.data.tell()
        aBone.theJiggleBone.baseMaxForward = self.readFloat()
        aBone.theJiggleBone.baseForwardFriction_offset = self.data.tell()
        aBone.theJiggleBone.baseForwardFriction = self.readFloat()

    def ReadTriggers(self, quatInterpBoneInputFileStreamPosition, aQuatInterpBone: SourceMdlQuatInterpBone):
        self.data.seek(quatInterpBoneInputFileStreamPosition + aQuatInterpBone.triggerOffset)
        aTrigger = SourceMdlQuatInterpBoneInfo()
        aTrigger.inverseToleranceAngle = self.readFloat()
        aTrigger.trigger = SourceQuaternion(self.data)
        aTrigger.pos = SourceVector(self.data)
        aTrigger.quat = SourceQuaternion(self.data)
        aQuatInterpBone.theTriggers.append(aTrigger)

    def ReadBoneControllers(self):

        if self.theMdlFileData.boneControllerCount > 0:
            for i in range(self.theMdlFileData.boneControllerCount):
                boneControllerInputFileStreamPosition = self.data.tell()
                self.data.seek(self.theMdlFileData.boneControllerOffset, 0)
                aBoneController = SourceMdlBoneController()
                aBoneController.boneIndex = self.readInt32()
                aBoneController.type = self.readInt32()
                aBoneController.startBlah = self.readInt32()
                aBoneController.endBlah = self.readInt32()
                aBoneController.restIndex = self.readInt32()
                aBoneController.inputField = self.readInt32()
                if self.theMdlFileData.version > 10:
                    aBoneController.unused = []
                    for j in range(8):
                        aBoneController.unused.append(self.readInt32())
                self.theMdlFileData.theBoneControllers.append(aBoneController)

    def ReadAttachments(self):
        if self.theMdlFileData.localAttachmentCount > 0:
            self.data.seek(self.theMdlFileData.localAttachmentOffset, 0)
            for i in range(self.theMdlFileData.localAttachmentCount):
                attachmentInputFileStreamPosition = self.data.tell()
                anAttachment = SourceMdlAttachment()
                if self.theMdlFileData.version == 10:
                    anAttachment['name'] = self.GetName(list([self.ReadBytes('c') for a in range(64)]))
                    # TODO:
                    # Do it for V10
                else:
                    anAttachment.nameOffset = self.readInt32()
                    anAttachment.name = self.GetNameFromOffset(self.data, attachmentInputFileStreamPosition,
                                                               anAttachment.nameOffset) if anAttachment.nameOffset != 0 else ""
                    anAttachment.flags = self.readInt32()
                    anAttachment.localBoneIndex = self.readInt32()
                    anAttachment.localM11 = self.readFloat()
                    anAttachment.localM12 = self.readFloat()
                    anAttachment.localM13 = self.readFloat()
                    anAttachment.localM14 = self.readFloat()
                    anAttachment.localM21 = self.readFloat()
                    anAttachment.localM22 = self.readFloat()
                    anAttachment.localM23 = self.readFloat()
                    anAttachment.localM24 = self.readFloat()
                    anAttachment.localM31 = self.readFloat()
                    anAttachment.localM32 = self.readFloat()
                    anAttachment.localM33 = self.readFloat()
                    anAttachment.localM34 = self.readFloat()
                    anAttachment.unused = list([self.readInt32() for j in range(8)])

                self.theMdlFileData.theAttachments.append(anAttachment)

    def ReadHitboxSets(self):

        self.data.seek(self.theMdlFileData.hitboxSetOffset, 0)
        start = self.data.tell()
        if self.theMdlFileData.hitboxSetCount > 0:
            hitboxSetInputFileStreamPosition = self.data.tell()
            for i in range(self.theMdlFileData.hitboxSetCount):
                aHitboxSet = SourceMdlHitboxSet()
                aHitboxSet.nameOffset = self.readInt32()
                aHitboxSet.name = self.GetNameFromOffset(self.data, hitboxSetInputFileStreamPosition,
                                                         aHitboxSet.nameOffset) if aHitboxSet.nameOffset != 0 else ""
                aHitboxSet.hitboxCount = self.readInt32()
                aHitboxSet.hitboxOffset = self.readInt32()
                inputFileStreamPosition = self.data.tell()

                self.ReadHitboxes(hitboxSetInputFileStreamPosition + aHitboxSet.hitboxOffset, aHitboxSet)
                self.theMdlFileData.theHitboxSets.append(aHitboxSet)
                self.data.seek(inputFileStreamPosition, 0)

    def ReadHitboxes(self, hitboxOffsetInputFileStreamPosition, aHitboxSet: SourceMdlHitboxSet):

        self.data.seek(hitboxOffsetInputFileStreamPosition, 0)
        start = self.data.tell()
        if aHitboxSet.hitboxCount > 0:
            for i in range(aHitboxSet.hitboxCount):
                hitboxInputFileStreamPosition = self.data.tell()
                aHitbox = SourceMdlHitbox()
                aHitbox.boneIndex = self.ReadBytes("i")
                aHitbox.groupIndex = self.ReadBytes("i")
                aHitbox.boundingBoxMin = SourceVector(self.data)
                aHitbox.boundingBoxMax = SourceVector(self.data)
                aHitbox.nameOffset = self.readInt32()
                aHitbox.name = self.GetNameFromOffset(self.data, hitboxInputFileStreamPosition,
                                                      aHitbox.nameOffset) if aHitbox.nameOffset != 0 else ""
                aHitbox.boundingBoxPitchYawRoll = {'z': self.readFloat(), 'x': self.readFloat(),
                                                   "y": self.readFloat()}
                aHitbox.unused_VERSION49 = list([self.readInt32() for j in range(5)])
                aHitboxSet.theHitboxes.append(aHitbox)

    def ReadBoneTableByName(self):
        self.data.seek(self.theMdlFileData.boneTableByNameOffset)
        if self.theMdlFileData.boneTableByNameOffset != 0:
            for i in range(self.theMdlFileData.theBones.__len__()):
                index = self.ReadByte()
                self.theMdlFileData.theBoneTableByName.append(index)

    def ReadBodyParts(self):
        if self.theMdlFileData.bodyPartCount > 0:
            self.data.seek(self.theMdlFileData.bodyPartOffset)
            for i in range(self.theMdlFileData.bodyPartCount):
                start = self.data.tell()
                bodyPartInputFileStreamPosition = self.data.tell()
                aBodyPart = SourceMdlBodyPart()
                aBodyPart.nameOffset = self.readInt32()
                aBodyPart.modelCount = self.readInt32()
                aBodyPart.base = self.readInt32()
                aBodyPart.modelOffset = self.readInt32()

                inputFileStreamPosition = self.data.tell()

                if aBodyPart.nameOffset != 0:
                    aBodyPart.name = self.GetNameFromOffset(self.data, bodyPartInputFileStreamPosition,
                                                            aBodyPart.nameOffset) if aBodyPart.nameOffset != 0 else ""

                self.ReadModels(bodyPartInputFileStreamPosition, aBodyPart)

                self.theMdlFileData.theBodyParts.append(aBodyPart)
                self.data.seek(inputFileStreamPosition, 0)

    def ReadModels(self, bodyPartInputFileStreamPosition, aBodyPart: SourceMdlBodyPart):
        if aBodyPart.modelCount > 0:
            # print(bodyPartInputFileStreamPosition,aBodyPart.modelOffset)
            self.data.seek(bodyPartInputFileStreamPosition + aBodyPart.modelOffset, 0)

            for j in range(aBodyPart.modelCount):
                start = self.data.tell()
                modelInputFileStreamPosition = self.data.tell()
                aModel = SourceMdlModel()
                aModel.name = list([self.ReadBytes('c') for _ in range(64)])
                aModel.name = self.GetName(aModel.name)
                # print(aModel.name)
                aModel.type = self.readInt32()
                aModel.boundingRadius = self.readFloat()
                aModel.meshCount = self.readInt32()
                aModel.meshOffset = self.readInt32()
                aModel.vertexCount = self.readInt32()
                aModel.vertexOffset = self.readInt32()
                aModel.tangentOffset = self.readInt32()
                aModel.attachmentCount = self.readInt32()
                aModel.attachmentOffset = self.readInt32()
                aModel.eyeballCount = self.readInt32()
                aModel.eyeballOffset = self.readInt32()

                aModel.vertexData.vertexDataP = self.readInt32()
                aModel.vertexData.tangentDataP = self.readInt32()
                aModel.unused = []
                for x in range(8):
                    aModel.unused.append(self.readInt32())
                inputFileStreamPosition = self.data.tell()

                self.ReadEyeballs(modelInputFileStreamPosition, aModel)
                self.ReadMeshes(modelInputFileStreamPosition, aModel)

                aBodyPart.theModels.append(aModel)

                self.data.seek(inputFileStreamPosition, 0)

    def ReadEyeballs(self, modelInputFileStreamPosition, aModel: SourceMdlModel):

        if aModel.eyeballCount > 0 and aModel.eyeballOffset != 0:
            self.data.seek(aModel.eyeballOffset + modelInputFileStreamPosition, 0)
            start = self.data.tell()
            for i in range(aModel.eyeballCount):
                eyeballInputFileStreamPosition = self.data.tell()
                anEyeball = SourceMdlEyeball()
                anEyeball.nameOffset = self.readInt32()
                anEyeball.boneIndex = self.readInt32()
                anEyeball.org = SourceVector(self.data)
                anEyeball.zOffset = self.readFloat()
                anEyeball.radius = self.readFloat()
                anEyeball.up = SourceVector(self.data)
                anEyeball.forward = SourceVector(self.data)
                anEyeball.unused1 = self.readInt32()
                anEyeball.irisScale = self.readFloat()
                anEyeball.unused2 = self.readInt32()
                anEyeball.upperFlexDesc = []
                for j in range(3):
                    anEyeball.upperFlexDesc.append(self.readInt32())
                anEyeball.lowerFlexDesc = []
                for j in range(3):
                    anEyeball.lowerFlexDesc.append(self.readInt32())
                anEyeball.upperTarget = []
                for j in range(3):
                    anEyeball.upperTarget.append(self.readFloat())
                anEyeball.lowerTarget = []
                for j in range(3):
                    anEyeball.lowerTarget.append(self.readFloat())
                anEyeball.upperLidFlexDesc = self.readInt32()
                anEyeball.lowerLidFlexDesc = self.readInt32()
                anEyeball.unused = []
                for j in range(4):
                    anEyeball.unused.append(self.readFloat())
                anEyeball.eyeballIsNonFacs = self.readUByte()
                anEyeball.unused3 = []
                for j in range(3):
                    anEyeball.unused3.append(self.ReadBytes('c'))
                anEyeball.unused4 = []
                for j in range(7):
                    anEyeball.unused4.append(self.readInt32())
                inputFileStreamPosition = self.data.tell()

                if anEyeball.nameOffset != 0:
                    anEyeball.name = self.GetNameFromOffset(self.data, eyeballInputFileStreamPosition,
                                                            anEyeball.nameOffset)
                else:
                    anEyeball.name = ""

                self.data.seek(inputFileStreamPosition, 0)

                if len(aModel.theEyeballs) > 0:
                    self.theMdlFileData.theModelCommandIsUsed = True

                aModel.theEyeballs.append(anEyeball)

    def ReadMeshes(self, modelInputFileStreamPosition, aModel: SourceMdlModel):
        if aModel.meshCount > 0 and aModel.meshOffset != 0:
            self.data.seek(modelInputFileStreamPosition + aModel.meshOffset, 0)
            for meshIndex in range(aModel.meshCount):
                start = self.data.tell()
                meshInputFileStreamPosition = self.data.tell()
                aMesh = SourceMdlMesh()
                # print('materialIndex',self.data.tell())
                aMesh.materialIndex = self.readInt32()
                aMesh.modelOffset = self.readInt32()
                aMesh.vertexCount = self.readInt32()
                aMesh.vertexIndexStart = self.readInt32()
                aMesh.flexCount = self.readInt32()
                aMesh.flexOffset = self.readInt32()
                aMesh.materialType = self.readInt32()
                aMesh.materialParam = self.readInt32()
                aMesh.id = self.readInt32()
                aMesh.centerX = self.readFloat()
                aMesh.centerY = self.readFloat()
                aMesh.centerZ = self.readFloat()
                meshVertexData = SourceMdlMeshVertexData()
                meshVertexData.modelVertexDataP = self.readInt32()
                for x in range(8):
                    meshVertexData.lodVertexCount.append(self.readInt32())
                aMesh.vertexData = meshVertexData
                for x in range(8):
                    aMesh.unused.append(self.readInt32())
                aModel.theMeshes.append(aMesh)
                if aMesh.materialType == 1:
                    aModel.theEyeballs[aMesh.materialParam].theTextureIndex = aMesh.materialIndex
                inputFileStreamPosition = self.data.tell()
                if aMesh.flexCount > 0 and aMesh.flexOffset != 0:
                    self.ReadFlexes(meshInputFileStreamPosition, aMesh)
                self.data.seek(inputFileStreamPosition, 0)

    def ReadFlexes(self, meshInputFileStreamPosition, aMesh: SourceMdlMesh):
        self.data.seek(meshInputFileStreamPosition + aMesh.flexOffset, 0)

        if aMesh.flexCount > 0:
            for k in range(aMesh.flexCount):
                flexInputFileStreamPosition = self.data.tell()
                aFlex = SourceMdlFlex()
                aFlex.flexDescIndex = self.readInt32()
                aFlex.target0 = self.readFloat()
                aFlex.target1 = self.readFloat()
                aFlex.target2 = self.readFloat()
                aFlex.target3 = self.readFloat()

                aFlex.vertCount = self.readInt32()
                aFlex.vertOffset = self.readInt32()

                aFlex.flexDescPartnerIndex = self.readInt32()
                aFlex.vertAnimType = self.readUByte()
                aFlex.unusedChar = []
                for x in range(3):
                    aFlex.unusedChar.append(self.ReadBytes('c'))
                aFlex.unused = []
                for x in range(6):
                    aFlex.unused.append(self.readInt32())
                inputFileStreamPosition = self.data.tell()

                if aFlex.vertCount > 0 and aFlex.vertOffset != 0:
                    self.ReadVertAnims(flexInputFileStreamPosition, aFlex)
                self.data.seek(inputFileStreamPosition, 0)

                aMesh.theFlexes.append(aFlex)

    def ReadVertAnims(self, flexInputFileStreamPosition, aFlex: SourceMdlFlex):
        self.data.seek(flexInputFileStreamPosition + aFlex.vertOffset, 0)
        for k in range(aFlex.vertCount):
            if aFlex.vertAnimType == aFlex.STUDIO_VERT_ANIM_WRINKLE:
                aVertAnim = SourceMdlVertAnimWrinkle()
            else:
                aVertAnim = SourceMdlVertAnim()
            aVertAnim.index = self.readUInt16()
            aVertAnim.speed = self.readUByte()
            aVertAnim.side = self.readUByte()
            aVertAnim.theDelta = []
            for x in range(3):
                aFloat = SourceFloat16bits()
                aFloat.the16BitValue = self.readUInt16()
                aVertAnim.theDelta.append(aFloat.TheFloatValue)

            aVertAnim.theNDelta = []
            for x in range(3):
                aFloat = SourceFloat16bits()
                aFloat.the16BitValue = self.readUInt16()
                aVertAnim.theNDelta.append(aFloat.TheFloatValue)
            if aFlex.vertAnimType == aFlex.STUDIO_VERT_ANIM_WRINKLE:
                aVertAnim.wrinkleDelta = self.readInt16()
            # pprint(aVertAnim)
            aFlex.theVertAnims.append(aVertAnim)

    def ReadFlexDescs(self):
        if self.theMdlFileData.flexDescCount > 0:
            self.data.seek(self.theMdlFileData.flexDescOffset, 0)
            for i in range(self.theMdlFileData.flexDescCount):
                flexDescInputFileStreamPosition = self.data.tell()
                aFlexDesc = SourceMdlFlexDesc()
                aFlexDesc.nameOffset = self.ReadInt32()
                inputFileStreamPosition = self.data.tell()
                if aFlexDesc.nameOffset != 0:
                    aFlexDesc.theName = self.GetNameFromOffset(self.data, flexDescInputFileStreamPosition,
                                                               aFlexDesc.nameOffset)
                self.data.seek(inputFileStreamPosition, 0)
                self.theMdlFileData.theFlexDescs.append(aFlexDesc)

    def ReadFlexControllers(self):
        if self.theMdlFileData.flexControllerCount > 0:
            self.data.seek(self.theMdlFileData.flexControllerOffset, 0)
            for i in range(self.theMdlFileData.flexControllerCount):
                flexControllerInputFileStreamPosition = self.data.tell()
                aFlexController = SourceMdlFlexController()
                aFlexController.typeOffset = self.ReadInt32()
                aFlexController.nameOffset = self.ReadInt32()
                aFlexController.localToGlobal = self.ReadInt32()
                aFlexController.min = self.ReadFloat()
                aFlexController.max = self.ReadFloat()
                self.theMdlFileData.theFlexControllers.append(aFlexController)
                inputFileStreamPosition = self.data.tell()
                if aFlexController.typeOffset != 0:
                    aFlexController.theType = self.GetNameFromOffset(self.data, flexControllerInputFileStreamPosition,
                                                                     aFlexController.typeOffset)
                else:
                    aFlexController.theType = ''
                if aFlexController.nameOffset != 0:
                    aFlexController.theName = self.GetNameFromOffset(self.data, flexControllerInputFileStreamPosition,
                                                                     aFlexController.nameOffset)
                else:
                    aFlexController.theName = 'blank_name_' + str(i)
                self.data.seek(inputFileStreamPosition, 0)

                if self.theMdlFileData.theFlexControllers.__len__() > 0:
                    self.theMdlFileData.theModelCommandIsUsed = True

    def ReadFlexRules(self):
        self.data.seek(self.theMdlFileData.flexRuleOffset, 0)
        for i in range(self.theMdlFileData.flexRuleCount):
            flexRuleInputFileStreamPosition = self.data.tell()
            aFlexRule = SourceMdlFlexRule()
            aFlexRule.flexIndex = self.ReadInt32()
            aFlexRule.opCount = self.ReadInt32()
            aFlexRule.opOffset = self.ReadInt32()
            inputFileStreamPosition = self.data.tell()
            if aFlexRule.opCount > 0 and aFlexRule.opOffset != 0:
                self.ReadFlexOps(flexRuleInputFileStreamPosition, aFlexRule)
            self.theMdlFileData.theFlexDescs[aFlexRule.flexIndex].theDescIsUsedByFlexRule = True
            self.theMdlFileData.theFlexRules.append(aFlexRule)
            self.data.seek(inputFileStreamPosition, 0)

        if self.theMdlFileData.theFlexRules.__len__() > 0:
            self.theMdlFileData.theModelCommandIsUsed = True

    def ReadFlexOps(self, flexRuleInputFileStreamPosition, aFlexRule: SourceMdlFlexRule):
        self.data.seek(flexRuleInputFileStreamPosition + aFlexRule.opOffset)
        for i in range(aFlexRule.opCount):
            aFlexOp = SourceMdlFlexOp()
            aFlexOp.op = self.ReadInt32()
            if aFlexOp.op == SourceMdlFlexOp.STUDIO_CONST:
                aFlexOp.value = self.ReadFloat()
            else:
                aFlexOp.index = self.ReadInt32()
                if aFlexOp.op == SourceMdlFlexOp.STUDIO_FETCH2:
                    self.theMdlFileData.theFlexDescs[aFlexOp.index].theDescIsUsedByFlexRule = True
            aFlexRule.theFlexOps.append(aFlexOp)

    def CreateFlexFrameList(self):
        aFlexFrame = FlexFrame()
        self.theMdlFileData.theFlexFrames.append(aFlexFrame)

        if self.theMdlFileData.theFlexFrames != [] and self.theMdlFileData.theFlexFrames.__len__() > 0:
            flexDescToFlexFrames = [None] * self.theMdlFileData.theFlexDescs.__len__()  # type: List[List[FlexFrame]]
            meshVertexIndexStart = 0
            for x in range(self.theMdlFileData.theFlexDescs.__len__()):
                flexFrameList = []  # type: List[FlexFrame]
                flexDescToFlexFrames.append(flexFrameList)
            for aBodyPart in self.theMdlFileData.theBodyParts:  # type: SourceMdlBodyPart
                if aBodyPart.theModels and aBodyPart.theModels.__len__() > 0:
                    for aModel in aBodyPart.theModels:  # type: SourceMdlModel
                        if aModel.theMeshes and aModel.theMeshes.__len__() > 0:
                            for aMesh in aModel.theMeshes:  # type: SourceMdlMesh
                                meshVertexIndexStart = aMesh.vertexIndexStart
                                if aMesh.theFlexes and aMesh.theFlexes.__len__() > 0:
                                    for flexIndex, aFlex in enumerate(aMesh.theFlexes):  # type: SourceMdlFlex
                                        aFlexFrame = None
                                        if flexDescToFlexFrames[aFlex.flexDescIndex] is not None:
                                            for x in range(len(flexDescToFlexFrames[aFlex.flexDescIndex])):
                                                searchedFlexFrame = flexDescToFlexFrames[aFlex.flexDescIndex][x]
                                                if searchedFlexFrame.flexes[0].target0 == aFlex.target0 and \
                                                                searchedFlexFrame.flexes[0].target1 == aFlex.target1 and \
                                                                searchedFlexFrame.flexes[0].target2 == aFlex.target2 and \
                                                                searchedFlexFrame.flexes[0].target3 == aFlex.target3:
                                                    aFlexFrame = searchedFlexFrame
                                        if not aFlexFrame:
                                            aFlexFrame = FlexFrame()
                                            aFlexFrame.bodyAndMeshVertexIndexStarts = []  # type: List[int]
                                            aFlexFrame.flexes = []  # type: List[SourceMdlFlex]
                                            aFlexDescPartnerIndex = aMesh.theFlexes[flexIndex].flexDescPartnerIndex
                                            aFlexFrame.flexName = self.theMdlFileData.theFlexDescs[
                                                aFlex.flexDescIndex].theName
                                            if aFlexDescPartnerIndex > 0:
                                                aFlexFrame.flexDescription = aFlexFrame.flexName \
                                                                             + '+' \
                                                                             + self.theMdlFileData.theFlexDescs[
                                                                                 aFlex.flexDescIndex].theName
                                                aFlexFrame.flexHasParner = True
                                                aFlexFrame.flexSplit = 1
                                                self.theMdlFileData.theFlexDescs[
                                                    aFlex.flexDescPartnerIndex].theDescIsUsedByFlex = True
                                                aFlexFrame.flexDescription = aFlexFrame.flexName
                                                aFlexFrame.flexHasPartner = False
                                            self.theMdlFileData.theFlexDescs[
                                                aFlex.flexDescIndex].theDescIsUsedByFlex = True

                                            self.theMdlFileData.theFlexFrames.append(aFlexFrame)
                                        aFlexFrame.bodyAndMeshVertexIndexStarts.append(meshVertexIndexStart)
                                        aFlexFrame.flexes.append(aFlex)

    def ReadTextures(self):
        if self.theMdlFileData.textureCount < 1:
            return
        self.data.seek(self.theMdlFileData.textureOffset, 0)
        for i in range(self.theMdlFileData.textureCount):
            textureInputFileStreamPosition = self.data.tell()
            aTexture = SourceMdlTexture()
            aTexture.nameOffset = self.ReadInt32()
            aTexture.flags = self.ReadInt32()
            aTexture.used = self.ReadInt32()
            aTexture.unused1 = self.ReadInt32()
            aTexture.materialP = self.ReadInt32()
            aTexture.clientMaterialP = self.ReadInt32()
            for x in range(0, 10):
                aTexture.unused.append(self.ReadInt32())

            inputFileStreamPosition = self.data.tell()

            if aTexture.nameOffset != 0:
                aTexture.thePathFileName = self.GetNameFromOffset(self.data, textureInputFileStreamPosition,
                                                                  aTexture.nameOffset)
            else:
                pass
                # aTexture.thePathFileName = ''
            self.data.seek(inputFileStreamPosition, 0)

            self.theMdlFileData.theTextures.append(aTexture)

    def ReadTexturePaths(self):
        if self.theMdlFileData.texturePathCount > 0:
            self.data.seek(self.theMdlFileData.texturePathOffset, 0)
            for i in range(self.theMdlFileData.texturePathCount):
                texturePathInputFileStreamPosition = self.data.tell()
                texturePathOffset = self.ReadInt32()
                inputFileStreamPosition = self.data.tell()
                if texturePathOffset != 0:
                    aTexturePath = self.GetNameFromOffset(self.data, texturePathOffset, 0)
                else:
                    aTexturePath = ''
                self.theMdlFileData.theTexturePaths.append(aTexturePath)
                self.data.seek(inputFileStreamPosition, 0)

    def ReadLocalAnimationDescs(self):
        aSectionOfAnimation = []  # type: List[SourceMdlAnimation]
        animationDescSize = 0

        self.data.seek(self.theMdlFileData.localAnimationOffset, 0)
        fileOffsetStart = self.data.tell()

        for i in range(self.theMdlFileData.localAnimationCount):
            animInputFileStreamPosition = self.data.tell()

            anAnimationDesc = SourceMdlAnimationDesc49()
            anAnimationDesc.baseHeaderOffset = self.readInt32()
            anAnimationDesc.nameOffset = self.ReadInt32()
            if anAnimationDesc.nameOffset != 0:
                anAnimationDesc.theName = self.GetNameFromOffset(self.data, animInputFileStreamPosition,
                                                                 anAnimationDesc.nameOffset)

            anAnimationDesc.fps = self.ReadFloat()
            anAnimationDesc.flags = self.ReadInt32()

            anAnimationDesc.frameCount = self.ReadInt32()
            anAnimationDesc.movementCount = self.ReadInt32()
            anAnimationDesc.movementOffset = self.ReadInt32()

            anAnimationDesc.ikRuleZeroFrameOffset = self.ReadInt32()

            for x in range(anAnimationDesc.unused1.__len__()):
                anAnimationDesc.unused1[x] = self.ReadInt32()

            anAnimationDesc.animBlock = self.ReadInt32()
            anAnimationDesc.animOffset = self.ReadInt32()
            anAnimationDesc.ikRuleCount = self.ReadInt32()
            anAnimationDesc.ikRuleOffset = self.ReadInt32()
            anAnimationDesc.animblockIkRuleOffset = self.ReadInt32()
            anAnimationDesc.localHierarchyCount = self.ReadInt32()
            anAnimationDesc.localHierarchyOffset = self.ReadInt32()
            anAnimationDesc.sectionOffset = self.ReadInt32()
            anAnimationDesc.sectionFrameCount = self.ReadInt32()

            anAnimationDesc.spanFrameCount = self.readInt16()
            anAnimationDesc.spanCount = self.readInt16()
            anAnimationDesc.spanOffset = self.ReadInt32()
            anAnimationDesc.spanStallTime = self.ReadFloat()
            if DEBUG:
                print(anAnimationDesc.__dict__)

            inputFileStreamPosition = self.data.tell()
            if i == 0:
                animationDescSize = inputFileStreamPosition - animInputFileStreamPosition

            self.theMdlFileData.theAnimationDescs.append(anAnimationDesc)
            debug_write(fileOffsetStart,'-', self.data.tell(), "theMdlFileData.theAnimationDescs")
        for i in range(self.theMdlFileData.localAnimationCount):
            anAnimationDesc = self.theMdlFileData.theAnimationDescs[i]  # type: MDL_DATA.SourceMdlAnimationDesc49
            if DEBUG:
                print(anAnimationDesc.__dict__)

            animInputFileStreamPosition = fileOffsetStart + (i * animationDescSize)

            if self.theMdlFileData.theFirstAnimationDesc is None and not anAnimationDesc.theName.startswith('@'):
                self.theMdlFileData.theFirstAnimationDesc = anAnimationDesc

            if (anAnimationDesc.flags & SourceMdlAnimationDesc49.STUDIO_ALLZEROS) == 0:
                debug_write('STUDIO_ALLZEROS')
                anAnimationDesc.theSectionsOfAnimations = [[]]  # type: List[List[SourceMdlAnimation]]
                aSectionOfAnimation = []  # type: List[SourceMdlAnimation]
                if (anAnimationDesc.flags & SourceMdlAnimationDesc49.STUDIO_FRAMEANIM) != 0:
                    debug_write('STUDIO_FRAMEANIM')

                    if anAnimationDesc.sectionOffset != 0 and anAnimationDesc.sectionFrameCount > 0:
                        debug_write('sectionOffset !=0 ,sectionFrameCount > 0 ')
                        self.theMdlFileData.theSectionFrameCount = anAnimationDesc.sectionFrameCount

                        if self.theMdlFileData.theSectionFrameMinFrameCount >= anAnimationDesc.sectionFrameCount:
                            self.theMdlFileData.theSectionFrameMinFrameCount = anAnimationDesc.frameCount-1
                        # sectionCount = math.trunc(anAnimationDesc.frameCount / anAnimationDesc.sectionFrameCount) + 2

                        for sectionIndex in range(1,sectionCount):
                            aSectionOfAnimation = []  # type: List[SourceMdlAnimation]
                            anAnimationDesc.theSectionsOfAnimations.append(aSectionOfAnimation)

                        self.data.seek(animInputFileStreamPosition + anAnimationDesc.sectionOffset, 0)

                        anAnimationDesc.theSections = []  # type: List[SourceMdlAnimationSection]

                        for sectionIndex in range(sectionCount):
                            self.ReadMdlAnimationSection(self.data.tell(), anAnimationDesc, )

                        if anAnimationDesc.animBlock == 0:
                            for sectionIndex in range(sectionCount):
                                aSectionOfAnimation = anAnimationDesc.theSectionsOfAnimations[sectionIndex]
                                self.data.seek(
                                    animInputFileStreamPosition + anAnimationDesc.theSections[sectionIndex].animOffset,
                                    0)
                                if sectionIndex < sectionCount - 2:
                                    sectionFrameCount = anAnimationDesc.sectionFrameCount
                                else:
                                    sectionFrameCount = anAnimationDesc.frameCount - (
                                        (sectionCount - 2) * anAnimationDesc.sectionFrameCount)
                                self.ReadAnimationFrameByBone(self.data.tell(), anAnimationDesc,
                                                              anAnimationDesc.frameCount,
                                                              anAnimationDesc.theSectionsOfAnimations[0])
                    elif anAnimationDesc.animBlock == 0:
                        self.data.seek(animInputFileStreamPosition + anAnimationDesc.animOffset, 0)
                        debug_write("anAnimationDesc.theAnimations [ReadAnimationFrameByBone()] pre-alignment (NOTE: Should end at: " + str(animInputFileStreamPosition + anAnimationDesc.animOffset - 1) + ")")
                        self.ReadAnimationFrameByBone(self.data.tell(), anAnimationDesc, anAnimationDesc.frameCount,
                                                      anAnimationDesc.theSectionsOfAnimations[0])

                else:

                    if anAnimationDesc.sectionOffset != 0 and anAnimationDesc.sectionFrameCount > 0:

                        self.theMdlFileData.theSectionFrameCount = anAnimationDesc.sectionFrameCount

                        if self.theMdlFileData.theSectionFrameMinFrameCount >= anAnimationDesc.sectionFrameCount:
                            self.theMdlFileData.theSectionFrameMinFrameCount = anAnimationDesc.frameCount-1
                        sectionCount = math.trunc(anAnimationDesc.frameCount / anAnimationDesc.sectionFrameCount) + 2

                        for sectionIndex in range(1,sectionCount):
                            aSectionOfAnimation = []  # type: List[SourceMdlAnimation]
                            anAnimationDesc.theSectionsOfAnimations.append(aSectionOfAnimation)

                        self.data.seek(animInputFileStreamPosition + anAnimationDesc.sectionOffset, 0)

                        anAnimationDesc.theSections = []  # type: SourceMdlAnimationSection
                        for sectionIndex in range(sectionCount):
                            self.ReadMdlAnimationSection(self.data.tell(), anAnimationDesc)

                        if anAnimationDesc.animBlock == 0:
                            for sectionIndex in range(sectionCount):
                                aSectionOfAnimation = anAnimationDesc.theSectionsOfAnimations[sectionIndex]
                                self.data.seek(
                                    animInputFileStreamPosition + anAnimationDesc.theSections[sectionIndex].animOffset,
                                    0)
                                if sectionIndex < sectionCount - 2:
                                    sectionFrameCount = anAnimationDesc.sectionFrameCount
                                else:
                                    sectionFrameCount = anAnimationDesc.frameCount - (
                                        (sectionCount - 2) * anAnimationDesc.sectionFrameCount)
                                self.ReadMdlAnimation(self.data.tell(), anAnimationDesc, sectionFrameCount,
                                                      aSectionOfAnimation)
                    elif anAnimationDesc.animBlock == 0:
                        fileOffsetEnd = self.data.tell()
                        debug_write(fileOffsetEnd,'-',fileOffsetEnd+16,
                            "anAnimationDesc.theAnimations pre-alignment (NOTE: Should end at: " + str(
                                animInputFileStreamPosition + anAnimationDesc.animOffset) + ")")
                        self.data.seek(animInputFileStreamPosition + anAnimationDesc.animOffset)
                        self.ReadMdlAnimation(self.data.tell(), anAnimationDesc, anAnimationDesc.frameCount,anAnimationDesc.theSectionsOfAnimations[0])
                anAnimationDesc.theSectionsOfAnimations.append(aSectionOfAnimation)
                if anAnimationDesc.animBlock == 0 and anAnimationDesc.ikRuleCount > 0:
                    pass
                if anAnimationDesc.animBlock == 0 and anAnimationDesc.localHierarchyCount > 0:
                    self.ReadLocalHierarchies(animInputFileStreamPosition, anAnimationDesc)
            inputFileStreamPosition = self.data.tell()
            if anAnimationDesc.movementCount > 0:
                self.ReadMdlMovements(animInputFileStreamPosition, anAnimationDesc)
            self.data.seek(inputFileStreamPosition, 0)

    def ReadLocalHierarchies(self, animInputFileStreamPosition, anAnimationDesc: SourceMdlAnimationDesc49):
        self.data.seek(animInputFileStreamPosition + anAnimationDesc.localHierarchyOffset, 0)
        anAnimationDesc.theLocalHierarchies = []  # type: List[SourceMdlLocalHierarchy]
        for j in range(anAnimationDesc.localHierarchyCount):
            aLocalHierarchy = SourceMdlLocalHierarchy()
            aLocalHierarchy.boneIndex = self.ReadInt32()
            aLocalHierarchy.boneNewParentIndex = self.ReadInt32()
            aLocalHierarchy.startInfluence = self.ReadFloat()
            aLocalHierarchy.peakInfluence = self.ReadFloat()
            aLocalHierarchy.tailInfluence = self.ReadFloat()
            aLocalHierarchy.endInfluence = self.ReadFloat()
            aLocalHierarchy.startFrameIndex = self.ReadInt32()
            aLocalHierarchy.localAnimOffset = self.ReadInt32()
            for x in range(4):
                aLocalHierarchy.unused.append(self.ReadInt32())
            anAnimationDesc.theLocalHierarchies.append(aLocalHierarchy)

    def ReadMdlMovements(self, animInputFileStreamPosition, anAnimationDesc: SourceMdlAnimationDesc49):
        self.data.seek(animInputFileStreamPosition + anAnimationDesc.movementOffset, 0)
        anAnimationDesc.theMovements = []  # type: List[SourceMdlMovement]
        for j in range(anAnimationDesc.movementCount):
            aMovement = SourceMdlMovement()
            aMovement.endframeIndex = self.ReadInt32()
            aMovement.motionFlags = self.ReadInt32()
            aMovement.v0 = self.ReadFloat()
            aMovement.v1 = self.ReadFloat()
            aMovement.angle = self.ReadFloat()

            aMovement.vector = SourceVector(self.data)
            aMovement.position = SourceVector(self.data)
            if DEBUG:
                print('aMovement', aMovement.__dict__)
            anAnimationDesc.theMovements.append(aMovement)

    def ReadMdlAnimationSection(self, animInputFileStreamPosition, anAnimationDesc: SourceMdlAnimationDesc49):
        anAnimSection = SourceMdlAnimationSection()
        anAnimSection.animBlock = self.ReadInt32()
        anAnimSection.animOffset = self.ReadInt32()
        if DEBUG:
            print('anAnimSection', anAnimSection.__dict__)

        anAnimationDesc.theSections.append(anAnimSection)

    def ReadAnimationFrameByBone(self, animInputFileStreamPosition, anAnimationDesc: SourceMdlAnimationDesc49,
                                 sectionFrameCount, aSectionOfAnimation: List[SourceMdlAnimation]):
        self.data.seek(animInputFileStreamPosition, 0)

        boneCount = self.theMdlFileData.theBones.__len__()
        try:
            animFrameInputFileStreamPosition = self.data.tell()
            anAniFrameAnim = SourceAniFrameAnim()
            anAnimationDesc.theAniFrameAnim = anAniFrameAnim
            anAniFrameAnim.constantsOffset = self.ReadInt32()
            anAniFrameAnim.frameOffset = self.ReadInt32()
            anAniFrameAnim.frameLength = self.ReadInt32()
            for x in range(3):
                anAniFrameAnim.unused[x] = self.ReadInt32()
            anAniFrameAnim.theBoneFlags = []  # type: List[int]
            for boneIndex in range(boneCount):
                boneFlag = self.ReadByte()
                anAniFrameAnim.theBoneFlags.append(boneFlag)
            if anAniFrameAnim.constantsOffset != 0:
                self.data.seek(animFrameInputFileStreamPosition + anAniFrameAnim.constantsOffset, 0)
                anAniFrameAnim.theBoneConstantInfos = []  # type: List[BoneConstantInfo]
                for boneIndex in range(boneCount):
                    aBoneConstantInfo = BoneConstantInfo()
                    boneFlag = anAniFrameAnim.theBoneFlags[boneIndex]
                    if DEBUG:
                        print('boneFlag', boneFlag, hex(boneFlag))
                    if (boneFlag & anAniFrameAnim.STUDIO_FRAME_RAWROT) > 0:
                        aBoneConstantInfo.theConstantRawRot = SourceQuaternion48bits()
                        aBoneConstantInfo.theConstantRawRot.theXInput = self.ReadBytes('H')
                        aBoneConstantInfo.theConstantRawRot.theYInput = self.ReadBytes('H')
                        aBoneConstantInfo.theConstantRawRot.theZWInput = self.ReadBytes('H')
                    if (boneFlag & SourceAniFrameAnim.STUDIO_FRAME_RAWPOS) > 0:
                        BoneConstantInfo.theConstantRawPos = SourceVector48bits()
                        aBoneConstantInfo.theConstantRawPos.theXInput.the16BitValue = self.ReadBytes('H')
                        aBoneConstantInfo.theConstantRawPos.theYInput.the16BitValue = self.ReadBytes('H')
                        aBoneConstantInfo.theConstantRawPos.theZInput.the16BitValue = self.ReadBytes('H')
                    anAniFrameAnim.theBoneConstantInfos.append(aBoneConstantInfo)
            if anAniFrameAnim.frameOffset != 0:
                self.data.seek(animFrameInputFileStreamPosition + anAniFrameAnim.frameOffset, 0)
                anAniFrameAnim.theBoneFrameDataInfos = []  # type: List[List[BoneFrameDataInfo]]
                for frameIndex in range(sectionFrameCount):
                    aBoneFrameDataInfoList = []  # type: List[BoneFrameDataInfo]
                    boneFrameDataStartInputFileStreamPosition = self.data.tell()
                    for boneIndex in range(boneCount):
                        aBoneFrameDataInfo = BoneFrameDataInfo()
                        boneFlag = anAniFrameAnim.theBoneFlags[boneIndex]

                        if (boneFlag & SourceAniFrameAnim.STUDIO_FRAME_ANIMROT) > 0:
                            aBoneFrameDataInfo.theAnimRotation = SourceQuaternion48bits()
                            aBoneFrameDataInfo.theAnimRotation.theXInput = self.ReadBytes('H')
                            aBoneFrameDataInfo.theAnimRotation.theYInput = self.ReadBytes('H')
                            aBoneFrameDataInfo.theAnimRotation.theZWInput = self.ReadBytes('H')
                        if (boneFlag & SourceAniFrameAnim.STUDIO_FRAME_ANIMPOS) > 0:
                            aBoneFrameDataInfo.theAnimPosition = SourceVector48bits()
                            aBoneFrameDataInfo.theAnimPosition.theXInput.the16BitValue = self.ReadBytes('H')
                            aBoneFrameDataInfo.theAnimPosition.theYInput.the16BitValue = self.ReadBytes('H')
                            aBoneFrameDataInfo.theAnimPosition.theZInput.the16BitValue = self.ReadBytes('H')
                        if (boneFlag & SourceAniFrameAnim.STUDIO_FRAME_FULLANIMPOS) > 0:
                            aBoneFrameDataInfo.theFullAnimPosition = SourceVector(self.data)

                        aBoneFrameDataInfoList.append(aBoneFrameDataInfo)

                    anAniFrameAnim.theBoneFrameDataInfos.append(aBoneFrameDataInfoList)
                    if DEBUG:
                        print('ReadAnimationFrameByBone')
                        pprint(anAniFrameAnim.__dict__)
        except Exception as E:
            import os, sys, traceback

            print(E)
            Tbtype, Tbvalue, traceback_ = sys.exc_info()
            print(Tbtype, Tbvalue)
            print(traceback.print_tb(traceback_))

    def ReadMdlAnimValues(self, animValuesInputFileStreamPosition, frameCount,
                          theAnimValues: List[SourceMdlAnimationValue], ):
        self.data.seek(animValuesInputFileStreamPosition, 0)
        animValue = SourceMdlAnimationValue()
        frameCountRemainingToBeChecked = frameCount
        accumulatedTotal = 0
        if DEBUG:
            print('ReadMdlAnimValues', self.data.tell())
        while frameCountRemainingToBeChecked > 0:
            animValue.value = self.readInt16()
            if DEBUG:
                print('animValue.value', animValue.value)
            currentTotal = animValue.total
            accumulatedTotal += currentTotal
            if currentTotal == 0:
                print('BAD IF THIS REACHED')
                break
            frameCountRemainingToBeChecked -= currentTotal
            theAnimValues.append(animValue)
            validCount = animValue.valid
            for i in range(validCount):
                animValue.value = self.ReadShort()
                theAnimValues.append(animValue)

    def ReadMdlAnimation(self, animInputFileStreamPosition, anAnimationDesc: SourceMdlAnimationDesc49,
                         sectionFrameCount, aSectionOfAnimation: List[SourceMdlAnimation]):
        if DEBUG:
            print('ReadMdlAnimation')
        boneCount = self.theMdlFileData.theBones.__len__()
        for j in range(boneCount):
            animationInputFileStreamPosition = self.data.tell()
            boneIndex = self.ReadByte()
            if boneIndex == 255:
                self.ReadByte()
                self.readInt16()
                input('boneIndex = 255')
                break
            if boneIndex >= boneCount:
                debug_write('Bone index out of range {} - {}'.format(boneIndex, boneCount))
                break
                # raise IndexError('Bone index out of range {} - {}'.format(boneIndex,boneCount))

            anAnimation = SourceMdlAnimation()

            anAnimation.boneIndex = boneIndex
            anAnimation.flags = self.ReadByte()
            anAnimation.nextSourceMdlAnimationOffset = self.ReadShort()
            # print(anAnimation.flags)
            if (anAnimation.flags & SourceMdlAnimation.STUDIO_ANIM_RAWROT2) > 0:
                anAnimation.theRot64bits = SourceQuaternion64bits()
                anAnimation.theRot64bits.theBytes = [self.ReadByte() for i in range(8)]
                if DEBUG:
                    print('theRot64bits {}'.format(anAnimation.theRot64bits.theBytes))
            if (anAnimation.flags & SourceMdlAnimation.STUDIO_ANIM_RAWROT) > 0:
                anAnimation.theRot48bits = SourceQuaternion48bits()
                anAnimation.theRot48bits.theXInput.the16BitValue = self.ReadBytes('H')
                anAnimation.theRot48bits.theYInput.the16BitValue = self.ReadBytes('H')
                anAnimation.theRot48bits.theZWInput.the16BitValue = self.ReadBytes('H')
                if DEBUG:
                    print('theRot48bits', anAnimation.theRot48bits.__dict__)
            if (anAnimation.flags & SourceMdlAnimation.STUDIO_ANIM_RAWPOS) > 0:
                anAnimation.thePos = SourceVector48bits()
                anAnimation.thePos.theXInput.the16BitValue = self.ReadBytes('H')
                anAnimation.thePos.theYInput.the16BitValue = self.ReadBytes('H')
                anAnimation.thePos.theZInput.the16BitValue = self.ReadBytes('H')
                if DEBUG:
                    print('SourceVector48bits', anAnimation.thePos.__dict__)
            aSectionOfAnimation.append(anAnimation)
            animValuePointerInputFileStreamPosition = self.data.tell()

            if (anAnimation.flags & SourceMdlAnimation.STUDIO_ANIM_ANIMROT) > 0:
                rotValuePointerInputFileStreamPosition = self.data.tell()
                anAnimation.theRotV = SourceMdlAnimationValuePointer()
                anAnimation.theRotV.animXValueOffset = self.ReadBytes('H')
                if anAnimation.theRotV.animXValueOffset == 0:
                    anAnimation.theRotV.theAnimXValues = []  # type: List[SourceMdlAnimationValue]
                anAnimation.theRotV.animYValueOffset = self.ReadBytes('H')
                if anAnimation.theRotV.animYValueOffset == 0:
                    anAnimation.theRotV.theAnimYValues = []  # type: List[SourceMdlAnimationValue]
                anAnimation.theRotV.animZValueOffset = self.ReadBytes('H')
                if anAnimation.theRotV.animZValueOffset == 0:
                    anAnimation.theRotV.theAnimZValues = []  # type: List[SourceMdlAnimationValue]
            if DEBUG:
                print('anAnimation.theRotV', anAnimation.theRotV.__dict__)
            if (anAnimation.flags & SourceMdlAnimation.STUDIO_ANIM_ANIMPOS) > 0:
                posValuePointerInputFileStreamPosition = self.data.tell()
                anAnimation.thePosV = SourceMdlAnimationValuePointer()
                anAnimation.thePosV.animXValueOffset = self.ReadShort()
                if anAnimation.thePosV.theAnimXValues != 0:
                    anAnimation.thePosV.theAnimXValues = []  # type: List[SourceMdlAnimationValue]
                anAnimation.thePosV.animYValueOffset = self.ReadShort()
                if anAnimation.thePosV.theAnimYValues != 0:
                    anAnimation.thePosV.theAnimYValues = []  # type: List[SourceMdlAnimationValue]
                anAnimation.thePosV.animZValueOffset = self.ReadShort()
                if anAnimation.thePosV.theAnimZValues != 0:
                    anAnimation.thePosV.theAnimZValues = []  # type: List[SourceMdlAnimationValue]
            if DEBUG:
                print('anAnimation.thePosV', anAnimation.thePosV.__dict__)
            sys.stderr.write('anAnimation.theRotV DEGUB ' + anAnimation.theRotV.__dict__.__str__() + '\n')
            if (anAnimation.flags & SourceMdlAnimation.STUDIO_ANIM_ANIMROT) > 0:
                if anAnimation.theRotV.animXValueOffset > 0:
                    self.ReadMdlAnimValues(
                        rotValuePointerInputFileStreamPosition + anAnimation.theRotV.animXValueOffset,
                        sectionFrameCount, anAnimation.theRotV.theAnimXValues)

                if anAnimation.theRotV.animYValueOffset > 0:
                    self.ReadMdlAnimValues(
                        rotValuePointerInputFileStreamPosition + anAnimation.theRotV.animYValueOffset,
                        sectionFrameCount, anAnimation.theRotV.theAnimYValues)

                if anAnimation.theRotV.animZValueOffset > 0:
                    self.ReadMdlAnimValues(
                        rotValuePointerInputFileStreamPosition + anAnimation.theRotV.animZValueOffset,
                        sectionFrameCount, anAnimation.theRotV.theAnimZValues)

            if (anAnimation.flags & SourceMdlAnimation.STUDIO_ANIM_ANIMPOS) > 0:
                if anAnimation.thePosV.animXValueOffset > 0:
                    self.ReadMdlAnimValues(
                        posValuePointerInputFileStreamPosition + anAnimation.theRotV.animXValueOffset,
                        sectionFrameCount, anAnimation.theRotV.theAnimXValues)

                if anAnimation.thePosV.animYValueOffset > 0:
                    self.ReadMdlAnimValues(
                        posValuePointerInputFileStreamPosition + anAnimation.theRotV.animYValueOffset,
                        sectionFrameCount, anAnimation.theRotV.theAnimYValues)

                if anAnimation.thePosV.animZValueOffset > 0:
                    self.ReadMdlAnimValues(
                        posValuePointerInputFileStreamPosition + anAnimation.theRotV.animZValueOffset,
                        sectionFrameCount, anAnimation.theRotV.theAnimZValues)

            if anAnimation.nextSourceMdlAnimationOffset == 0:
                print('DONE WITH ANIMATIONS')
                if DEBUG:
                    pprint(anAnimation.__dict__)
                break
            else:
                nextAnimationInputFileStreamPosition = animationInputFileStreamPosition + anAnimation.nextSourceMdlAnimationOffset
                if nextAnimationInputFileStreamPosition < self.data.tell():
                    print('PROBLEM! Should not be going backwards in file.')
                    # raise BufferError('PROBLEM! Should not be going backwards in file.')
                elif nextAnimationInputFileStreamPosition > self.data.tell():
                    print(
                        'PROBLEM! Should not be skipping ahead. Plugin has skipped some data, but continue decompiling')
                    # raise BufferError('PROBLEM! Should not be skipping ahead. Plugin has skipped some data, but continue decompiling')

                self.data.seek(nextAnimationInputFileStreamPosition)
            aSectionOfAnimation.append(anAnimation)
        if boneIndex != 255:
            self.ReadByte()
            self.ReadByte()
            self.ReadShort()


if __name__ == "__main__":
    DEBUG = True
    with open('log.log', "w") as f:
        with f as sys.stdout:
            A = SourceMdlFile49(r"test_data\orisa_classic.mdl")



# pprint(A.SourceMdlBone)
# pprint(A.SourceMdlBoneController)
