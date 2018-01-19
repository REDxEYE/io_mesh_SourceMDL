from enum import Enum
from pprint import pprint
from typing import List

import struct

import math

try:
    from .ByteIO import ByteIO
    from .GLOBALS import SourceFloat16bits, SourceVector
    from .MDL_DATA import *
except:
    from ByteIO import ByteIO
    from GLOBALS import SourceFloat16bits, SourceVector
    from MDL_DATA import *


class SourceMdlAnimationValuePointer:
    """"FROM: SourceEngine2006_source\public\studio.h
    struct mstudioanim_valueptr_t
    {
       short	offset[3];
       inline mstudioanimvalue_t *pAnimvalue( int i ) const { if (offset[i] > 0) return
         (mstudioanimvalue_t *)(((byte *)this) + offset[i]); else return NULL; };
    };"""

    def __init__(self):
        self.animXValueOffset = 0
        self.animYValueOffset = 0
        self.animZValueOffset = 0

        self.theAnimXValues = []
        self.theAnimYValues = []
        self.theAnimZValues = []

    def read(self, reader: ByteIO):
        self.animXValueOffset = reader.read_int16()
        self.animYValueOffset = reader.read_int16()
        self.animZValueOffset = reader.read_int16()

    def read_values(self, entry, frames, reader):
        with reader.save_current_pos():
            if self.animXValueOffset > 0:
                self.read_value(entry, frames, self.theAnimXValues, self.animXValueOffset, reader)
            if self.animYValueOffset > 0:
                self.read_value(entry, frames, self.theAnimYValues, self.animYValueOffset, reader)
            if self.animZValueOffset > 0:
                self.read_value(entry, frames, self.theAnimZValues, self.animZValueOffset, reader)
                # print(self)

    def read_value(self, entry, frames, holder, offset, reader):
        reader.seek(entry + offset)
        frameCountRemainingToBeChecked = frames
        accumulatedTotal = 0
        while frameCountRemainingToBeChecked > 0:
            value = SourceMdlAnimationValue()
            value.value = reader.read_int16()
            currentTotal = value.total
            accumulatedTotal += currentTotal
            if currentTotal == 0:
                print('BAD IF THIS REACHED')
                break
            frameCountRemainingToBeChecked -= currentTotal
            holder.append(value)
            validCount = value.valid
            for i in range(validCount):
                value = SourceMdlAnimationValue()
                value.value = reader.read_int16()
                holder.append(value)

    def __repr__(self):  # X:{0.theAnimXValues} Y:{0.theAnimYValues} Z:{0.theAnimZValues}
        return "<AnimationValuePointer X off:{0.animXValueOffset} Y off:{0.animYValueOffset} Z off:{0.animZValueOffset}>".format(
            self)


class SourceQuaternion48bits(object):
    def __init__(self):
        self.theXInput = SourceFloat16bits()
        self.theYInput = SourceFloat16bits()
        self.theZWInput = SourceFloat16bits()

    def read(self, reader: ByteIO):
        self.theXInput.read(reader)
        self.theYInput.read(reader)
        self.theZWInput.read(reader)

    def __repr__(self):
        return '<Quaternion X: {} Y: {} Z: {}>'.format(self.theXInput.TheFloatValue, self.theYInput.TheFloatValue,
                                                       self.theZWInput.TheFloatValue)


class SourceQuaternion64bits(object):
    def __init__(self):
        self.theBytes = []  # type: List[int]

    def read(self, reader: ByteIO):
        self.theBytes = [reader.read_uint8() for _ in range(8)]

    @property
    def x(self):
        byte0 = (self.theBytes[0] & 0xFF)
        byte1 = (self.theBytes[1] & 0xFF) << 8
        byte2 = (self.theBytes[2] & 0x1F) << 16

        bitsResult = IntegerAndSingleUnion(byte2|byte1|byte0)
        return (bitsResult.i - 1048576) * (1 / 1048576.5)

    @property
    def y(self):
        byte2 = (self.theBytes[2] & 0xE0) >> 5
        byte3 = (self.theBytes[3] & 0xFF) << 3
        byte4 = (self.theBytes[4] & 0xFF) << 11
        byte5 = (self.theBytes[5] & 0x3) >> 19
        bitsResult = IntegerAndSingleUnion(byte5|byte4|byte3|byte2)
        return (bitsResult.i -1048576) * (1 / 1048576.5)

    @property
    def z(self):
        byte5 = (self.theBytes[5] & 0xFC) >> 2
        byte6 = (self.theBytes[6] & 0xFF) << 6
        byte7 = (self.theBytes[7] & 0x7F) << 14

        bitsResult = IntegerAndSingleUnion(byte7|byte6|byte5)
        return (bitsResult.i -1048576) * (1 / 1048576.5)

    @property
    def wneg(self):
        return -1 if self.theBytes[7]&0x80 > 0 else 1

    @property
    def w(self):
        print(1-self.x**2-self.y**2-self.z**2)
        return math.sqrt(1-(self.x**2)-(self.y**2)-(self.z**2))*self.wneg

    @property
    def as_4D_vec(self):
        return [self.x,self.y,self.z,self.w]

    def r2d(self,val):
        cos_a = self.w
        angle = math.acos(cos_a)*2
        sin_a = math.sqrt(1-cos_a**2)
        if math.fabs(sin_a)<0.000005:sin_a = 1
        return val/sin_a

    @property
    def xd(self):
        return self.r2d(self.x)
    @property
    def yd(self):
        return self.r2d(self.y)
    @property
    def zd(self):
        return self.r2d(self.z)

    @property
    def as_3D_vec(self):
        return [self.xd,self.yd,self.zd]

    def __repr__(self):
        return "<Quaternion64 X:{0.xd} Y:{0.yd} Z:{0.zd}>".format(self)

class IntegerAndSingleUnion:

    def __init__(self,i):
        self.i = i

    @property
    def s(self):
        return struct.unpack('f',struct.pack('i',self.i))

class SourceVector48bits:
    def __init__(self):
        self.theXInput = SourceFloat16bits()
        self.theYInput = SourceFloat16bits()
        self.theZInput = SourceFloat16bits()

    def read(self, reader: ByteIO):
        self.theXInput.read(reader)
        self.theYInput.read(reader)
        self.theZInput.read(reader)

    def __repr__(self):
        return '<Vector X: {} Y: {} Z: {}>'.format(self.theXInput.TheFloatValue, self.theYInput.TheFloatValue,
                                                   self.theZInput.TheFloatValue)


class SourceMdlAnimation:
    class STUDIO_ANIM:
        RAWPOS = 1
        RAWROT = 2
        ANIMPOS = 4
        ANIMROT = 8
        DELTA = 16
        RAWROT2 = 32

        @classmethod
        def get_flags(cls, flag):
            flags = []
            for name, val in vars(cls).items():
                if name.isupper():
                    if (flag & val) > 0:
                        flags.append(name)
            return flags

    def __init__(self):
        self.boneIndex = 0
        self.flags = 0
        self.nextSourceMdlAnimationOffset = 0
        self.theRotV = SourceMdlAnimationValuePointer()
        self.thePosV = SourceMdlAnimationValuePointer()
        self.theRot48bits = SourceQuaternion48bits()
        self.theRot64bits = SourceQuaternion64bits()
        self.thePos = SourceVector48bits()

    def read(self, frame_count, anim_section, mdl: SourceMdlFileData, reader: ByteIO):
        anim_entry = reader.tell()
        self.boneIndex = reader.read_int8()
        print('BoneIndex:',self.boneIndex)
        if self.boneIndex == 255:
            reader.skip(3)
            return self, 0
        if self.boneIndex >= mdl.boneCount:
            print('Bone index out of range {} - {}'.format(self.boneIndex, mdl.boneCount))
            return self, 0
        self.flags = reader.read_uint8()
        self.sflags = self.STUDIO_ANIM.get_flags(self.flags)
        self.nextSourceMdlAnimationOffset = reader.read_int16()
        pdata = reader.tell()
        if (self.flags & self.STUDIO_ANIM.RAWROT2) > 0:
            with reader.save_current_pos():
                self.theRot64bits.read(reader)

        if (self.flags & self.STUDIO_ANIM.RAWROT) > 0:
            with reader.save_current_pos():
                self.theRot48bits.read(reader)

        if (self.flags & self.STUDIO_ANIM.RAWPOS) > 0:
            with reader.save_current_pos():
                self.thePos.read(reader)

        if (self.flags & self.STUDIO_ANIM.ANIMROT) > 0:
            rotV_entry = reader.tell()
            reader.seek(pdata)
            self.theRotV.read(reader)
            self.theRotV.read_values(rotV_entry, frame_count, reader)

        if (self.flags & self.STUDIO_ANIM.ANIMPOS) > 0:
            reader.seek((self.flags & self.STUDIO_ANIM.ANIMPOS) + pdata)
            posV_entry = reader.tell()
            self.thePosV.read(reader)
            self.thePosV.read_values(posV_entry, frame_count, reader)
        pprint(self.__dict__)
        if self.nextSourceMdlAnimationOffset == 0:
            print('DONE WITH ANIMATIONS')
            return self, 1
        else:
            nextAnimationInputFileStreamPosition = anim_entry + self.nextSourceMdlAnimationOffset
            if nextAnimationInputFileStreamPosition < reader.tell():
                print('PROBLEM! Should not be going backwards in file.')
                # raise BufferError('PROBLEM! Should not be going backwards in file.')
            reader.seek(nextAnimationInputFileStreamPosition)

        anim_section.append(self)

        return self, 1

    def __repr__(self):
        return "<Animation bone index:{0.boneIndex} flags:{0.sflags} thePosV:{0.thePosV} theRotV:{0.theRotV} >".format(
            self)


class BoneConstantInfo:
    def __init__(self):
        self.theConstantRawPos = SourceVector48bits()
        self.theConstantRawRot = SourceQuaternion48bits()

    def read(self, reader: ByteIO):
        self.theConstantRawPos.read(reader)
        self.theConstantRawRot.read(reader)

    def __repr__(self):
        return "<BoneConstantInfo constant pos:{} constant rot:{}>".format(self.theConstantRawPos,
                                                                           self.theConstantRawRot)


class BoneFrameDataInfo:
    def __init__(self):
        self.theAnimPosition = SourceVector48bits()
        self.theAnimRotation = SourceQuaternion48bits()
        self.theFullAnimPosition = SourceVector()
        self.theFullAnimUnknown01 = 0
        self.theFullAnimUnknown02 = SourceQuaternion64bits()

    def __repr__(self):
        return "<BoneFrameDataInfo anim position:{} anim rotation:{} Full Anim Position:{}>".format(
            self.theAnimPosition, self.theAnimRotation, self.theFullAnimPosition)


class SourceAniFrameAnim:
    STUDIO_FRAME_RAWPOS = 1
    STUDIO_FRAME_RAWROT = 2
    STUDIO_FRAME_ANIMPOS = 4
    STUDIO_FRAME_ANIMROT = 8
    STUDIO_FRAME_FULLANIMPOS = 16
    STUDIO_FRAME_UNKNOWN01 = 64
    STUDIO_FRAME_UNKNOWN02 = 128

    def __init__(self):
        self.constantsOffset = 0
        self.frameOffset = 0
        self.unused = []
        self.theBoneFlags = []
        self.theBoneConstantInfos = []  # type: List[BoneConstantInfo]
        self.theBoneFrameDataInfos = []  # type: List[BoneFrameDataInfo]

    def __repr__(self):
        return "<AniFrameAnim frame offset:{} constant offset:{}>".format(self.frameOffset, self.constantsOffset)


class SourceMdlMovement:
    def __init__(self):
        self.endframeIndex = 0
        self.motionFlags = 0
        self.v0 = 0.0
        self.v1 = 0.0
        self.angle = 0.0
        self.vector = SourceVector()
        self.position = SourceVector()

    def read(self, reader: ByteIO):
        self.endframeIndex = reader.read_uint32()
        self.motionFlags = reader.read_uint32()
        self.v0 = reader.read_float()
        self.v1 = reader.read_float()
        self.angle = reader.read_float()
        self.vector.read(reader)
        self.position.read(reader)
        return self

    def __repr__(self):
        return "<Movement angle:{} vector:{} position:{}>".format(self.angle, self.vector, self.position)


class SourceMdlAnimationValue:
    """"FROM: SourceEngine2006_source\public\studio.h
    // animation frames
    union mstudioanimvalue_t
    {
        struct
        {
          byte	valid;
          byte	total;
        } num;
        short		value;
    };"""

    def __init__(self, value=0):
        self._valid = 0
        self._total = 1

        self.value = value

    @property
    def valid(self):
        a = struct.pack('h', self.value)
        _, ret = struct.unpack('BB', a)
        return ret

    @property
    def total(self):
        a = struct.pack('h', self.value)
        ret, _ = struct.unpack('BB', a)
        return ret

    def __repr__(self):
        return "<AnimationValue value:{} valid:{} total:{}>".format(self.value, self.valid, self.total)


class SourceMdlCompressedIkError:
    def __init__(self):
        self.scale = []  # len 6
        self.offset = []  # len 6
        self.theAnimValues = []  # type: List[SourceMdlAnimationValue]

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.scale = [reader.read_uint32() for _ in range(6)]
        self.offset = [reader.read_uint32() for _ in range(6)]
        for offset in self.offset:
            with reader.save_current_pos():
                reader.seek(entry + offset)
                self.theAnimValues.append(SourceMdlAnimationValue(reader.read_uint16()))
        return self

    def __repr__(self):
        return "<CompressedIkError scale:{} anim values:{}>".format(self.scale, self.theAnimValues)


class SourceMdlLocalHierarchy:
    def __init__(self):
        self.boneIndex = 0
        self.boneNewParentIndex = 0
        self.startInfluence = 0.0
        self.peakInfluence = 0.0
        self.tailInfluence = 0.0
        self.endInfluence = 0.0
        self.startFrameIndex = 0
        self.localAnimOffset = 0
        self.unused = []  # len 4
        self.theLocalAnims = SourceMdlCompressedIkError()

    def read(self, reader: ByteIO):
        entry = reader.tell()
        self.boneIndex = reader.read_uint32()
        self.boneNewParentIndex = reader.read_uint32()
        self.startInfluence = reader.read_float()
        self.peakInfluence = reader.read_float()
        self.tailInfluence = reader.read_float()
        self.endInfluence = reader.read_float()
        self.startFrameIndex = reader.read_uint32()
        self.localAnimOffset = reader.read_uint32()

        if self.localAnimOffset != 0:
            with reader.save_current_pos():
                reader.seek(entry + self.localAnimOffset)
                self.theLocalAnims.read(reader)

        self.unused = [reader.read_uint32() for _ in range(4)]
        return self

    def __repr__(self):
        return "<LocalHierarchy bone index:{}>".format(self.boneIndex)


class SourceMdlAnimationSection:
    def __init__(self):
        self.animBlock = 0
        self.animOffset = 0

    def read(self, reader: ByteIO):
        self.animBlock = reader.read_uint32()
        self.animOffset = reader.read_uint32()
        return self

    def __repr__(self):
        return "<AnimationSection anim Block:{} anim offset:{}>".format(self.animBlock, self.animOffset)


class SourceMdlAnimationDescBase:
    def __init__(self):
        self.theName = ''

    def __repr__(self):
        return "<AnimationDesc name:{}>".format(self.theName)


class SourceMdlIkRule:
    pass


class SourceMdlAnimationDesc49(SourceMdlAnimationDescBase):

    class STUDIO:
        LOOPING = 1
        SNAP = 2
        DELTA = 4
        AUTOPLAY = 8
        POST = 16
        ALLZEROS = 32
        FRAMEANIM = 64
        CYCLEPOSE = 128
        REALTIME = 256
        LOCAL = 512
        HIDDEN = 1024
        OVERRIDE = 2048
        ACTIVITY = 4096
        EVENT = 8192
        WORLD = 16384
        NOFORCELOOP = 32768
        EVENT_CLIENT = 65536

        def __init__(self,flag):
            self.flag = flag

        def __contains__(self, item):
            return (self.flag&item)>0
        @property
        def get_flags(self):
            flags = []
            for name, val in vars(self.__class__).items():
                if name.isupper():
                    if (self.flag & val) > 0:
                        flags.append(name)
            return flags

        def __repr__(self):
            return "<Flags value:{0.flag}  {0.get_flags}>".format(self)


    def __init__(self):
        super().__init__()
        self.baseHeaderOffset = 0
        self.nameOffset = 0
        self.fps = 0.0
        self.flags = self.STUDIO
        self.frameCount = 0
        self.movementCount = 0
        self.movementOffset = 0
        self.ikRuleZeroFrameOffset = 0
        self.unused1 = []  # 5 ints
        self.animBlock = 0
        self.animOffset = 0
        self.ikRuleCount = 0
        self.ikRuleOffset = 0
        self.animblockIkRuleOffset = 0
        self.localHierarchyCount = 0
        self.localHierarchyOffset = 0
        self.sectionOffset = 0
        self.sectionFrameCount = 0
        self.spanFrameCount = 0
        self.spanCount = 0
        self.spanOffset = 0
        self.spanStallTime = 0.0
        self.theSectionsOfAnimations = []  # type: List[List[SourceMdlAnimation]]
        self.theAniFrameAnim = SourceAniFrameAnim()
        self.theIkRules = SourceMdlIkRule()
        self.theSections = []  # type: List[SourceMdlAnimationSection]
        self.theMovements = []  # type: List[SourceMdlMovement]
        self.theLocalHierarchies = []  # type: List[SourceMdlLocalHierarchy]
        self.theAnimIsLinkedToSequence = False
        self.theLinkedSequences = False
        self.size = 100
        self.fileOffsetStart2 = -1
        self.fileOffsetEnd2 = -1
        self.entry = -1

    def read(self, reader: ByteIO, MDL: SourceMdlFileData):
        entry = reader.tell()
        self.entry = entry
        self.baseHeaderOffset = reader.read_int32()
        self.nameOffset = reader.read_int32()
        self.theName = reader.read_from_offset(entry + self.nameOffset, reader.read_ascii_string)
        self.fps = reader.read_float()
        self.flags = self.STUDIO(reader.read_uint32())
        self.frameCount = reader.read_uint32()
        self.movementCount = reader.read_uint32()
        self.movementOffset = reader.read_uint32()

        # if self.movementCount > 0:
        #     with reader.save_current_pos():
        #         reader.seek(entry + self.movementCount)
        #         self.theMovements.append(SourceMdlMovement().read(reader))

        self.unused1 = [reader.read_uint32() for _ in range(6)]
        self.animBlock = reader.read_uint32()
        self.animOffset = reader.read_uint32()
        # sectionCount = math.trunc(self.frameCount / self.sectionFrameCount) + 2
        # if self.animBlock == 0:
        #     for section_index in range(sectionCount):
        # if self.animOffset != 0:
        #     with reader.save_current_pos():
        #         reader.seek(entry + self.animOffset)
        #         ret, stat = SourceMdlAnimation().read(self.frameCount, self.theSectionsOfAnimations, MDL, reader)

        self.ikRuleCount = reader.read_uint32()
        self.ikRuleOffset = reader.read_uint32()
        self.animblockIkRuleOffset = reader.read_uint32()
        self.localHierarchyCount = reader.read_uint32()
        self.localHierarchyOffset = reader.read_uint32()

        # if self.localHierarchyCount > 0:
        #     with reader.save_current_pos():
        #         reader.seek(entry + self.localHierarchyOffset)
        #         self.theLocalHierarchies.append(SourceMdlLocalHierarchy().read(reader))

        self.sectionOffset = reader.read_uint32()
        self.sectionFrameCount = reader.read_uint32()

        # if self.sectionFrameCount != 0:
        #     with reader.save_current_pos():
        #         reader.seek(entry + self.sectionOffset)
        #         self.theSections.append(SourceMdlAnimationSection().read(reader))

        self.spanFrameCount = reader.read_uint16()
        self.spanCount = reader.read_uint16()
        self.spanOffset = reader.read_uint32()
        self.spanStallTime = reader.read_float()
        self.fileOffsetStart2 = entry + self.spanOffset
        self.fileOffsetEnd2 = entry + self.spanOffset-1
        if self.spanFrameCount!=0 or self.spanCount!=0 or self.spanOffset!=0 or self.spanStallTime!=0:
            for bone_index in range(len(MDL.theBones)):
                bone = MDL.theBones[bone_index] #type: SourceMdlBone
                if bone.flags & SourceMdlBone.BONE_HAS_SAVEFRAME_POS:
                    self.fileOffsetEnd2 += self.spanCount * 6
                if bone.flags & SourceMdlBone.BONE_HAS_SAVEFRAME_ROT:
                    self.fileOffsetEnd2 += self.spanCount * 8




        return self

    def __repr__(self):
        return "<AnimationDesc49 name:{0.theName} fps:{0.fps} frames:{0.frameCount} sectionFrameCount count:{0.sectionFrameCount}>".format(
            self)
