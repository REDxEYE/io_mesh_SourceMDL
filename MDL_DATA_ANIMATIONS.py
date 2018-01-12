from typing import List

import struct

try:
    from .ByteIO import ByteIO
    from .GLOBALS import SourceFloat16bits,SourceVector
    from .MDL_DATA import SourceMdlFileData
except:
    from ByteIO import ByteIO
    from GLOBALS import SourceFloat16bits,SourceVector
    from MDL_DATA import SourceMdlFileData

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

    def read_values(self,entry,frames,reader):
        self.read_value(entry,frames,self.theAnimXValues,self.animXValueOffset,reader)
        self.read_value(entry,frames,self.theAnimYValues,self.animYValueOffset,reader)
        self.read_value(entry,frames,self.theAnimZValues,self.animZValueOffset,reader)


    def read_value(self,entry,frames,holder,offset,reader):
        reader.seek(entry+offset)
        frameCountRemainingToBeChecked = frames
        accumulatedTotal = 0
        while frameCountRemainingToBeChecked>0:
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


    def __repr__(self):
        return "<AnimationValuePointer X pointer:{} Y pointer:{} Z pointer:{}>".format(self.animXValueOffset,
                                                                                       self.animYValueOffset,
                                                                                       self.animZValueOffset)


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
        self.theBytes = []  # type: List[bytes]

    def read(self,reader:ByteIO):
        self.theBytes = [reader.read_uint8() for _ in range(8)]

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
    STUDIO_ANIM_RAWPOS = 1
    STUDIO_ANIM_RAWROT = 2
    STUDIO_ANIM_ANIMPOS = 4
    STUDIO_ANIM_ANIMROT = 8
    STUDIO_ANIM_DELTA = 16
    STUDIO_ANIM_RAWROT2 = 32

    def __init__(self):
        self.boneIndex = 0
        self.flags = 0
        self.nextSourceMdlAnimationOffset = 0
        self.theRotV = SourceMdlAnimationValuePointer()
        self.thePosV = SourceMdlAnimationValuePointer()
        self.theRot48bits = SourceQuaternion48bits()
        self.theRot64bits = SourceQuaternion64bits()
        self.thePos = SourceVector48bits()

    def read(self,frame_count,anim_section,MDL:SourceMdlFileData,reader:ByteIO):
        anim_entry = reader.tell()
        self.boneIndex = reader.read_int8()
        if self.boneIndex == 255:
            reader.skip(3)
            return 0
        if self.boneIndex>=MDL.boneCount:
            print('Bone index out of range {} - {}'.format(self.boneIndex, MDL.boneCount))
            return 0
        self.flags = reader.read_uint8()
        self.nextSourceMdlAnimationOffset = reader.read_int16()
        if (self.flags & self.STUDIO_ANIM_RAWROT2)>0:
            self.theRot64bits.read(reader)

        if (self.flags & self.STUDIO_ANIM_RAWROT)>0:
            self.theRot48bits.read(reader)

        if (self.flags & self.STUDIO_ANIM_RAWPOS)>0:
            self.thePos.read(reader)

        entry = reader.tell()

        if (self.flags & self.STUDIO_ANIM_ANIMROT)>0:
            rotV_entry = reader.tell()
            self.theRotV.read(reader)
            if self.theRotV.animXValueOffset!=0 and self.theRotV.animYValueOffset!=0 and self.theRotV.animZValueOffset!=0:
                self.theRotV.read_values(rotV_entry,frame_count,reader)


        if (self.flags & self.STUDIO_ANIM_ANIMPOS)>0:
            posV_entry = reader.tell()
            self.thePosV.read(reader)
            if self.thePosV.animXValueOffset!=0 and self.thePosV.animYValueOffset!=0 and self.thePosV.animZValueOffset!=0:
                self.thePosV.read_values(posV_entry,frame_count,reader)

        if self.nextSourceMdlAnimationOffset == 0:
            print('DONE WITH ANIMATIONS')
            return 1
        else:
            nextAnimationInputFileStreamPosition = anim_entry + self.nextSourceMdlAnimationOffset
            if nextAnimationInputFileStreamPosition < reader.tell():
                print('PROBLEM! Should not be going backwards in file.')
                # raise BufferError('PROBLEM! Should not be going backwards in file.')
            elif nextAnimationInputFileStreamPosition > reader.tell():
                print(
                    'PROBLEM! Should not be skipping ahead. Plugin has skipped some data, but continue decompiling')
                # raise BufferError('PROBLEM! Should not be skipping ahead. Plugin has skipped some data, but continue decompiling')

            reader.seek(nextAnimationInputFileStreamPosition)


        anim_section.append(self)


        return self,1

class BoneConstantInfo:
    def __init__(self):
        self.theConstantRawPos = SourceVector48bits()
        self.theConstantRawRot = SourceQuaternion48bits()

    def read(self,reader:ByteIO):
        self.theConstantRawPos.read(reader)
        self.theConstantRawRot.read(reader)

    def __repr__(self):
        return "<BoneConstantInfo constant pos:{} constant rot:{}>".format(self.theConstantRawPos,self.theConstantRawRot)

class BoneFrameDataInfo:
    def __init__(self):
        self.theAnimPosition = SourceVector48bits()
        self.theAnimRotation = SourceQuaternion48bits()
        self.theFullAnimPosition = SourceVector()
        self.theFullAnimUnknown01 = 0
        self.theFullAnimUnknown02 = SourceQuaternion64bits()


    def __repr__(self):
        return "<BoneFrameDataInfo anim position:{} anim rotation:{} Full Anim Position:{}>".format(self.theAnimPosition,self.theAnimRotation,self.theFullAnimPosition)

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
        return "<AniFrameAnim frame offset:{} constant offset:{}>".format(self.frameOffset,self.constantsOffset)

class SourceMdlMovement:
    def __init__(self):
        self.endframeIndex = 0
        self.motionFlags = 0
        self.v0 = 0.0
        self.v1 = 0.0
        self.angle = 0.0
        self.vector = SourceVector()
        self.position = SourceVector()

    def __repr__(self):
        return "<Movement angle:{} vector:{} position:{}>".format(self.angle,self.vector,self.position)


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

    def __init__(self):
        self._valid = 0
        self._total = 1

        self.value = 0



    @property
    def valid(self):
        a = struct.pack('h',self.value)
        return struct.unpack('B',bytes(a))[0]

    @property
    def total(self):
        a = struct.pack('h', self.value)
        return struct.unpack('B',bytes(a[0]))[0]


    def __repr__(self):
        return "<AnimationValue value:{} valid:{} total:{}>".format(self.value,self.valid,self.total)


class SourceMdlCompressedIkError:
    def __init__(self):
        self.scale = []  # len 6
        self.offset = []  # len 6
        self.theAnimValues = []  # type: List[SourceMdlAnimationValue]



    def __repr__(self):
        return "<CompressedIkError scale:{} anim values:{}>".format(self.scale,self.theAnimValues)

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

    def __repr__(self):
        return "<LocalHierarchy bone index:{}>".format(self.boneIndex)

class SourceMdlAnimationSection:
    def __init__(self):
        self.animBlock = 0
        self.animOffset = 0


    def __repr__(self):
        return "<AnimationSection anim Block:{} anim offset:{}>".format(self.animBlock,self.animOffset)



class SourceMdlAnimationDescBase:
    def __init__(self):
        self.theName = ''

    def __repr__(self):
        return "<AnimationDesc name:{}>".format(self.theName)

class SourceMdlIkRule:
    pass


class SourceMdlAnimationDesc49(SourceMdlAnimationDescBase):
    STUDIO_LOOPING = 1
    STUDIO_SNAP = 2
    STUDIO_DELTA = 4
    STUDIO_AUTOPLAY = 8
    STUDIO_POST = 16
    STUDIO_ALLZEROS = 32
    STUDIO_FRAMEANIM = 64
    STUDIO_CYCLEPOSE = 128
    STUDIO_REALTIME = 256
    STUDIO_LOCAL = 512
    STUDIO_HIDDEN = 1024
    STUDIO_OVERRIDE = 2048
    STUDIO_ACTIVITY = 4096
    STUDIO_EVENT = 8192
    STUDIO_WORLD = 16384
    STUDIO_NOFORCELOOP = 32768
    STUDIO_EVENT_CLIENT = 65536

    def __init__(self):
        super().__init__()
        self.baseHeaderOffset = 0
        self.nameOffset = 0
        self.fps = 0.0
        self.flags = 0
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

    def read(self, reader: ByteIO):
        pass
    def __repr__(self):
        return "<AnimationDesc49 name:{}>".format(self.theName)
