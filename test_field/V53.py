import io
from pprint import pprint, pformat

import test_field.ByteReader as ByteReader
import test_field.MDL_DATA_V53 as MD
import VTX2,VVD2

class Mdl53(ByteReader.ByteReader):

    def __init__(self,file):
        super().__init__(file)
        self.theMdlFileData = MD.SourceMdlFileData()
        self.ReadMdlHeader00()
        self.ReadMdlHeader01()
        self.ReadMdlHeader02()
        self.ReadBones()
        self.ReadBoneTableByName()
        self.ReadAttachments()
        self.ReadBodyParts()
        self.ReadTextures()
        self.ReadTexturePaths()


    def findVTX(self):
        start = self.tell()
        buff = ByteReader.ByteReader(self.read())
        pos = 0
        poses = []
        probLoc = []
        while True:
            pos = buff.find(self.theMdlFileData.checksum,pos)
            if pos == -1:
                break
            poses.append(pos)
            pos += 1

        while poses:
            datapos = poses.pop()
            self.seek(datapos+12)
            # print('offset',self.tell(),len(poses))
            self.rewind(8)
            if self.readASCII(4) == 'IDSV':
                self.VVDoffset = self.tell()-4
                print('Found VVD offset:',self.VVDoffset)
                continue
            self.skip(4)


            self.skip(8)
            if self.readASCII(4) == 'VPHY':
                print('Found PHY')

                continue
            self.rewind(12)
            probLoc.append(datapos)
        if len(probLoc) == 1:
            self.VTXoffset = probLoc[0]-4
            print('Found VTX offset:', self.VTXoffset)




        self.seek(start)
    def ReadMdlHeader00(self):
        self.VVDoffset,self.VTXoffset = 0,0
        self.theMdlFileData.id = self.readASCII(4)
        self.theMdlFileData.theId = self.theMdlFileData.id
        self.theMdlFileData.version = self.readInt32()
        self.theMdlFileData.checksum = self.read(4)

        self.findVTX()
        if self.VVDoffset!=0 and self.VTXoffset!=0:
            start = self.tell()
            self.seek(self.VTXoffset)
            self.VTX = VTX2.SourceVtxFile49(io.BytesIO(self.read()))
            self.seek(start)
            start = self.tell()
            self.seek(self.VVDoffset)
            self.VVD = VVD2.SourceVvdFile49(io.BytesIO(self.read()))
            self.seek(start)

        self.theMdlFileData.nameCopyOffset = self.readInt32()
        self.theMdlFileData.theNameCopy = self.get_string_at_offset(0,self.theMdlFileData.nameCopyOffset)

        self.theMdlFileData.name = self.readASCII(64)
        self.theMdlFileData.theName = self.theMdlFileData.name.rstrip('\x00')

        self.theMdlFileData.fileSize = self.readUInt32()
        self.theMdlFileData.theActualFileSize = len(self)

    def ReadMdlHeader01(self):
        start = self.tell()
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

        self.theMdlFileData.theSurfacePropName = self.get_string_at_offset(0,self.theMdlFileData.surfacePropOffset)

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
                inputFileStreamPosition = self.tell()
                self.seek(self.theMdlFileData.animBlockNameOffset)
                self.theMdlFileData.theAnimBlockRelativePathFileName = self.readASCIIString()
                self.seek(inputFileStreamPosition)
            if self.theMdlFileData.animBlockOffset > 0:
                inputFileStreamPosition = self.tell()
                self.seek(self.theMdlFileData.animBlockOffset)
                for i in range(self.theMdlFileData.animBlockCount-1):
                    anAnimBlock = MD.SourceMdlAnimBlock
                    anAnimBlock.dataStart = self.readInt32()
                    anAnimBlock.dataEnd = self.readInt32()
                    self.theMdlFileData.theAnimBlocks.append(anAnimBlock)
                self.seek(inputFileStreamPosition)

        self.theMdlFileData.boneTableByNameOffset = self.readInt32()

        self.theMdlFileData.vertexBaseP = self.readInt32()
        self.theMdlFileData.indexBaseP = self.readInt32()

        self.theMdlFileData.directionalLightDot = self.readByte()

        self.theMdlFileData.rootLod = self.readByte()

        self.theMdlFileData.allowedRootLodCount = self.readByte()

        self.theMdlFileData.unused = self.readByte()

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

        self.theMdlFileData.sourceBoneTransformCount = self.readInt32()
        self.theMdlFileData.sourceBoneTransformOffset = self.readInt32()
        self.theMdlFileData.illumPositionAttachmentIndex = self.readInt32()
        self.theMdlFileData.maxEyeDeflection = self.readFloat()
        self.theMdlFileData.linearBoneOffset = self.readInt32()

        self.theMdlFileData.nameOffset = self.readInt32()
        self.theMdlFileData.boneFlexDriverCount = self.readInt32()
        self.theMdlFileData.boneFlexDriverOffset = self.readInt32()
        for n,_ in enumerate(self.theMdlFileData.reserved):
            self.theMdlFileData.reserved[n] = self.readInt32()

    def ReadBones(self):
        self.seek(self.theMdlFileData.boneOffset)
        for i in range(self.theMdlFileData.boneCount):
            boneInputFileStreamPosition = self.tell()
            aBone = MD.SourceMdlBone()
            aBone.nameOffset = self.readInt32()

            aBone.parentBoneIndex = self.readInt32()
            for j in range(6):
                aBone.boneControllerIndex.append(self.readInt32())
            aBone.position = aBone.position.gen(self)
            aBone.quat = aBone.quat(self)
            aBone.rotation = aBone.rotation.gen(self)
            aBone.positionScale = aBone.positionScale.gen(self)
            aBone.rotationScale = aBone.rotationScale.gen(self)
            aBone.poseToBoneColumn0 = aBone.poseToBoneColumn0()
            aBone.poseToBoneColumn1 = aBone.poseToBoneColumn1()
            aBone.poseToBoneColumn2 = aBone.poseToBoneColumn2()
            aBone.poseToBoneColumn3 = aBone.poseToBoneColumn3()
            aBone.poseToBoneColumn0.x = self.readFloat()
            aBone.poseToBoneColumn1.x = self.readFloat()
            aBone.poseToBoneColumn2.x = self.readFloat()
            aBone.poseToBoneColumn3.x = self.readFloat()
            aBone.poseToBoneColumn0.y = self.readFloat()
            aBone.poseToBoneColumn1.y = self.readFloat()
            aBone.poseToBoneColumn2.y = self.readFloat()
            aBone.poseToBoneColumn3.y = self.readFloat()
            aBone.poseToBoneColumn0.z = self.readFloat()
            aBone.poseToBoneColumn1.z = self.readFloat()
            aBone.poseToBoneColumn2.z = self.readFloat()
            aBone.poseToBoneColumn3.z = self.readFloat()

            aBone.qAlignment = aBone.qAlignment(self)

            aBone.flags = self.readInt32()

            aBone.proceduralRuleType = self.readInt32()
            aBone.proceduralRuleOffset = self.readInt32()
            aBone.physicsBoneIndex = self.readInt32()
            aBone.surfacePropNameOffset = self.readInt32()
            aBone.contents = self.readInt32()

            for k in range(8):
                aBone.unused.append(self.readInt32())

            for k in range(7):
                self.readInt32()

            aBone.name = self.get_string_at_offset(boneInputFileStreamPosition,aBone.nameOffset)

            if aBone.proceduralRuleOffset != 0:
                if aBone.proceduralRuleType == aBone.STUDIO_PROC_AXISINTERP:
                    pass
            if aBone.surfacePropNameOffset !=0:
                aBone.theSurfacePropName = self.get_string_at_offset(boneInputFileStreamPosition,aBone.surfacePropNameOffset)


            self.theMdlFileData.theBones.append(aBone)

    def ReadBoneTableByName(self):
        if self.theMdlFileData.boneTableByNameOffset != 0:
            self.seek(self.theMdlFileData.boneTableByNameOffset)
            for i in range(self.theMdlFileData.boneCount):
                self.theMdlFileData.theBoneTableByName.append(self.readByte())

    def ReadAttachments(self):

        self.seek(self.theMdlFileData.localAttachmentOffset)
        for i in range(self.theMdlFileData.localAttachmentCount):
            attachmentInputFileStreamPosition = self.tell()
            anAttachment = MD.SourceMdlAttachment()
            anAttachment.nameOffset = self.readInt32()
            anAttachment.theName = self.get_string_at_offset(attachmentInputFileStreamPosition,anAttachment.nameOffset)
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

            for _ in range(8):
                anAttachment.unused.append(self.readInt32())

            self.theMdlFileData.theAttachments.append(anAttachment)
            # pprint(anAttachment.__dict__)

    def ReadBodyParts(self):
        if self.theMdlFileData.bodyPartCount>0:
            self.seek(self.theMdlFileData.bodyPartOffset)
            for i in range(self.theMdlFileData.bodyPartCount):
                bodyPartInputFileStreamPosition = self.tell()
                aBodyPart = MD.SourceMdlBodyPart()

                aBodyPart.nameOffset = self.readInt32()
                aBodyPart.theName = self.get_string_at_offset(bodyPartInputFileStreamPosition,aBodyPart.nameOffset)
                aBodyPart.modelCount = self.readInt32()
                aBodyPart.base = self.readInt32()
                aBodyPart.modelOffset = self.readInt32()
                inputFileStreamPosition = self.tell()
                self.ReadModels(bodyPartInputFileStreamPosition,aBodyPart)
                self.seek(inputFileStreamPosition)
                self.theMdlFileData.theBodyParts.append(aBodyPart)

    def ReadModels(self,bodyPartInputFileStreamPosition,aBodyPart:MD.SourceMdlBodyPart):
        ll = []
        if aBodyPart.modelCount>0:
            self.seek(bodyPartInputFileStreamPosition+aBodyPart.modelOffset)

            for j in range(aBodyPart.modelCount-1):
                modelInputFileStreamPosition = self.tell()
                aModel = MD.SourceMdlModel()

                aModel.name = self.readASCII(64).rstrip('\x00')
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
                modelVertexData = MD.SourceMdlModelVertexData()
                modelVertexData.vertexDataP = self.readInt32()
                modelVertexData.tangentDataP = self.readInt32()
                aModel.vertexData = modelVertexData
                for _ in range(8):
                    aModel.unused.append(self.readInt32())

                inputFileStreamPosition = self.tell()

                self.ReadEyeballs(modelInputFileStreamPosition,aModel)
                self.ReadMeshes(modelInputFileStreamPosition,aModel)
                aBodyPart.theModels.append(aModel)

                self.seek(inputFileStreamPosition)
    def ReadMeshes(self, modelInputFileStreamPosition, aModel: MD.SourceMdlModel):
        if aModel.meshCount>0 and aModel.meshOffset!=0:
            self.seek(aModel.meshOffset+modelInputFileStreamPosition)

            for meshIndex in range(aModel.meshCount):
                meshInputFileStreamPosition = self.tell()
                aMesh = MD.SourceMdlMesh()
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
                aMesh.centerX = self.readFloat()
                aMesh.centerX = self.readFloat()
                meshVertexData = MD.SourceMdlMeshVertexData()
                meshVertexData.modelVertexDataP = self.readInt32()
                for x in range(MD.MAX_NUM_LODS):
                    meshVertexData.lodVertexCount.append(self.readInt32())
                aMesh.vertexData = meshVertexData

                for x in range(8):
                    aMesh.unused.append(self.readInt32())
                aModel.theMeshes.append(aMesh)
                if aMesh.materialType == 1:
                    aModel.theEyeballs[aMesh.materialParam].theTextureIndex = aMesh.materialIndex

                inputFileStreamPosition = self.tell()

                if aMesh.flexCount > 0 and aMesh.flexOffset!=0:
                    self.ReadFlexes(meshInputFileStreamPosition,aMesh)

                self.seek(inputFileStreamPosition)
                # ll.append(aMesh)

        # return ll

    def ReadEyeballs(self, modelInputFileStreamPosition, aModel: MD.SourceMdlModel):
        if aModel.eyeballCount > 0 and aModel.eyeballOffset != 0:
            self.seek(modelInputFileStreamPosition+aModel.eyeballOffset)

            for k in range(aModel.eyeballCount):
                eyeballInputFileStreamPosition = self.tell()
                anEyeball = MD.SourceMdlEyeball()

                anEyeball.nameOffset = self.readInt32()
                anEyeball.theName = self.get_string_at_offset(eyeballInputFileStreamPosition,anEyeball.nameOffset)

                anEyeball.boneIndex = self.readInt32()
                anEyeball.org = anEyeball.org.gen(self)
                anEyeball.zOffset = self.readFloat()
                anEyeball.radius = self.readFloat()
                anEyeball.up = anEyeball.org.gen(self)
                anEyeball.forward = anEyeball.org.gen(self)
                anEyeball.texture = self.readInt32()

                anEyeball.unused1 = self.readInt32()
                anEyeball.irisScale = self.readFloat()
                anEyeball.unused2 = self.readInt32()
                anEyeball.upperFlexDesc[0] = self.readInt32()
                anEyeball.upperFlexDesc[1] = self.readInt32()
                anEyeball.upperFlexDesc[2] = self.readInt32()
                anEyeball.lowerFlexDesc[0] = self.readInt32()
                anEyeball.lowerFlexDesc[1] = self.readInt32()
                anEyeball.lowerFlexDesc[2] = self.readInt32()
                anEyeball.upperTarget[0] = self.readFloat()
                anEyeball.upperTarget[1] = self.readFloat()
                anEyeball.upperTarget[2] = self.readFloat()
                anEyeball.lowerTarget[0] = self.readFloat()
                anEyeball.lowerTarget[1] = self.readFloat()
                anEyeball.lowerTarget[2] = self.readFloat()

                anEyeball.upperLidFlexDesc = self.readInt32()
                anEyeball.lowerLidFlexDesc = self.readInt32()

                for _ in range(3):
                    anEyeball.unused.append(self.readInt32())

                anEyeball.eyeballIsNonFacs = self.readByte()

                for _ in range(2):
                    anEyeball.unused3.append(self.readACSIIChar())

                for _ in range(6):
                    anEyeball.unused3.append(self.readInt32())

                anEyeball.theTextureIndex = -1
                aModel.theEyeballs.append(anEyeball)


    def ReadFlexes(self, meshInputFileStreamPosition, aMesh: MD.SourceMdlMesh):
        self.data.seek(meshInputFileStreamPosition + aMesh.flexOffset, 0)

        if aMesh.flexCount > 0:
            for k in range(aMesh.flexCount-1):
                flexInputFileStreamPosition = self.data.tell()
                aFlex = MD.SourceMdlFlex()
                aFlex.flexDescIndex = self.readInt32()
                aFlex.target0 = self.readFloat()
                aFlex.target1 = self.readFloat()
                aFlex.target2 = self.readFloat()
                aFlex.target3 = self.readFloat()

                aFlex.vertCount = self.readInt32()
                aFlex.vertOffset = self.readInt32()

                aFlex.flexDescPartnerIndex = self.readInt32()
                aFlex.vertAnimType = self.readByte()
                aFlex.unusedChar = []
                for x in range(2):
                    aFlex.unusedChar.append(self.readACSIIChar())
                aFlex.unused = []
                for x in range(5):
                    aFlex.unused.append(self.readInt32())
                inputFileStreamPosition = self.data.tell()

                if aFlex.vertCount > 0 and aFlex.vertOffset != 0:
                    self.ReadVertAnims(flexInputFileStreamPosition, aFlex)
                self.data.seek(inputFileStreamPosition, 0)

                aMesh.theFlexes.append(aFlex)

    def ReadVertAnims(self, flexInputFileStreamPosition, aFlex: MD.SourceMdlFlex):
        self.data.seek(flexInputFileStreamPosition + aFlex.vertOffset, 0)
        for k in range(aFlex.vertCount):
            if aFlex.vertAnimType == aFlex.STUDIO_VERT_ANIM_WRINKLE:
                aVertAnim = MD.SourceMdlVertAnimWrinkle()
            else:
                aVertAnim = MD.SourceMdlVertAnim()
            aVertAnim.index = self.readUInt16()
            aVertAnim.speed = self.readUByte()
            aVertAnim.side = self.readUByte()
            aVertAnim.theDelta = []
            for x in range(3):
                aFloat = MD.SourceFloat16bits()
                aFloat.the16BitValue = self.readUInt16()
                aVertAnim.theDelta.append(aFloat.TheFloatValue)

            aVertAnim.theNDelta = []
            for x in range(3):
                aFloat = MD.SourceFloat16bits()
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
                aFlexDesc = MD.SourceMdlFlexDesc()
                aFlexDesc.nameOffset = self.readInt32()
                inputFileStreamPosition = self.data.tell()
                if aFlexDesc.nameOffset != 0:
                    aFlexDesc.theName = self.get_string_at_offset(flexDescInputFileStreamPosition,
                                                               aFlexDesc.nameOffset)
                self.data.seek(inputFileStreamPosition, 0)
                self.theMdlFileData.theFlexDescs.append(aFlexDesc)

    def ReadFlexControllers(self):
        if self.theMdlFileData.flexControllerCount > 0:
            self.data.seek(self.theMdlFileData.flexControllerOffset, 0)
            for i in range(self.theMdlFileData.flexControllerCount):
                flexControllerInputFileStreamPosition = self.data.tell()
                aFlexController = MD.SourceMdlFlexController()
                aFlexController.typeOffset = self.readInt32()
                aFlexController.nameOffset = self.readInt32()
                aFlexController.localToGlobal = self.readInt32()
                aFlexController.min = self.readFloat()
                aFlexController.max = self.readFloat()
                self.theMdlFileData.theFlexControllers.append(aFlexController)
                inputFileStreamPosition = self.data.tell()
                if aFlexController.typeOffset != 0:
                    aFlexController.theType = self.get_string_at_offset( flexControllerInputFileStreamPosition,
                                                                     aFlexController.typeOffset)
                else:
                    aFlexController.theType = ''
                if aFlexController.nameOffset != 0:
                    aFlexController.theName = self.get_string_at_offset( flexControllerInputFileStreamPosition,
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
            aFlexRule = MD.SourceMdlFlexRule()
            aFlexRule.flexIndex = self.readInt32()
            aFlexRule.opCount = self.readInt32()
            aFlexRule.opOffset = self.readInt32()
            inputFileStreamPosition = self.data.tell()
            if aFlexRule.opCount > 0 and aFlexRule.opOffset != 0:
                self.ReadFlexOps(flexRuleInputFileStreamPosition, aFlexRule)
            self.theMdlFileData.theFlexDescs[aFlexRule.flexIndex].theDescIsUsedByFlexRule = True
            self.theMdlFileData.theFlexRules.append(aFlexRule)
            self.data.seek(inputFileStreamPosition, 0)

        if self.theMdlFileData.theFlexRules.__len__() > 0:
            self.theMdlFileData.theModelCommandIsUsed = True

    def ReadFlexOps(self, flexRuleInputFileStreamPosition, aFlexRule: MD.SourceMdlFlexRule):
        self.data.seek(flexRuleInputFileStreamPosition + aFlexRule.opOffset)
        for i in range(aFlexRule.opCount):
            aFlexOp = MD.SourceMdlFlexOp()
            aFlexOp.op = self.readInt32()
            if aFlexOp.op == MD.SourceMdlFlexOp.STUDIO_CONST:
                aFlexOp.value = self.readFloat()
            else:
                aFlexOp.index = self.readInt32()
                if aFlexOp.op == MD.SourceMdlFlexOp.STUDIO_FETCH2:
                    self.theMdlFileData.theFlexDescs[aFlexOp.index].theDescIsUsedByFlexRule = True
            aFlexRule.theFlexOps.append(aFlexOp)


    def ReadTextures(self):
        if self.theMdlFileData.textureCount>0:
            self.seek(self.theMdlFileData.textureOffset)
            for i in range(self.theMdlFileData.textureCount-1):
                textureInputFileStreamPosition = self.tell()
                aTexture = MD.SourceMdlTexture()
                aTexture.nameOffset = self.readInt32()
                aTexture.thePathFileName = self.get_string_at_offset(textureInputFileStreamPosition,aTexture.nameOffset)
                aTexture.flags = self.readInt32()
                aTexture.used = self.readInt32()
                aTexture.unused1 = self.readInt32()
                aTexture.materialP = self.readInt32()
                aTexture.clientMaterialP = self.readInt32()


                for _ in range(5):
                    aTexture.unused.append(self.readInt32())


                self.theMdlFileData.theTextures.append(aTexture)

    def ReadTexturePaths(self):
        if self.theMdlFileData.texturePathCount > 0:
            self.data.seek(self.theMdlFileData.texturePathOffset, 0)
            for i in range(self.theMdlFileData.texturePathCount):
                texturePathInputFileStreamPosition = self.data.tell()
                texturePathOffset = self.readInt32()
                inputFileStreamPosition = self.data.tell()
                if texturePathOffset != 0:
                    aTexturePath = self.get_string_at_offset(texturePathOffset, 0)
                else:
                    aTexturePath = ''
                self.theMdlFileData.theTexturePaths.append(aTexturePath)
                self.data.seek(inputFileStreamPosition, 0)



if __name__ == '__main__':
    mdl = Mdl53(open(r'E:\MDL_reader\test_data\titan_buddy.mdl','rb'))
    pprint(mdl.theMdlFileData.theBodyParts[1].theModels[1].theMeshes)
    for body in mdl.theMdlFileData.theBodyParts: #type: MD.SourceMdlBodyPart
        print(body.modelCount)
        for model in body.theModels: #type: MD.SourceMdlModel
            print(model.meshCount)
            print(model.theMeshes)
    # pprint(mdl.theMdlFileData.theBones)
    # for bd in mdl.theMdlFileData.theBodyParts: #type: MD.SourceMdlBodyPart
    #     print(bd.theName)
    #     for model in bd.theModels: #type: MD.SourceMdlModel
    #         for mesh in model.theMeshes: #type:MD.SourceMdlMesh
    #             pprint(mesh.theFlexes)

