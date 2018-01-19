import sys



try:
    from .MDL_DATA import *
    from .ByteIO import ByteIO
    from .MDL_DATA_ANIMATIONS import *
except:
    from MDL_DATA import *
    from ByteIO import ByteIO
    from MDL_DATA_ANIMATIONS import *

class SourceMdlFile49:

    def __init__(self, filepath):
        self.reader = ByteIO(path = filepath+'.mdl')
        self.mdl = SourceMdlFileData()
        self.mdl.read(self.reader)

        self.read_bones()
        self.readBoneControllers()

        self.read_flex_descs()
        self.read_flex_controllers()
        self.readFlexRules()

        self.read_attachments()
        self.read_bone_table_by_name()

        self.read_body_parts()
        self.read_textures()
        self.read_texture_paths()
        # self.read_local_animation_descs()

        # print(self.mdl)

    def read_bones(self):
        if self.mdl.boneCount>0:
            self.reader.seek(self.mdl.boneOffset, 0)
            for i in range(self.mdl.boneCount):
                SourceMdlBone().read(self.reader, self.mdl)

    def readBoneControllers(self):
        if self.mdl.boneControllerCount>0:
            for _ in range(self.mdl.boneControllerCount):
                SourceMdlBoneController().read(self.reader, self.mdl)

    def read_flex_descs(self):
        if self.mdl.flexDescCount > 0:
            self.reader.seek(self.mdl.flexDescOffset, 0)
            for _ in range(self.mdl.flexDescCount):
                FlexDesc = SourceMdlFlexDesc()
                FlexDesc.read(self.reader)
                self.mdl.theFlexDescs.append(FlexDesc)

    def read_flex_controllers(self):
        if self.mdl.flexControllerCount > 0:
            self.reader.seek(self.mdl.flexControllerOffset, 0)
            for i in range(self.mdl.flexControllerCount):
                SourceMdlFlexController().read(self.reader, self.mdl)

    def readFlexRules(self):
        self.reader.seek(self.mdl.flexRuleOffset, 0)
        for i in range(self.mdl.flexRuleCount):
            SourceMdlFlexRule().read(self.reader, self.mdl)

    def read_attachments(self):
        if self.mdl.localAttachmentCount>0:
            self.reader.seek(self.mdl.localAttachmentOffset, 0)
            for _ in range(self.mdl.localAttachmentCount):
                SourceMdlAttachment().read(self.reader, self.mdl)

    def read_bone_table_by_name(self):
        self.reader.seek(self.mdl.boneTableByNameOffset)
        if self.mdl.boneTableByNameOffset != 0:
            for i in range(self.mdl.boneCount):
                index = self.reader.read_uint8()
                self.mdl.theBoneTableByName.append(index)

    def read_body_parts(self):
        if self.mdl.bodyPartCount>0:
            self.reader.seek(self.mdl.bodyPartOffset)
            for _ in range(self.mdl.bodyPartCount):
                SourceMdlBodyPart().read(self.reader,self.mdl)

    def read_textures(self):
        if self.mdl.textureCount<1:
            return
        self.reader.seek(self.mdl.textureOffset)
        for _ in range(self.mdl.textureCount):
            SourceMdlTexture().read(self.reader,self.mdl)

    def read_texture_paths(self):
        if self.mdl.texturePathCount>0:
            self.reader.seek(self.mdl.texturePathOffset)
            for _ in range(self.mdl.texturePathCount):
                texturePathOffset = self.reader.read_uint32()
                entry = self.reader.tell()
                if texturePathOffset!=0:
                    self.mdl.theTexturePaths.append(self.reader.read_from_offset(texturePathOffset,self.reader.read_ascii_string))
                else:
                    self.mdl.theTexturePaths.append("")
                self.reader.seek(entry)

    def read_local_animation_descs(self):
        self.reader.seek(self.mdl.localAnimationOffset)
        with self.reader.save_current_pos():
            for _ in range(self.mdl.localAnimationCount):
                self.mdl.theAnimationDescs.append(SourceMdlAnimationDesc49().read(self.reader,self.mdl))
        self.read_animations()

    def read_animations(self):
        for i in range(self.mdl.localAnimationCount):

            anim_desc = self.mdl.theAnimationDescs[i]# type: SourceMdlAnimationDesc49
            anim_desc.theSectionsOfAnimations = [[]]
            entry = anim_desc.entry + i*anim_desc.size

            if anim_desc.flags.flag & anim_desc.STUDIO.ALLZEROS ==0:

                if anim_desc.flags.flag & anim_desc.STUDIO.FRAMEANIM!=0:
                    if anim_desc.sectionOffset!=0 and anim_desc.sectionFrameCount>0:
                        self.mdl.theSectionFrameCount = anim_desc.sectionFrameCount
                        if self.mdl.theSectionFrameMinFrameCount >= anim_desc.frameCount:
                            self.mdl.theSectionFrameMinFrameCount = anim_desc.frameCount-1
                        sectionCount = math.trunc(anim_desc.frameCount / anim_desc.sectionFrameCount) + 2
                        for sectionIndex in range(sectionCount):
                            anim_desc.theSectionsOfAnimations.append([])
                        with self.reader.save_current_pos():
                            self.reader.seek(entry+anim_desc.sectionOffset)
                            for _ in range(sectionCount):
                                anim_desc.theSections.append(SourceMdlAnimationSection().read(self.reader))
                else:
                    if anim_desc.sectionOffset != 0 and anim_desc.sectionFrameCount > 0:
                        self.mdl.theSectionFrameCount = anim_desc.sectionFrameCount
                        if self.mdl.theSectionFrameMinFrameCount >= anim_desc.frameCount:
                            self.mdl.theSectionFrameMinFrameCount = anim_desc.frameCount - 1
                        sectionCount = math.trunc(anim_desc.frameCount / anim_desc.sectionFrameCount) + 2
                        print(sectionCount)
                        for sectionIndex in range(sectionCount):
                            anim_desc.theSectionsOfAnimations.append([])
                        with self.reader.save_current_pos():
                            self.reader.seek(entry + anim_desc.sectionOffset)
                            for _ in range(sectionCount):
                                anim_desc.theSections.append(SourceMdlAnimationSection().read(self.reader))
                    if anim_desc.animBlock == 0:
                        with self.reader.save_current_pos():
                            self.reader.seek(entry+anim_desc.animOffset)
                            for _ in range(self.mdl.boneCount):
                                entry_anim = self.reader.tell()
                                anim = SourceMdlAnimation().read(anim_desc.frameCount,anim_desc.theSectionsOfAnimations[0],self.mdl,self.reader)




            pprint(anim_desc.__dict__)


    def test(self):
        pass
        # print(self.mdl.theAnimationDescs)
        # for part in self.mdl.theBodyParts: # type: SourceMdlBodyPart
        #     for model in part.theModels: # type: SourceMdlModel
        #         for mesh in model.theMeshes: # type: SourceMdlMesh
        #             print(mesh.materialIndex)
        # for m in self.mdl.theTextures: #type: SourceMdlTexture
        #     print(m)

class SourceMdlFile53(SourceMdlFile49):

    def __init__(self, path):
        self.reader = ByteIO(path = path+'.mdl')
        self.mdl = SourceMdlFileDataV53()
        self.mdl.read(self.reader)
        self.VVD = self.mdl.VVD
        self.VTX = self.mdl.VTX
        self.read_bones()
        self.readBoneControllers()

        self.read_flex_descs()
        self.read_flex_controllers()
        self.readFlexRules()

        self.read_attachments()
        self.read_bone_table_by_name()

        self.read_body_parts()
        self.read_textures()
        self.read_texture_paths()


if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            a = SourceMdlFile49(r'.\test_data\orisa_classic')
            a.test()
            # print(a.mdl)
