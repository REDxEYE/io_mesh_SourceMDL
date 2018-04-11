import sys, os.path

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
        self.reader = ByteIO(path=filepath + '.mdl')
        self.filename = os.path.basename(filepath + '.mdl')[:-4]
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
        self.build_flex_frames()
        # self.read_local_animation_descs()
        # self.read_sequences()

        # print(self.mdl)

    def read_bones(self):
        print('Reading bones')
        if self.mdl.boneCount > 0:
            self.reader.seek(self.mdl.boneOffset, 0)
            for i in range(self.mdl.boneCount):
                SourceMdlBone().read(self.reader, self.mdl)

    def readBoneControllers(self):
        print('Reading Bone Controllers')
        if self.mdl.boneControllerCount > 0:
            for _ in range(self.mdl.boneControllerCount):
                SourceMdlBoneController().read(self.reader, self.mdl)

    def read_flex_descs(self):
        print('Reading flex descs')
        if self.mdl.flexDescCount > 0:
            self.reader.seek(self.mdl.flexDescOffset, 0)
            for _ in range(self.mdl.flexDescCount):
                FlexDesc = SourceMdlFlexDesc()
                FlexDesc.read(self.reader)
                self.mdl.theFlexDescs.append(FlexDesc)

    def read_flex_controllers(self):
        print("Reading flex controllers")
        if self.mdl.flexControllerCount > 0:
            self.reader.seek(self.mdl.flexControllerOffset, 0)
            for i in range(self.mdl.flexControllerCount):
                SourceMdlFlexController().read(self.reader, self.mdl)

    def readFlexRules(self):
        print('Reading flex rules')
        self.reader.seek(self.mdl.flexRuleOffset, 0)
        for i in range(self.mdl.flexRuleCount):
            SourceMdlFlexRule().read(self.reader, self.mdl)

    def read_attachments(self):
        print('Reading attachments')
        if self.mdl.localAttachmentCount > 0:
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
        print('Readding body parts')
        if self.mdl.bodyPartCount > 0:
            self.reader.seek(self.mdl.bodyPartOffset)
            for _ in range(self.mdl.bodyPartCount):
                SourceMdlBodyPart().read(self.reader, self.mdl)

    def read_textures(self):
        if self.mdl.textureCount < 1:
            return
        self.reader.seek(self.mdl.textureOffset)
        for _ in range(self.mdl.textureCount):
            SourceMdlTexture().read(self.reader, self.mdl)

    def read_texture_paths(self):
        if self.mdl.texturePathCount > 0:
            self.reader.seek(self.mdl.texturePathOffset)
            for _ in range(self.mdl.texturePathCount):
                texturePathOffset = self.reader.read_uint32()
                entry = self.reader.tell()
                if texturePathOffset != 0:
                    self.mdl.theTexturePaths.append(
                        self.reader.read_from_offset(texturePathOffset, self.reader.read_ascii_string))
                else:
                    self.mdl.theTexturePaths.append("")
                self.reader.seek(entry)

    def read_local_animation_descs(self):
        self.reader.seek(self.mdl.localAnimationOffset)
        with self.reader.save_current_pos():
            for _ in range(self.mdl.localAnimationCount):
                self.mdl.theAnimationDescs.append(SourceMdlAnimationDesc49().read(self.reader, self.mdl))
        self.read_animations()

    def read_sequences(self):
        with self.reader.save_current_pos():
            self.reader.seek(self.mdl.localSequenceOffset)
            for _ in range(self.mdl.localSequenceCount):
                self.mdl.theSequenceDescs.append(SourceMdlSequenceDesc().read(self.reader, self.mdl))

    def read_animations(self):
        for i in range(self.mdl.localAnimationCount):
            anim_desc = self.mdl.theAnimationDescs[i]  # type: SourceMdlAnimationDesc49
            print('Reading anim', anim_desc.theName, 'flags', anim_desc.flags.get_flags)
            print(anim_desc)
            anim_desc.theSectionsOfAnimations = [[]]
            entry = anim_desc.entry + i * anim_desc.size

            if anim_desc.flags.flag & anim_desc.STUDIO.ALLZEROS == 0:

                if anim_desc.flags.flag & anim_desc.STUDIO.FRAMEANIM != 0:
                    if anim_desc.sectionOffset != 0 and anim_desc.sectionFrameCount > 0:
                        self.mdl.theSectionFrameCount = anim_desc.sectionFrameCount
                        if self.mdl.theSectionFrameMinFrameCount >= anim_desc.frameCount:
                            self.mdl.theSectionFrameMinFrameCount = anim_desc.frameCount - 1
                        sectionCount = math.trunc(anim_desc.frameCount / anim_desc.sectionFrameCount) + 2
                        for sectionIndex in range(sectionCount):
                            anim_desc.theSectionsOfAnimations.append([])
                        with self.reader.save_current_pos():
                            self.reader.seek(entry + anim_desc.sectionOffset)
                            for _ in range(sectionCount):
                                pass
                                anim_desc.theSections.append(SourceMdlAnimationSection().read(self.reader))
                else:
                    if anim_desc.sectionOffset != 0 and anim_desc.sectionFrameCount > 0:
                        self.mdl.theSectionFrameCount = anim_desc.sectionFrameCount
                        if self.mdl.theSectionFrameMinFrameCount >= anim_desc.frameCount:
                            self.mdl.theSectionFrameMinFrameCount = anim_desc.frameCount - 1
                        sectionCount = math.trunc(anim_desc.frameCount / anim_desc.sectionFrameCount) + 2
                        # print(sectionCount)
                        for sectionIndex in range(sectionCount):
                            anim_desc.theSectionsOfAnimations.append([])
                        with self.reader.save_current_pos():
                            self.reader.seek(entry + anim_desc.sectionOffset)
                            for _ in range(sectionCount):
                                pass
                                anim_desc.theSections.append(SourceMdlAnimationSection().read(self.reader))
                    if anim_desc.animBlock == 0:
                        with self.reader.save_current_pos():
                            self.reader.seek(entry + anim_desc.animOffset)
                            for _ in range(self.mdl.boneCount):
                                entry_anim = self.reader.tell()
                                print('Trying to read animation from offset', entry_anim)
                                pass
                                anim, stat = SourceMdlAnimation().read(anim_desc.frameCount,
                                                                       anim_desc.theSectionsOfAnimations[0], self.mdl,
                                                                       self.reader)
                                if stat == -1:
                                    print('Success, breaking the loop')
                                    break
                                if stat == 1:
                                    anim_desc.theSectionsOfAnimations.append(anim)
                                if stat == 0:
                                    print('ERROR, breaking the loop')
                                    break

            # pprint(anim_desc.__dict__)

    def test(self):
        pass
        # for flex_rule in self.mdl.theFlexRules:
        #     print(flex_rule)
        #     print(self.mdl.theFlexDescs[flex_rule.flexIndex])
        #     print(self.mdl.theFlexControllers[flex_rule.flexIndex])
        # for flex_cont in self.mdl.theFlexControllers:
        #     print(flex_cont)
        # print(self.mdl.theFlexDescs[flex_rule.flexIndex])
        # for flex_dest in self.mdl.theFlexDescs:
        #     print(flex_dest)
        # for bone in self.mdl.theBones:
        #     print(bone)
        # print(self.mdl.theAnimationDescs)
        for part in self.mdl.theBodyParts:  # type: SourceMdlBodyPart
            print(part.theName, "list of meshes in bodygroup")
            for model in part.theModels:  # type: SourceMdlModel
                print(model.name)
                pprint(model.flex_frames)
                # print('\t', model.name, 'list of flexes in this mesh:')
                # for mesh in model.theMeshes:  # type: SourceMdlMesh
                #     for flex in mesh.theFlexes:  # type: SourceMdlFlex
                #         print('\t\t', flex, self.mdl.theFlexDescs[flex.flexDescIndex])
        # for m in self.mdl.theTextures: #type: SourceMdlTexture
        #     print(m)

    def build_flex_frames(self):
        print('Building flex frames')
        cumulative_vertex_offset = 0
        flex_dest_flex_frame = []  # type:List[List[FlexFrame]]

        for x in range(len(self.mdl.theFlexDescs)):
            flex_dest_flex_frame.append([])

        for body_part in self.mdl.theBodyParts:
            print('Building flex frame for {}'.format(body_part.theName))
            for model in body_part.theModels:
                print('Processing model {}'.format(model.name))
                for mesh in model.theMeshes:
                    vertex_offset = mesh.vertexIndexStart
                    # print(vertex_offset)
                    for flex_index, flex in enumerate(mesh.theFlexes):
                        print('\tParsing {} flex from {}'.format(self.mdl.theFlexDescs[flex.flexDescIndex].theName,model.name))
                        flex_frame = None
                        if flex_dest_flex_frame[flex.flexDescIndex]:
                            for s_flex in flex_dest_flex_frame[flex.flexDescIndex]:
                                if s_flex.flexes[0].target0 == flex.target0 and \
                                        s_flex.flexes[0].target1 == flex.target1 and \
                                        s_flex.flexes[0].target2 == flex.target2 and \
                                        s_flex.flexes[0].target3 == flex.target3:
                                    flex_frame = s_flex

                        if not flex_frame:
                            flex_frame = FlexFrame()
                            flex_frame.flex_name = self.mdl.theFlexDescs[flex.flexDescIndex].theName[:-1]
                            flex_desc_partner_index = mesh.theFlexes[flex_index].flexDescPartnerIndex
                            if flex_desc_partner_index>0:
                                flex_frame.has_partner = True
                                flex_frame.partner = flex_desc_partner_index
                            flex_dest_flex_frame[flex.flexDescIndex].append(flex_frame)
                        flex_frame.vertex_offsets.append(vertex_offset + cumulative_vertex_offset)
                        flex_frame.flexes.append(flex)
                        model.flex_frames.append(flex_frame)


                cumulative_vertex_offset += model.vertexCount



class SourceMdlFile53(SourceMdlFile49):

    def __init__(self, filepath):
        self.reader = ByteIO(path=filepath + '.mdl')
        self.filename = os.path.basename(filepath + '.mdl')[:-4]
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
        self.read_sequences()

    def test(self):
        for sq in self.mdl.theSequenceDescs:
            print(sq.__dict__)


if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            # a = SourceMdlFile53(r'H:\games\Titanfall 2\extr\models\weapons\titan_sniper_rifle\w_titan_sniper_rifle')
            a = SourceMdlFile49(
                r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod\models\undertale\undyne_bigger_nude')
            # a = SourceMdlFile49(r'.\test_data\nick_hwm')
            # a = SourceMdlFile49(r'.\test_data\xenomorph')
            # mdl2 = SourceMdlFile53(r'.\test_data\titan_buddy')
            # mdl2.test()
            a.test()
            # print(a.mdl)
