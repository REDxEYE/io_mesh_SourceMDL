from _ast import Bytes
from pprint import pformat
from typing import List

try:
    from .GLOBALS import *
except Exception:
    from GLOBALS import *

MAX_NUM_LODS  = 8
MAX_NUM_BONES_PER_VERT = 3

class SourceMdlAnimationDesc:
    def __init__(self):
        self.theName = ''


class SourceMdlFileData:
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

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlBoneController:
    def __init__(self):
        self.boneIndex = 0
        self.type = 0
        self.startBlah = 0
        self.endBlah = 0
        self.restIndex = 0
        self.inputField = 0
        self.unused = []

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlMeshVertexData:
    def __init__(self):
        self.modelVertexDataP = 0
        self.lodVertexCount = []

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlModelGroup:
    def __init__(self):
        self.labelOffset = 0
        self.fileNameOffset = 0
        self.theLabel = 0
        self.theFileName = 0
        self.theMdlFileData = SourceMdlFileData()

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlModelVertexData:
    def __init__(self):
        self.vertexDataP = 0
        self.tangentDataP = 0
    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

class SourceMdlBodyPart:
    def __init__(self):
        self.nameOffset = 0
        self.modelCount = 0
        self.base = 0
        self.modelOffset = 0
        self.theName = ""
        self.theModels = []

    def __repr__(self):
        return "<BodyPart name:{} model count:{} actual:{} models:{}>".format(self.theName, self.modelCount,len(self.theModels), self.theModels)

class SourceMdlHitboxSet:
    def __init__(self):
        self.nameOffset = 0
        self.hitboxCount = 0
        self.hitboxOffset = 0

        self.theName = ""
        self.theHitboxes = []

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlHitbox:
    def __init__(self):
        self.boneIndex = 0
        self.groupIndex = 0
        self.boundingBoxMin = SourceVector()
        self.boundingBoxMax = SourceVector()
        self.nameOffset = 0
        self.unused = []
        self.boundingBoxPitchYawRoll = SourceVector()
        self.unused_VERSION49 = 0
        self.theName = ""

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

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlQuatInterpBone:
    def __init__(self):
        self.controlBoneIndex = 0
        self.triggerCount = 0
        self.triggerOffset = 0
        self.theTriggers = []

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlJiggleBone:
    def __init__(self):
        self.flag_offset = 0
        self.flags = 0
        self.length = 0.0
        self.length_offset = 0.0
        self.tipMass = 0.0
        self.tipMass_offset = 0.0

        self.yawStiffness = 0.0
        self.yawStiffness_offset = 0.0
        self.yawDamping = 0.0
        self.yawDamping_offset = 0.0
        self.pitchStiffness = 0.0
        self.pitchStiffness_offset = 0.0
        self.pitchDamping = 0.0
        self.pitchDamping_offset = 0.0
        self.alongStiffness = 0.0
        self.alongStiffness_offset = 0.0
        self.alongDamping = 0.0
        self.alongDamping_offset = 0.0

        self.angleLimit = 0.0
        self.angleLimit_offset = 0.0

        self.minYaw = 0.0
        self.minYaw_offset = 0.0
        self.maxYaw = 0.0
        self.maxYaw_offset = 0.0
        self.yawFriction = 0.0
        self.yawFriction_offset = 0.0
        self.yawBounce = 0.0
        self.yawBounce_offset = 0.0

        self.minPitch = 0.0
        self.minPitch_offset = 0.0
        self.maxPitch = 0.0
        self.maxPitch_offset = 0.0
        self.pitchFriction_offset = 0.0
        self.pitchBounce = 0.0
        self.pitchBounce_offset = 0.0

        self.baseMass = 0.0
        self.baseMass_offset = 0.0
        self.baseStiffness = 0.0
        self.baseStiffness_offset = 0.0
        self.baseDamping = 0.0
        self.baseDamping_offset = 0.0
        self.baseMinLeft = 0.0
        self.baseMinLeft_offset = 0.0
        self.baseMaxLeft = 0.0
        self.baseMaxLeft_offset = 0.0
        self.baseLeftFriction = 0.0
        self.baseLeftFriction_offset = 0.0
        self.baseMinUp = 0.0
        self.baseMinUp_offset = 0.0
        self.baseMaxUp = 0.0
        self.baseMaxUp_offset = 0.0
        self.baseUpFriction = 0.0
        self.baseUpFriction_offset = 0.0
        self.baseMinForward = 0.0
        self.baseMinForward_offset = 0.0
        self.baseMaxForward = 0.0
        self.baseMaxForward_offset = 0.0
        self.baseForwardFriction = 0.0
        self.baseForwardFriction_offset = 0.0

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlBone:
    def __init__(self):
        self.boneOffset = 0
        self.name = []
        self.nameOffset = 0
        self.parentBoneIndex = 0
        self.boneControllerIndex = []
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
    def __repr__(self):
        return "<Bone {} pos:{} rot: {}>".format(self.name, self.position.as_string, self.rotation.as_string)

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

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

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

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return self.__str__()
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
        print('valid',a)
        return struct.unpack('B',bytes(a))[0]

    @property
    def total(self):
        a = struct.pack('h', self.value)
        print('total', bytes(a[0]))
        return struct.unpack('B',bytes(a[0]))[0]

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

class SourceMdlQuatInterpBoneInfo:
    def __init__(self):
        self.inverseToleranceAngle = 0
        self.trigger = SourceQuaternion
        self.pos = SourceVector()
        self.quat = SourceQuaternion


class SourceMdlAttachment:
    def __init__(self):
        self.name = ""
        self.type = 0
        self.bone = 0
        self.attachmentPoint = SourceVector()
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

        self.theName = ''

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

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

    def __repr__(self):
        return "<Model name:{} type:{} mesh count:{} actual:{} meshes:{} eyeballs:{}>".format(self.name, self.type,
                                                                                    self.meshCount,len(self.theMeshes),
                                                                                    self.theMeshes, self.theEyeballs)


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
        self.unused3 = []
        self.unused4 = []

        self.theName = ''
        self.theTextureIndex = 0

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

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

    def __repr__(self):
        return "<Mesh material index:{} vertex count:{} flex count:{} flexes:{}>".format(self.materialIndex,
                                                                                         self.vertexCount,
                                                                                         self.flexCount, self.theFlexes)


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

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

class FlexFrame:
    def __init__(self):
        self.flexName = ''
        self.flexDescription = ''
        self.flexHasParner = False
        self.flexSplit = 0.0
        self.bodyAndMeshVertexIndexStarts = [] # type List[int]
        self.flexes = [] # type List[SourceMdlFlex]
        self.meshIndexes = [] # type List[int]



    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlVertAnim:
    VertAnimFixedPointScale = 1/4096

    def __init__(self):
        self.index = 0
        self.speed = 0
        self.side = 0
        self.theDelta = []  # 3
        self.theNDelta = []  # 3

    def __str__(self):
        return pformat(self.__dict__)
    def __repr__(self):
        return pformat(self.__dict__)

class SourceMdlVertAnimWrinkle(SourceMdlVertAnim):
    def __init__(self):
        super().__init__()
        self.wrinkleDelta = 0

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

class SourceMdlFlexDesc:
    def __init__(self):
        self.nameOffset = 0
        self.theName = ''
        self.theDescIsUsedByFlex = False
        self.theDescIsUsedByFlexRule = False
        self.theDescIsUsedByEyelid = False

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlFlexController:
    def __init__(self):
        self.typeOffset = 0
        self.nameOffset = 0
        self.localToGlobal = 0
        self.min = 0.0
        self.max = 0.0
        self.theName = ''
        self.theType = ''

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

class SourceMdlFlexRule:
    def __init__(self):
        self.flexIndex = 0
        self.opCount = 0
        self.opOffset = 0
        self.theFlexOps = []

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

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlAnimationDescBase:
    def __init__(self):
        self.theName = ''

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
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
        self.unused1 = [None]*5  # type: List[int]*5
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
        self.theMovements = [] #type: List[SourceMdlMovement]
        self.theLocalHierarchies = [] #type: List[SourceMdlLocalHierarchy]
        self.theAnimIsLinkedToSequence = False
        self.theLinkedSequences = False

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

class BoneConstantInfo:
    def __init__(self):
        self.theConstantRawPos = SourceVector48bits()
        self.theConstantRawRot = SourceQuaternion48bits()

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

class BoneFrameDataInfo:
    def __init__(self):
        self.theAnimPosition = SourceVector48bits()
        self.theAnimRotation = SourceQuaternion48bits()
        self.theFullAnimPosition = SourceVector()
        self.theFullAnimUnknown01 = 0
        self.theFullAnimUnknown02 = SourceQuaternion64bits()

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)

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

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlIkRule:
    pass


class SourceMdlMovement:
    def __init__(self):
        self.endframeIndex = 0
        self.motionFlags = 0
        self.v0 = 0.0
        self.v1 = 0.0
        self.angle = 0.0
        self.vector = SourceVector()
        self.position = SourceVector()

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlCompressedIkError:
    def __init__(self):
        self.scale = []  # len 6
        self.offset = []  # len 6
        self.theAnimValues = []  # type: List[SourceMdlAnimationValue]

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
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

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceMdlAnimationSection:
    def __init__(self):
        self.animBlock = 0
        self.animOffset = 0

    def __str__(self):
        return pformat(self.__dict__)

    def __repr__(self):
        return pformat(self.__dict__)
class SourceQuaternion48bits(object):
    def __init__(self):
        self.theXInput = SourceFloat16bits()
        self.theYInput = SourceFloat16bits()
        self.theZWInput = SourceFloat16bits()

    def __str__(self):
        return 'Quaternion X: {} Y: {} Z: {}'.format(self.theXInput.TheFloatValue, self.theYInput.TheFloatValue, self.theZWInput.TheFloatValue)
    def __repr__(self):
        return self.__str__()

class SourceQuaternion64bits(object):
    def __init__(self):
        self.theBytes = []  # type: List[bytes]


class SourceVector48bits:
    def __init__(self):
        self.theXInput = SourceFloat16bits()
        self.theYInput = SourceFloat16bits()
        self.theZInput = SourceFloat16bits()

    def __str__(self):
        return 'Vector X: {} Y: {} Z: {}'.format(self.theXInput.TheFloatValue, self.theYInput.TheFloatValue, self.theZInput.TheFloatValue)
    def __repr__(self):
        return self.__str__()

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


class SourceMdlEvent:
    NEW_EVENT_STYLE = 1024

    def __init__(self):
        self.cycle = 0.0
        self.eventIndex = 0
        self.eventType = 0
        self.options = []  # len 64
        self.nameOffset = 0
        self.theName = ''


class SourceMdlAutoLayer:
    STUDIO_AL_SPLINE = 64
    STUDIO_AL_XFADE = 128
    STUDIO_AL_NOBLEND = 512
    STUDIO_AL_LOCAL = 4096
    STUDIO_AL_POSE = 16384

    def __init__(self):
        self.sequenceIndex = 0
        self.poseIndex = 0
        self.flags = 0
        self.influenceStart = 0.0
        self.influencePeak = 0.0
        self.influenceTail = 0.0
        self.influenceEnd = 0.0


class SourceMdlIkLock:
    pass


class SourceMdlActivityModifier:
    def __init__(self):
        self.nameOffset = 0
        self.theName = 0


class SourceMdlSequenceDesc:
    def __init__(self):
        self.theWeightListIndex = -1
        self.baseHeaderOffset = 0
        self.nameOffset = 0
        self.activityNameOffset = 0
        self.flags = 0
        self.activity = 0
        self.activityWeight = 0
        self.eventCount = 0
        self.eventOffset = 0
        self.bbMin = SourceVector()
        self.bbMax = SourceVector()
        self.blendCount = 0
        self.animIndexOffset = 0
        self.movementIndex = 0
        self.groupSize = []
        self.paramIndex = []
        self.paramStart = []
        self.paramEnd = []
        self.paramParent = 0
        self.fadeInTime = 0
        self.fadeOutTime = 0
        self.localEntryNodeIndex = 0
        self.localExitNodeIndex = 0
        self.nodeFlags = 0
        self.entryPhase = 0
        self.exitPhase = 0
        self.lastFrame = 0
        self.nextSeq = 0
        self.pose = 0
        self.ikRuleCount = 0
        self.autoLayerCount = 0
        self.autoLayerOffset = 0
        self.weightOffset = 0
        self.poseKeyOffset = 0
        self.ikLockCount = 0
        self.ikLockOffset = 0
        self.keyValueOffset = 0
        self.keyValueSize = 0
        self.cyclePoseIndex = 0
        self.activityModifierOffset = 0
        self.activityModifierCount = 0
        self.unused = []  # len 5
        self.theName = ''
        self.theActivityName = ''
        self.thePoseKeys = []
        self.theEvents = []  # type: List[SourceMdlEvent]
        self.theAutoLayers = []  # type: List[SourceMdlAutoLayer]
        self.theIkLocks = []  # type: List[SourceMdlIkLock]
        self.theBoneWeights = []  # type: float
        self.theWeightListIndex = []  # type: int
        self.theAnimDescIndexes = []  # type: int
        self.theKeyValues = []  # type: int
        self.theActivityModifiers = []  # type: List[SourceMdlActivityModifier]
        self.theBoneWeightsAreDefault = False


