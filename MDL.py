import sys, os.path

try:
    from .MDL_DATA import *
    from .ByteIO import *
    from .MDL_DATA_ANIMATIONS import *
except:
    from MDL_DATA import *
    from ByteIO import *
    from MDL_DATA_ANIMATIONS import *


class SourceMdlFile49:

    def __init__(self, filepath):
        self.reader = ByteIO(path=filepath + '.mdl',copy_data_from_handle=False,)
        self.filename = os.path.basename(filepath + '.mdl')[:-4]
        self.mdl = SourceMdlFileData()
        self.mdl.read(self.reader)
        # print(self)
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
        self.prepare_models()
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
        # for n,model in enumerate(self.mdl.bodyparts):
        #     print(n,' ',end = '')
        #     pprint(model)
        # GenericUInt.set_reader(self.reader)
        # GenericString.set_reader(self.reader)
        # self.mdl.boneCount.value = 1
        # self.mdl.name.value = r'red_eye\nick_HW2.mdl'
        # print(repr(self.mdl.boneCount))
        # print(repr(self.mdl.name))
        for bone in self.mdl.theBones:
            print(bone)
        # for attachment in self.mdl.theAttachments:
        #     print(attachment)
        # print(self.mdl.theAnimationDescs)
        # for part in self.mdl.theBodyParts:  # type: SourceMdlBodyPart
        #     print("list of models in \"{}\" bodygroup".format(part.theName))
        #     for model in part.theModels:  # type: SourceMdlModel
        #         print('\tmodel:', model.name)
        #         # print('\teyeball count:',model.eyeballCount)
        #         # pprint(model.flex_frames)
        #         for flex_frame in model.flex_frames:
        #             print('\t', flex_frame)
                # print('\t', model.name, 'list of flexes in this mesh:')
                # for mesh in model.theMeshes:  # type: SourceMdlMesh
                #     for flex in mesh.theFlexes:  # type: SourceMdlFlex
                #         print('\t\t', flex, self.mdl.theFlexDescs[flex.flexDescIndex])
        # for m in self.mdl.theTextures: #type: SourceMdlTexture
        #     print(m)

    def build_flex_frames(self):
        print('Building flex frames')

        # flexDescToFlexFrames = New List(Of List(Of FlexFrame))(Me.theMdlFileData.theFlexDescs.Count)
        # For x As Integer = 0 To Me.theMdlFileData.theFlexDescs.Count - 1
        # 	Dim flexFrameList As New List(Of FlexFrame)()
        # 	flexDescToFlexFrames.Add(flexFrameList)
        # Next ----┐
        #          ▼
        flex_dest_flex_frame = []  # type:List[List[FlexFrame]]
        for x in range(len(self.mdl.theFlexDescs)):
            flex_dest_flex_frame.append([])

        cumulative_vertex_offset = 0
        for body_part in self.mdl.theBodyParts:
            print('Building flex frame for {}'.format(body_part.theName))
            # No need to create defaultflex here.

            for model in body_part.theModels:
                print('\tProcessing model {}'.format(model.name))

                for mesh in model.theMeshes:
                    vertex_offset = mesh.vertexIndexStart

                    for flex_index, flex in enumerate(mesh.theFlexes):
                        # print('\t\tParsing {} flex from {}'.format(self.mdl.theFlexDescs[flex.flexDescIndex].theName,
                        #                                          model.name))
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
                            flex_frame.flex_name = self.mdl.theFlexDescs[flex.flexDescIndex].theName
                            flex_desc_partner_index = mesh.theFlexes[flex_index].flexDescPartnerIndex

                            if flex_desc_partner_index > 0:
                                # aFlexFrame.flexDescription is skipped, because addon don't need this
                                # False by default -------┐
                                #                         ▼
                                flex_frame.has_partner = True
                                flex_frame.partner = flex_desc_partner_index

                            flex_dest_flex_frame[flex.flexDescIndex].append(flex_frame)

                        # aFlexFrame.bodyAndMeshVertexIndexStarts.Add(meshVertexIndexStart + cumulativebodyPartVertexIndexStart)
                        # aFlexFrame.flexes.Add(aFlex)
                        flex_frame.vertex_offsets.append(vertex_offset + cumulative_vertex_offset)
                        flex_frame.flexes.append(flex)
                        # Adding flex frames to bodymodel instead of bodypart
                        model.flex_frames.append(flex_frame)

                cumulative_vertex_offset += model.vertexCount
    @staticmethod
    def comp_flex_frames(f1,f2):
        if len(f1)!=len(f2):
            return False
        for a,b in zip(f1,f2):
            if a!=b:
                return False
        return True

    def prepare_models(self):
        for n,bodypart in enumerate(self.mdl.theBodyParts):
            if bodypart.modelCount>1:
                self.mdl.bodyparts.append([(n,bodypart)])
                continue
            model = bodypart.theModels[0]
            added = False
            for bodyparts in self.mdl.bodyparts:
                for _,_model in bodyparts:
                    if self.comp_flex_frames(model.flex_frames,_model.theModels[0].flex_frames):
                        bodyparts.append((n,bodypart))
                        added = True
                        break
            if not added:
                self.mdl.bodyparts.append([(n,bodypart)])




class SourceMdlFile53(SourceMdlFile49):

    def __init__(self, path):
        self.reader = ByteIO(path=path + '.mdl')
        self.filename = os.path.basename(path + '.mdl')[:-4]
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
        self.build_flex_frames()
        self.prepare_models()
        # self.read_sequences()



    def test(self):
        for sq in self.mdl.theSequenceDescs:
            print(sq.__dict__)
        for bone in self.mdl.theBones:
            print(bone)


if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            # model = r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\tf_movies\models\player\hwm\medic'
            # model = r'.\test_data\nick_hw2'
            # model = r'.\test_data\xenomorph'
            model = r'H:\games\Titanfall 2\extr\models\weapons\titan_sniper_rifle\w_titan_sniper_rifle'
            # model = r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\workshop\models\player\asrielflex'
            # model = r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\tf_movies\models\player\hwm\spy'
            # model = r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod\models\MMmallow\KerriganSuccubusHOTS\kerrigansuccubus'
            # model = r'.\test_data\test_case-2models-with-flexes'
            # a = SourceMdlFile49(model)
            # a.test()

            mdl2 = SourceMdlFile53(model)
            mdl2.test()
            # print(a.mdl)
