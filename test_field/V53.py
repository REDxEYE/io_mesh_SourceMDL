import io
from pprint import pprint, pformat
from test_field import VTX2, VVD2
import test_field.MDL_DATA_V53 as MD
from test_field.GLOBALS import SourceMdlTexture
from test_field.ByteReader import ByteReader


class Mdl53:
    def __init__(self, file):
        self.reader = ByteReader(file)
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

    def ReadMdlHeader00(self):
        self.VVDoffset, self.VTXoffset = 0, 0
        self.theMdlFileData.id = self.reader.readASCII(4)
        self.theMdlFileData.theId = self.theMdlFileData.id
        self.theMdlFileData.version = self.reader.readInt32()
        self.theMdlFileData.checksum = self.reader.read(4)

        self.theMdlFileData.nameCopyOffset = self.reader.readInt32()
        self.theMdlFileData.theNameCopy = self.reader.get_string_at_offset(0, self.theMdlFileData.nameCopyOffset)

        self.theMdlFileData.name = self.reader.readASCII(64)
        self.theMdlFileData.theName = self.theMdlFileData.name.rstrip('\x00')

        self.theMdlFileData.fileSize = self.reader.readUInt32()
        self.theMdlFileData.theActualFileSize = len(self.reader)

    def ReadMdlHeader01(self):
        start = self.reader.tell()
        self.theMdlFileData.eyePosition.read(self.reader)
        self.theMdlFileData.illuminationPosition.read(self.reader)
        self.theMdlFileData.hullMinPosition.read(self.reader)
        self.theMdlFileData.hullMaxPosition.read(self.reader)
        self.theMdlFileData.viewBoundingBoxMinPosition.read(self.reader)
        self.theMdlFileData.viewBoundingBoxMaxPosition.read(self.reader)
        self.theMdlFileData.flags = self.reader.readInt32()

        self.theMdlFileData.boneCount = self.reader.readInt32()
        self.theMdlFileData.boneOffset = self.reader.readInt32()

        self.theMdlFileData.boneControllerCount = self.reader.readInt32()
        self.theMdlFileData.boneControllerOffset = self.reader.readInt32()

        self.theMdlFileData.hitboxSetCount = self.reader.readInt32()
        self.theMdlFileData.hitboxSetOffset = self.reader.readInt32()

        self.theMdlFileData.localAnimationCount = self.reader.readInt32()
        self.theMdlFileData.localAnimationOffset = self.reader.readInt32()

        self.theMdlFileData.localSequenceCount = self.reader.readInt32()
        self.theMdlFileData.localSequenceOffset = self.reader.readInt32()

        self.theMdlFileData.activityListVersion = self.reader.readInt32()
        self.theMdlFileData.eventsIndexed = self.reader.readInt32()

        self.theMdlFileData.textureCount = self.reader.readInt32()
        self.theMdlFileData.textureOffset = self.reader.readInt32()

        self.theMdlFileData.texturePathCount = self.reader.readInt32()
        self.theMdlFileData.texturePathOffset = self.reader.readInt32()

        self.theMdlFileData.skinReferenceCount = self.reader.readInt32()
        self.theMdlFileData.skinFamilyCount = self.reader.readInt32()
        self.theMdlFileData.skinFamilyOffset = self.reader.readInt32()

        self.theMdlFileData.bodyPartCount = self.reader.readInt32()
        self.theMdlFileData.bodyPartOffset = self.reader.readInt32()

        self.theMdlFileData.localAttachmentCount = self.reader.readInt32()
        self.theMdlFileData.localAttachmentOffset = self.reader.readInt32()

        self.theMdlFileData.localNodeCount = self.reader.readInt32()
        self.theMdlFileData.localNodeOffset = self.reader.readInt32()

        self.theMdlFileData.localNodeNameOffset = self.reader.readInt32()

        self.theMdlFileData.flexDescCount = self.reader.readInt32()
        self.theMdlFileData.flexDescOffset = self.reader.readInt32()

        self.theMdlFileData.flexControllerCount = self.reader.readInt32()
        self.theMdlFileData.flexControllerOffset = self.reader.readInt32()

        self.theMdlFileData.flexRuleCount = self.reader.readInt32()
        self.theMdlFileData.flexRuleOffset = self.reader.readInt32()

        self.theMdlFileData.ikChainCount = self.reader.readInt32()
        self.theMdlFileData.ikChainOffset = self.reader.readInt32()

        self.theMdlFileData.mouthCount = self.reader.readInt32()
        self.theMdlFileData.mouthOffset = self.reader.readInt32()

        self.theMdlFileData.localPoseParamaterCount = self.reader.readInt32()
        self.theMdlFileData.localPoseParameterOffset = self.reader.readInt32()

        self.theMdlFileData.surfacePropOffset = self.reader.readInt32()

        self.theMdlFileData.theSurfacePropName = self.reader.get_string_at_offset(0, self.theMdlFileData.surfacePropOffset)

        self.theMdlFileData.keyValueOffset = self.reader.readInt32()
        self.theMdlFileData.keyValueSize = self.reader.readInt32()

        self.theMdlFileData.localIkAutoPlayLockCount = self.reader.readInt32()
        self.theMdlFileData.localIkAutoPlayLockOffset = self.reader.readInt32()

        self.theMdlFileData.mass = self.reader.readFloat()
        self.theMdlFileData.contents = self.reader.readInt32()

        self.theMdlFileData.includeModelCount = self.reader.readInt32()
        self.theMdlFileData.includeModelOffset = self.reader.readInt32()

        self.theMdlFileData.virtualModelP = self.reader.readInt32()

        self.theMdlFileData.animBlockNameOffset = self.reader.readInt32()
        self.theMdlFileData.animBlockCount = self.reader.readInt32()
        self.theMdlFileData.animBlockOffset = self.reader.readInt32()
        self.theMdlFileData.animBlockModelP = self.reader.readInt32()
        # if self.theMdlFileData.animBlockCount > 0:
        #     if self.theMdlFileData.animBlockNameOffset > 0:
        #         inputFileStreamPosition = self.reader.tell()
        #         self.reader.seek(self.theMdlFileData.animBlockNameOffset)
        #         self.theMdlFileData.theAnimBlockRelativePathFileName = self.reader.readASCIIString()
        #         self.reader.seek(inputFileStreamPosition)
        #     if self.theMdlFileData.animBlockOffset > 0:
        #         inputFileStreamPosition = self.reader.tell()
        #         self.reader.seek(self.theMdlFileData.animBlockOffset)
        #         for i in range(self.theMdlFileData.animBlockCount - 1):
        #             anAnimBlock = MD.SourceMdlAnimBlock
        #             anAnimBlock.dataStart = self.reader.readInt32()
        #             anAnimBlock.dataEnd = self.reader.readInt32()
        #             self.theMdlFileData.theAnimBlocks.append(anAnimBlock)
        #         self.reader.seek(inputFileStreamPosition)

        self.theMdlFileData.boneTableByNameOffset = self.reader.readInt32()

        self.theMdlFileData.vertexBaseP = self.reader.readInt32()
        self.theMdlFileData.indexBaseP = self.reader.readInt32()

        self.theMdlFileData.directionalLightDot = self.reader.readByte()

        self.theMdlFileData.rootLod = self.reader.readByte()

        self.theMdlFileData.allowedRootLodCount = self.reader.readByte()

        self.theMdlFileData.unused = self.reader.readByte()

        self.theMdlFileData.unused4 = self.reader.readInt32()

        self.theMdlFileData.flexControllerUiCount = self.reader.readInt32()
        self.theMdlFileData.flexControllerUiOffset = self.reader.readInt32()

        self.theMdlFileData.vertAnimFixedPointScale = self.reader.readFloat()
        self.theMdlFileData.surfacePropLookup = self.reader.readInt32()

        self.theMdlFileData.studioHeader2Offset = self.reader.readInt32()

        self.theMdlFileData.unused2 = self.reader.readInt32()

        print('DANGER',self.reader.tell())
        self.reader.read(16)
        self.VTXoffset = self.reader.readInt32()
        self.VVDoffset = self.reader.readInt32()
        print('Found VTX:{} and VVD:{}'.format(self.VTXoffset,self.VVDoffset))
        if self.VVDoffset != 0 and self.VTXoffset != 0:
            start = self.reader.tell()
            self.reader.seek(self.VTXoffset)
            self.VTX = VTX2.SourceVtxFile49(io.BytesIO(self.reader.read()))
            self.reader.seek(self.VVDoffset)
            self.VVD = VVD2.SourceVvdFile49(io.BytesIO(self.reader.read()))
            self.reader.seek(start)


        if self.theMdlFileData.bodyPartCount == 0 and self.theMdlFileData.localSequenceCount > 0:
            self.theMdlFileData.theMdlFileOnlyHasAnimations = True


    def ReadMdlHeader02(self):
        self.theMdlFileData.sourceBoneTransformCount = self.reader.readInt32()
        self.theMdlFileData.sourceBoneTransformOffset = self.reader.readInt32()
        self.theMdlFileData.illumPositionAttachmentIndex = self.reader.readInt32()
        self.theMdlFileData.maxEyeDeflection = self.reader.readFloat()
        self.theMdlFileData.linearBoneOffset = self.reader.readInt32()

        self.theMdlFileData.nameOffset = self.reader.readInt32()
        self.theMdlFileData.boneFlexDriverCount = self.reader.readInt32()
        self.theMdlFileData.boneFlexDriverOffset = self.reader.readInt32()
        for n, _ in enumerate(self.theMdlFileData.reserved):
            self.theMdlFileData.reserved[n] = self.reader.readInt32()


    def ReadBones(self):
        self.reader.seek(self.theMdlFileData.boneOffset)
        for i in range(self.theMdlFileData.boneCount):
            boneInputFileStreamPosition = self.reader.tell()
            aBone = MD.SourceMdlBone()
            aBone.nameOffset = self.reader.readInt32()

            aBone.parentBoneIndex = self.reader.readInt32()
            for j in range(6):
                aBone.boneControllerIndex.append(self.reader.readInt32())
            aBone.position = aBone.position.read(self.reader)
            aBone.quat = aBone.quat.read(self.reader)
            aBone.rotation = aBone.rotation.read(self.reader)
            aBone.positionScale = aBone.positionScale.read(self.reader)
            aBone.rotationScale = aBone.rotationScale.read(self.reader)
            aBone.poseToBoneColumn0.x = self.reader.readFloat()
            aBone.poseToBoneColumn1.x = self.reader.readFloat()
            aBone.poseToBoneColumn2.x = self.reader.readFloat()
            aBone.poseToBoneColumn3.x = self.reader.readFloat()
            aBone.poseToBoneColumn0.y = self.reader.readFloat()
            aBone.poseToBoneColumn1.y = self.reader.readFloat()
            aBone.poseToBoneColumn2.y = self.reader.readFloat()
            aBone.poseToBoneColumn3.y = self.reader.readFloat()
            aBone.poseToBoneColumn0.z = self.reader.readFloat()
            aBone.poseToBoneColumn1.z = self.reader.readFloat()
            aBone.poseToBoneColumn2.z = self.reader.readFloat()
            aBone.poseToBoneColumn3.z = self.reader.readFloat()

            aBone.qAlignment = aBone.qAlignment.read(self.reader)
            aBone.flags = self.reader.readInt32()

            aBone.proceduralRuleType = self.reader.readInt32()
            aBone.proceduralRuleOffset = self.reader.readInt32()
            aBone.physicsBoneIndex = self.reader.readInt32()
            aBone.surfacePropNameOffset = self.reader.readInt32()
            aBone.contents = self.reader.readInt32()

            for k in range(8):
                aBone.unused.append(self.reader.readInt32())

            for k in range(7):
                self.reader.readInt32()

            aBone.name = self.reader.get_string_at_offset(boneInputFileStreamPosition, aBone.nameOffset)

            if aBone.proceduralRuleOffset != 0:
                if aBone.proceduralRuleType == aBone.STUDIO_PROC_AXISINTERP:
                    pass
            if aBone.surfacePropNameOffset != 0:
                aBone.theSurfacePropName = self.reader.get_string_at_offset(boneInputFileStreamPosition,
                                                                     aBone.surfacePropNameOffset)

            self.theMdlFileData.theBones.append(aBone)


    def ReadBoneTableByName(self):
        if self.theMdlFileData.boneTableByNameOffset != 0:
            self.reader.seek(self.theMdlFileData.boneTableByNameOffset)
            for i in range(self.theMdlFileData.boneCount):
                self.theMdlFileData.theBoneTableByName.append(self.reader.readByte())


    def ReadAttachments(self):
        self.reader.seek(self.theMdlFileData.localAttachmentOffset)
        for i in range(self.theMdlFileData.localAttachmentCount):
            attachmentInputFileStreamPosition = self.reader.tell()
            anAttachment = MD.SourceMdlAttachment()
            anAttachment.nameOffset = self.reader.readInt32()
            anAttachment.theName = self.reader.get_string_at_offset(attachmentInputFileStreamPosition, anAttachment.nameOffset)
            anAttachment.flags = self.reader.readInt32()
            anAttachment.localBoneIndex = self.reader.readInt32()
            anAttachment.localM11 = self.reader.readFloat()
            anAttachment.localM12 = self.reader.readFloat()
            anAttachment.localM13 = self.reader.readFloat()
            anAttachment.localM14 = self.reader.readFloat()
            anAttachment.localM21 = self.reader.readFloat()
            anAttachment.localM22 = self.reader.readFloat()
            anAttachment.localM23 = self.reader.readFloat()
            anAttachment.localM24 = self.reader.readFloat()
            anAttachment.localM31 = self.reader.readFloat()
            anAttachment.localM32 = self.reader.readFloat()
            anAttachment.localM33 = self.reader.readFloat()
            anAttachment.localM34 = self.reader.readFloat()

            for _ in range(8):
                anAttachment.unused.append(self.reader.readInt32())

            self.theMdlFileData.theAttachments.append(anAttachment)
            # pprint(anAttachment.__dict__)


    def ReadBodyParts(self):
        if self.theMdlFileData.bodyPartCount > 0:
            self.reader.seek(self.theMdlFileData.bodyPartOffset)
            for i in range(self.theMdlFileData.bodyPartCount):
                bodyPartInputFileStreamPosition = self.reader.tell()
                aBodyPart = MD.SourceMdlBodyPart()

                aBodyPart.nameOffset = self.reader.readInt32()
                aBodyPart.theName = self.reader.get_string_at_offset(bodyPartInputFileStreamPosition, aBodyPart.nameOffset)
                aBodyPart.modelCount = self.reader.readInt32()
                aBodyPart.base = self.reader.readInt32()
                aBodyPart.modelOffset = self.reader.readInt32()
                inputFileStreamPosition = self.reader.tell()
                self.ReadModels(bodyPartInputFileStreamPosition, aBodyPart)
                self.reader.seek(inputFileStreamPosition)
                self.theMdlFileData.theBodyParts.append(aBodyPart)


    def ReadModels(self, bodyPartInputFileStreamPosition, aBodyPart: MD.SourceMdlBodyPart):
        if aBodyPart.modelCount > 0:
            self.reader.seek(bodyPartInputFileStreamPosition + aBodyPart.modelOffset)

            for j in range(aBodyPart.modelCount):
                modelInputFileStreamPosition = self.reader.tell()
                aModel = MD.SourceMdlModel()

                aModel.name = self.reader.readASCII(64).rstrip('\x00')
                aModel.type = self.reader.readInt32()
                aModel.boundingRadius = self.reader.readFloat()
                aModel.meshCount = self.reader.readInt32()
                aModel.meshOffset = self.reader.readInt32()
                aModel.vertexCount = self.reader.readInt32()
                aModel.vertexOffset = self.reader.readInt32()
                aModel.tangentOffset = self.reader.readInt32()
                aModel.attachmentCount = self.reader.readInt32()
                aModel.attachmentOffset = self.reader.readInt32()
                aModel.eyeballCount = self.reader.readInt32()
                aModel.eyeballOffset = self.reader.readInt32()
                modelVertexData = MD.SourceMdlModelVertexData()
                modelVertexData.vertexDataP = self.reader.readInt32()
                modelVertexData.tangentDataP = self.reader.readInt32()
                aModel.vertexData = modelVertexData
                for _ in range(8):
                    aModel.unused.append(self.reader.readInt32())

                inputFileStreamPosition = self.reader.tell()

                self.ReadEyeballs(modelInputFileStreamPosition, aModel)
                self.ReadMeshes(modelInputFileStreamPosition, aModel)
                aBodyPart.theModels.append(aModel)

                self.reader.seek(inputFileStreamPosition)


    def ReadMeshes(self, modelInputFileStreamPosition, aModel: MD.SourceMdlModel):
        if aModel.meshCount > 0 and aModel.meshOffset != 0:
            self.reader.seek(aModel.meshOffset + modelInputFileStreamPosition)

            for meshIndex in range(aModel.meshCount):
                meshInputFileStreamPosition = self.reader.tell()
                aMesh = MD.SourceMdlMesh()
                aMesh.materialIndex = self.reader.readInt32()
                aMesh.modelOffset = self.reader.readInt32()
                aMesh.vertexCount = self.reader.readInt32()
                aMesh.vertexIndexStart = self.reader.readInt32()
                aMesh.flexCount = self.reader.readInt32()
                aMesh.flexOffset = self.reader.readInt32()
                aMesh.materialType = self.reader.readInt32()
                aMesh.materialParam = self.reader.readInt32()
                aMesh.id = self.reader.readInt32()
                aMesh.centerX = self.reader.readFloat()
                aMesh.centerX = self.reader.readFloat()
                aMesh.centerX = self.reader.readFloat()
                meshVertexData = MD.SourceMdlMeshVertexData()
                meshVertexData.modelVertexDataP = self.reader.readInt32()
                for x in range(MD.MAX_NUM_LODS):
                    meshVertexData.lodVertexCount.append(self.reader.readInt32())
                aMesh.vertexData = meshVertexData

                for x in range(8):
                    aMesh.unused.append(self.reader.readInt32())
                aModel.theMeshes.append(aMesh)
                if aMesh.materialType == 1:
                    aModel.theEyeballs[aMesh.materialParam].theTextureIndex = aMesh.materialIndex

                inputFileStreamPosition = self.reader.tell()

                if aMesh.flexCount > 0 and aMesh.flexOffset != 0:
                    self.ReadFlexes(meshInputFileStreamPosition, aMesh)

                self.reader.seek(inputFileStreamPosition)
                # ll.append(aMesh)

                # return ll


    def ReadEyeballs(self, modelInputFileStreamPosition, aModel: MD.SourceMdlModel):
        if aModel.eyeballCount > 0 and aModel.eyeballOffset != 0:
            self.reader.seek(modelInputFileStreamPosition + aModel.eyeballOffset)

            for k in range(aModel.eyeballCount):
                eyeballInputFileStreamPosition = self.reader.tell()
                anEyeball = MD.SourceMdlEyeball()

                anEyeball.nameOffset = self.reader.readInt32()
                anEyeball.theName = self.reader.get_string_at_offset(eyeballInputFileStreamPosition, anEyeball.nameOffset)

                anEyeball.boneIndex = self.reader.readInt32()
                anEyeball.org = anEyeball.org.gen(self)
                anEyeball.zOffset = self.reader.readFloat()
                anEyeball.radius = self.reader.readFloat()
                anEyeball.up = anEyeball.org.gen(self)
                anEyeball.forward = anEyeball.org.gen(self)
                anEyeball.texture = self.reader.readInt32()

                anEyeball.unused1 = self.reader.readInt32()
                anEyeball.irisScale = self.reader.readFloat()
                anEyeball.unused2 = self.reader.readInt32()
                anEyeball.upperFlexDesc[0] = self.reader.readInt32()
                anEyeball.upperFlexDesc[1] = self.reader.readInt32()
                anEyeball.upperFlexDesc[2] = self.reader.readInt32()
                anEyeball.lowerFlexDesc[0] = self.reader.readInt32()
                anEyeball.lowerFlexDesc[1] = self.reader.readInt32()
                anEyeball.lowerFlexDesc[2] = self.reader.readInt32()
                anEyeball.upperTarget[0] = self.reader.readFloat()
                anEyeball.upperTarget[1] = self.reader.readFloat()
                anEyeball.upperTarget[2] = self.reader.readFloat()
                anEyeball.lowerTarget[0] = self.reader.readFloat()
                anEyeball.lowerTarget[1] = self.reader.readFloat()
                anEyeball.lowerTarget[2] = self.reader.readFloat()

                anEyeball.upperLidFlexDesc = self.reader.readInt32()
                anEyeball.lowerLidFlexDesc = self.reader.readInt32()

                for _ in range(3):
                    anEyeball.unused.append(self.reader.readInt32())

                anEyeball.eyeballIsNonFacs = self.reader.readByte()

                for _ in range(2):
                    anEyeball.unused3.append(self.reader.readACSIIChar())

                for _ in range(6):
                    anEyeball.unused3.append(self.reader.readInt32())

                anEyeball.theTextureIndex = -1
                aModel.theEyeballs.append(anEyeball)


    def ReadFlexes(self, meshInputFileStreamPosition, aMesh: MD.SourceMdlMesh):
        self.reader.seek(meshInputFileStreamPosition + aMesh.flexOffset, 0)

        if aMesh.flexCount > 0:
            for k in range(aMesh.flexCount - 1):
                flexInputFileStreamPosition = self.reader.tell()
                aFlex = MD.SourceMdlFlex()
                aFlex.flexDescIndex = self.reader.readInt32()
                aFlex.target0 = self.reader.readFloat()
                aFlex.target1 = self.reader.readFloat()
                aFlex.target2 = self.reader.readFloat()
                aFlex.target3 = self.reader.readFloat()

                aFlex.vertCount = self.reader.readInt32()
                aFlex.vertOffset = self.reader.readInt32()

                aFlex.flexDescPartnerIndex = self.reader.readInt32()
                aFlex.vertAnimType = self.reader.readByte()
                aFlex.unusedChar = []
                for x in range(2):
                    aFlex.unusedChar.append(self.reader.readACSIIChar())
                aFlex.unused = []
                for x in range(5):
                    aFlex.unused.append(self.reader.readInt32())
                inputFileStreamPosition = self.reader.tell()

                if aFlex.vertCount > 0 and aFlex.vertOffset != 0:
                    self.ReadVertAnims(flexInputFileStreamPosition, aFlex)
                self.reader.seek(inputFileStreamPosition, 0)

                aMesh.theFlexes.append(aFlex)


    def ReadVertAnims(self, flexInputFileStreamPosition, aFlex: MD.SourceMdlFlex):
        self.reader.seek(flexInputFileStreamPosition + aFlex.vertOffset, 0)
        for k in range(aFlex.vertCount):
            if aFlex.vertAnimType == aFlex.STUDIO_VERT_ANIM_WRINKLE:
                aVertAnim = MD.SourceMdlVertAnimWrinkle()
            else:
                aVertAnim = MD.SourceMdlVertAnim()
            aVertAnim.index = self.reader.readUInt16()
            aVertAnim.speed = self.reader.readUByte()
            aVertAnim.side = self.reader.readUByte()
            aVertAnim.theDelta = []
            for x in range(3):
                aFloat = MD.SourceFloat16bits()
                aFloat.the16BitValue = self.reader.readUInt16()
                aVertAnim.theDelta.append(aFloat.TheFloatValue)

            aVertAnim.theNDelta = []
            for x in range(3):
                aFloat = MD.SourceFloat16bits()
                aFloat.the16BitValue = self.reader.readUInt16()
                aVertAnim.theNDelta.append(aFloat.TheFloatValue)
            if aFlex.vertAnimType == aFlex.STUDIO_VERT_ANIM_WRINKLE:
                aVertAnim.wrinkleDelta = self.reader.readInt16()
            # pprint(aVertAnim)
            aFlex.theVertAnims.append(aVertAnim)


    def ReadFlexDescs(self):
        if self.theMdlFileData.flexDescCount > 0:
            self.reader.seek(self.theMdlFileData.flexDescOffset, 0)
            for i in range(self.theMdlFileData.flexDescCount):
                flexDescInputFileStreamPosition = self.reader.tell()
                aFlexDesc = MD.SourceMdlFlexDesc()
                aFlexDesc.nameOffset = self.reader.readInt32()
                inputFileStreamPosition = self.reader.tell()
                if aFlexDesc.nameOffset != 0:
                    aFlexDesc.theName = self.reader.get_string_at_offset(flexDescInputFileStreamPosition,
                                                                  aFlexDesc.nameOffset)
                self.reader.seek(inputFileStreamPosition, 0)
                self.theMdlFileData.theFlexDescs.append(aFlexDesc)


    def ReadFlexControllers(self):
        if self.theMdlFileData.flexControllerCount > 0:
            self.reader.seek(self.theMdlFileData.flexControllerOffset, 0)
            for i in range(self.theMdlFileData.flexControllerCount):
                flexControllerInputFileStreamPosition = self.reader.tell()
                aFlexController = MD.SourceMdlFlexController()
                aFlexController.typeOffset = self.reader.readInt32()
                aFlexController.nameOffset = self.reader.readInt32()
                aFlexController.localToGlobal = self.reader.readInt32()
                aFlexController.min = self.reader.readFloat()
                aFlexController.max = self.reader.readFloat()
                self.theMdlFileData.theFlexControllers.append(aFlexController)
                inputFileStreamPosition = self.reader.tell()
                if aFlexController.typeOffset != 0:
                    aFlexController.theType = self.reader.get_string_at_offset(flexControllerInputFileStreamPosition,
                                                                        aFlexController.typeOffset)
                else:
                    aFlexController.theType = ''
                if aFlexController.nameOffset != 0:
                    aFlexController.theName = self.reader.get_string_at_offset(flexControllerInputFileStreamPosition,
                                                                        aFlexController.nameOffset)
                else:
                    aFlexController.theName = 'blank_name_' + str(i)
                self.reader.seek(inputFileStreamPosition, 0)

                if self.theMdlFileData.theFlexControllers.__len__() > 0:
                    self.theMdlFileData.theModelCommandIsUsed = True


    def ReadFlexRules(self):
        self.reader.seek(self.theMdlFileData.flexRuleOffset, 0)
        for i in range(self.theMdlFileData.flexRuleCount):
            flexRuleInputFileStreamPosition = self.reader.tell()
            aFlexRule = MD.SourceMdlFlexRule()
            aFlexRule.flexIndex = self.reader.readInt32()
            aFlexRule.opCount = self.reader.readInt32()
            aFlexRule.opOffset = self.reader.readInt32()
            inputFileStreamPosition = self.reader.tell()
            if aFlexRule.opCount > 0 and aFlexRule.opOffset != 0:
                self.ReadFlexOps(flexRuleInputFileStreamPosition, aFlexRule)
            self.theMdlFileData.theFlexDescs[aFlexRule.flexIndex].theDescIsUsedByFlexRule = True
            self.theMdlFileData.theFlexRules.append(aFlexRule)
            self.reader.seek(inputFileStreamPosition, 0)

        if self.theMdlFileData.theFlexRules.__len__() > 0:
            self.theMdlFileData.theModelCommandIsUsed = True


    def ReadFlexOps(self, flexRuleInputFileStreamPosition, aFlexRule: MD.SourceMdlFlexRule):
        self.reader.seek(flexRuleInputFileStreamPosition + aFlexRule.opOffset)
        for i in range(aFlexRule.opCount):
            aFlexOp = MD.SourceMdlFlexOp()
            aFlexOp.op = self.reader.readInt32()
            if aFlexOp.op == MD.SourceMdlFlexOp.STUDIO_CONST:
                aFlexOp.value = self.reader.readFloat()
            else:
                aFlexOp.index = self.reader.readInt32()
                if aFlexOp.op == MD.SourceMdlFlexOp.STUDIO_FETCH2:
                    self.theMdlFileData.theFlexDescs[aFlexOp.index].theDescIsUsedByFlexRule = True
            aFlexRule.theFlexOps.append(aFlexOp)


    def ReadTextures(self):
        if self.theMdlFileData.textureCount > 0:
            self.reader.seek(self.theMdlFileData.textureOffset)
            for i in range(self.theMdlFileData.textureCount - 1):
                textureInputFileStreamPosition = self.reader.tell()
                aTexture = SourceMdlTexture()
                aTexture.nameOffset = self.reader.readInt32()
                aTexture.thePathFileName = self.reader.get_string_at_offset(textureInputFileStreamPosition, aTexture.nameOffset)
                aTexture.flags = self.reader.readInt32()
                aTexture.used = self.reader.readInt32()
                aTexture.unused1 = self.reader.readInt32()
                aTexture.materialP = self.reader.readInt32()
                aTexture.clientMaterialP = self.reader.readInt32()

                for _ in range(5):
                    aTexture.unused.append(self.reader.readInt32())

                self.theMdlFileData.theTextures.append(aTexture)


    def ReadTexturePaths(self):
        if self.theMdlFileData.texturePathCount > 0:
            self.reader.seek(self.theMdlFileData.texturePathOffset, 0)
            for i in range(self.theMdlFileData.texturePathCount):
                texturePathInputFileStreamPosition = self.reader.tell()
                texturePathOffset = self.reader.readInt32()
                inputFileStreamPosition = self.reader.tell()
                if texturePathOffset != 0:
                    aTexturePath = self.reader.get_string_at_offset(texturePathOffset, 0)
                else:
                    aTexturePath = ''
                self.theMdlFileData.theTexturePaths.append(aTexturePath)
                self.reader.seek(inputFileStreamPosition, 0)


if __name__ == '__main__':
    mdl = Mdl53(open(r'H:\games\Titanfall 2\extr\models\robots\super_spectre\super_spectre_v1.mdl', 'rb'))
    pprint(mdl.theMdlFileData.theBodyParts)
    # for body in mdl.theMdlFileData.theBodyParts:  # type: MD.SourceMdlBodyPart
    #     print(body.modelCount)
    #     for model in body.theModels:  # type: MD.SourceMdlModel
    #         print(model.meshCount)
    #         print(model.theMeshes)
            # pprint(mdl.theMdlFileData.theBones)
            # for bd in mdl.theMdlFileData.theBodyParts: #type: MD.SourceMdlBodyPart
            #     print(bd.theName)
            #     for model in bd.theModels: #type: MD.SourceMdlModel
            #         for mesh in model.theMeshes: #type:MD.SourceMdlMesh
            #             pprint(mesh.theFlexes)
