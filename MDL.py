import os.path

try:
    from .MDL_DATA import *
    from .ByteIO import *
    from .MDL_DATA_ANIMATIONS import *
except ImportError:
    from MDL_DATA import *
    from ByteIO import *
    from MDL_DATA_ANIMATIONS import *


class SourceMdlFile49:

    def __init__(self, filepath):
        self.reader = ByteIO(path=filepath + '.mdl', copy_data_from_handle=False, )
        self.filename = os.path.basename(filepath + '.mdl')[:-4]
        self.file_data = SourceMdlFileData()
        self.file_data.read(self.reader)
        self.read_bones()
        self.read_bone_controllers()

        self.read_flex_descs()
        self.read_flex_controllers()
        self.read_flex_rules()

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
        if self.file_data.bone_count > 0:
            self.reader.seek(self.file_data.bone_offset, 0)
            for i in range(self.file_data.bone_count):
                SourceMdlBone().read(self.reader, self.file_data)

    def read_bone_controllers(self):
        print('Reading Bone Controllers')
        if self.file_data.bone_controller_count > 0:
            for _ in range(self.file_data.bone_controller_count):
                SourceMdlBoneController().read(self.reader, self.file_data)

    def read_flex_descs(self):
        print('Reading flex descs')
        if self.file_data.flex_desc_count > 0:
            self.reader.seek(self.file_data.flex_desc_offset, 0)
            for _ in range(self.file_data.flex_desc_count):
                flex_desc = SourceMdlFlexDesc()
                flex_desc.read(self.reader)
                self.file_data.flex_descs.append(flex_desc)

    def read_flex_controllers(self):
        print("Reading flex controllers")
        if self.file_data.flex_controller_count > 0:
            self.reader.seek(self.file_data.flex_controller_offset, 0)
            for i in range(self.file_data.flex_controller_count):
                SourceMdlFlexController().read(self.reader, self.file_data)

    def read_flex_rules(self):
        print('Reading flex rules')
        self.reader.seek(self.file_data.flex_rule_offset, 0)
        for i in range(self.file_data.flex_rule_count):
            SourceMdlFlexRule().read(self.reader, self.file_data)

    def read_attachments(self):
        print('Reading attachments')
        if self.file_data.local_attachment_count > 0:
            self.reader.seek(self.file_data.local_attachment_offset, 0)
            for _ in range(self.file_data.local_attachment_count):
                SourceMdlAttachment().read(self.reader, self.file_data)

    def read_bone_table_by_name(self):
        self.reader.seek(self.file_data.bone_table_by_name_offset)
        if self.file_data.bone_table_by_name_offset != 0:
            for i in range(self.file_data.bone_count):
                index = self.reader.read_uint8()
                self.file_data.bone_table_by_name.append(index)

    def read_body_parts(self):
        print('Reading body parts')
        if self.file_data.body_part_count > 0:
            self.reader.seek(self.file_data.body_part_offset)
            for _ in range(self.file_data.body_part_count):
                SourceMdlBodyPart().read(self.reader, self.file_data)

    def read_textures(self):
        if self.file_data.texture_count < 1:
            return
        self.reader.seek(self.file_data.texture_offset)
        for _ in range(self.file_data.texture_count):
            SourceMdlTexture().read(self.reader, self.file_data)

    def read_texture_paths(self):
        if self.file_data.texture_path_count > 0:
            self.reader.seek(self.file_data.texture_path_offset)
            for _ in range(self.file_data.texture_path_count):
                texture_path_offset = self.reader.read_uint32()
                entry = self.reader.tell()
                if texture_path_offset != 0:
                    self.file_data.texture_paths.append(
                        self.reader.read_from_offset(texture_path_offset, self.reader.read_ascii_string))
                else:
                    self.file_data.texture_paths.append("")
                self.reader.seek(entry)

    def read_local_animation_descs(self):
        self.reader.seek(self.file_data.local_animation_offset)
        with self.reader.save_current_pos():
            for _ in range(self.file_data.local_animation_count):
                self.file_data.animation_descs.append(SourceMdlAnimationDesc49().read(self.reader, self.file_data))
        self.read_animations()

    def read_sequences(self):
        with self.reader.save_current_pos():
            self.reader.seek(self.file_data.local_sequence_offset)
            for _ in range(self.file_data.local_sequence_count):
                self.file_data.sequence_descs.append(SourceMdlSequenceDesc().read(self.reader, self.file_data))

    def read_animations(self):
        for i in range(self.file_data.local_animation_count):
            anim_desc = self.file_data.animation_descs[i]  # type: SourceMdlAnimationDesc49
            print('Reading anim', anim_desc.theName, 'flags', anim_desc.flags.get_flags)
            print(anim_desc)
            anim_desc.theSectionsOfAnimations = [[]]
            entry = anim_desc.entry + i * anim_desc.size

            if anim_desc.flags.flag & anim_desc.STUDIO.ALLZEROS == 0:

                if anim_desc.flags.flag & anim_desc.STUDIO.FRAMEANIM != 0:
                    if anim_desc.sectionOffset != 0 and anim_desc.sectionFrameCount > 0:
                        self.file_data.section_frame_count = anim_desc.sectionFrameCount
                        if self.file_data.section_frame_min_frame_count >= anim_desc.frameCount:
                            self.file_data.section_frame_min_frame_count = anim_desc.frameCount - 1
                        section_count = math.trunc(anim_desc.frameCount / anim_desc.sectionFrameCount) + 2
                        for sectionIndex in range(section_count):
                            anim_desc.theSectionsOfAnimations.append([])
                        with self.reader.save_current_pos():
                            self.reader.seek(entry + anim_desc.sectionOffset)
                            for _ in range(section_count):
                                pass
                                anim_desc.theSections.append(SourceMdlAnimationSection().read(self.reader))
                else:
                    if anim_desc.sectionOffset != 0 and anim_desc.sectionFrameCount > 0:
                        self.file_data.section_frame_count = anim_desc.sectionFrameCount
                        if self.file_data.section_frame_min_frame_count >= anim_desc.frameCount:
                            self.file_data.section_frame_min_frame_count = anim_desc.frameCount - 1
                        section_count = math.trunc(anim_desc.frameCount / anim_desc.sectionFrameCount) + 2
                        # print(section_count)
                        for sectionIndex in range(section_count):
                            anim_desc.theSectionsOfAnimations.append([])
                        with self.reader.save_current_pos():
                            self.reader.seek(entry + anim_desc.sectionOffset)
                            for _ in range(section_count):
                                pass
                                anim_desc.theSections.append(SourceMdlAnimationSection().read(self.reader))
                    if anim_desc.animBlock == 0:
                        with self.reader.save_current_pos():
                            self.reader.seek(entry + anim_desc.animOffset)
                            for _ in range(self.file_data.bone_count):
                                entry_anim = self.reader.tell()
                                print('Trying to read animation from offset', entry_anim)
                                pass
                                anim, stat = SourceMdlAnimation().read(anim_desc.frameCount,
                                                                       anim_desc.theSectionsOfAnimations[0],
                                                                       self.file_data,
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
        # self.mdl.bone_count.value = 1
        # self.mdl.name.value = r'red_eye\nick_HW2.mdl'
        # print(repr(self.mdl.bone_count))
        # print(repr(self.mdl.name))
        # for bone in self.mdl.theBones:
        #     print(bone)
        # for attachment in self.mdl.theAttachments:
        #     print(attachment)
        # print(self.mdl.theAnimationDescs)
        # for part in self.mdl.theBodyParts:  # type: SourceMdlBodyPart
        #     print("list of models in \"{}\" bodygroup".format(part.name))
        #     for model in part.models:  # type: SourceMdlModel
        #         print('\tmodel:', model.name)
        #         # print('\teyeball count:',model.eyeball_count)
        #         # pprint(model.flex_frames)
        #         for flex_frame in model.flex_frames:
        #             print('\t', flex_frame)
        # print('\t', model.name, 'list of flexes in this mesh:')
        # for mesh in model.meshes:  # type: SourceMdlMesh
        #     for flex in mesh.flexes:  # type: SourceMdlFlex
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
        for x in range(len(self.file_data.flex_descs)):
            flex_dest_flex_frame.append([])

        cumulative_vertex_offset = 0
        for body_part in self.file_data.body_parts:
            print('Building flex frame for {}'.format(body_part.name))
            # No need to create defaultflex here.

            for model in body_part.models:
                print('\tProcessing model {}'.format(model.name))

                for mesh in model.meshes:
                    vertex_offset = mesh.vertex_index_start

                    for flex_index, flex in enumerate(mesh.flexes):
                        # print('\t\tParsing {} flex from {}'.format(self.mdl.theFlexDescs[flex.flexDescIndex].name,
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
                            flex_frame.flex_name = self.file_data.flex_descs[flex.flexDescIndex].name
                            flex_desc_partner_index = mesh.flexes[flex_index].flexDescPartnerIndex

                            if flex_desc_partner_index > 0:
                                # aFlexFrame.flexDescription is skipped, because addon don't need this
                                # False by default -------┐
                                #                         ▼
                                flex_frame.has_partner = True
                                flex_frame.partner = flex_desc_partner_index

                            flex_dest_flex_frame[flex.flexDescIndex].append(flex_frame)

                        # aFlexFrame.bodyAndMeshVertexIndexStarts.Add(meshVertexIndexStart +
                        # + cumulativebodyPartVertexIndexStart)
                        # aFlexFrame.flexes.Add(aFlex)
                        flex_frame.vertex_offsets.append(vertex_offset + cumulative_vertex_offset)
                        flex_frame.flexes.append(flex)
                        # Adding flex frames to bodymodel instead of bodypart
                        model.flex_frames.append(flex_frame)

                cumulative_vertex_offset += model.vertex_count

    @staticmethod
    def comp_flex_frames(flex_frame1, flex_frame2):
        if len(flex_frame1) != len(flex_frame2):
            return False
        for flex1, flex2 in zip(flex_frame1, flex_frame2):
            if flex1 != flex2:
                return False
        return True

    def prepare_models(self):
        for n, body_part in enumerate(self.file_data.body_parts):
            if body_part.model_count > 1:
                self.file_data.bodypart_frames.append([(n, body_part)])
                continue
            model = body_part.models[0]
            added = False
            for bodyparts in self.file_data.bodypart_frames:
                for _, _model in bodyparts:
                    if self.comp_flex_frames(model.flex_frames, _model.models[0].flex_frames):
                        bodyparts.append((n, body_part))
                        added = True
                        break
            if not added:
                self.file_data.bodypart_frames.append([(n, body_part)])


class SourceMdlFile53(SourceMdlFile49):
    # Super class call does not required here due to different __init__ behaviour
    # noinspection PyMissingConstructor
    def __init__(self, path):
        self.reader = ByteIO(path=path + '.mdl')
        self.filename = os.path.basename(path + '.mdl')[:-4]
        self.file_data = SourceMdlFileDataV53()
        self.file_data.read(self.reader)
        self.VVD = self.file_data.vvd
        self.VTX = self.file_data.vtx
        self.read_bones()
        self.read_bone_controllers()

        self.read_flex_descs()
        self.read_flex_controllers()
        self.read_flex_rules()

        self.read_attachments()
        self.read_bone_table_by_name()

        self.read_body_parts()
        self.read_textures()
        self.read_texture_paths()
        self.build_flex_frames()
        self.prepare_models()
        # self.read_sequences()

    def test(self):
        for sq in self.file_data.sequence_descs:
            print(sq.__dict__)
        for bone in self.file_data.bones:
            print(bone)


if __name__ == '__main__':
    # with open('log.log', "w",encoding='utf8') as f:  # replace filepath & filename
    #     with f as sys.stdout:
    # model_path = r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\tf_movies\models\player\hwm\medic'
    # model_path = r'.\test_data\nick_hw2'
    # model_path = r'.\test_data\reimu_v2'
    # model_path = r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\usermod\models\bge\narry\zach_water_v3'
    model_path = r'.\test_data\hard_suit'
    # model_path = r'H:\games\Titanfall 2\extr\models\weapons\titan_sniper_rifle\w_titan_sniper_rifle'
    # model_path = r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\workshop\models\player\asrielflex'
    # model_path = r'G:\SteamLibrary\SteamApps\common\SourceFilmmaker\game\tf_movies\models\player\hwm\spy'
    # model_path = r'.\test_data\test_case-2models-with-flexes'
    a = SourceMdlFile49(model_path)
    a.test()

    # mdl2 = SourceMdlFile53(model_path)
    # mdl2.test()
    # print(a.mdl)
