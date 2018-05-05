import io
import os.path
import random
import struct
import time
from contextlib import redirect_stdout

try:
    from . import VVD, VVD_DATA, VTX, MDL, MDL_DATA, VTX_DATA, GLOBALS, progressBar
    from . import math_utilities
except ImportError:
    import sys

    sys.path.append(r'E:\PYTHON\MDL_reader\rewrite')
    import VVD
    import VVD_DATA
    import VTX
    import MDL
    import MDL_DATA
    import VTX_DATA
    import GLOBALS
    import progressBar
    import math_utilities

# Blender imports
try:
    import bpy

    # bpy.app.debug = True
    import mathutils
    from mathutils import Vector, Matrix, Euler
except ImportError:
    raise Exception("Cannot be run without bpy (blender) module")

stdout = io.StringIO()


def split(array, n=3):
    return [array[i:i + n] for i in range(0, len(array), n)]


class IOMdl:
    def __init__(self, path: str = None, import_textures=False, working_directory=None, co=None, rot=False,
                 internal_files=None,
                 custom_name=None, normal_bones=False,join_clamped = False):
        # TODO: make import_textures to do stuff
        self.import_textures = import_textures
        # TODO: make working_directory to do something useful
        self.working_directory = working_directory
        # TODO: recall what this this is for
        self.internal_files = internal_files

        self.join_clamped = join_clamped

        self.name = os.path.basename(path)[:-4]
        self.co = co
        self.rot = rot
        self.vertex_offset = 0
        with open(path, 'rb') as fp:
            fp.read(4)
            version = struct.unpack('i', fp.read(4))[0]

        file_path = path.replace('.dx90', "")[:-4]
        self.MDL = None  # type: MDL.SourceMdlFile49
        self.VVD = None  # type: VVD.SourceVvdFile49
        self.VTX = None  # type: VTX.SourceVtxFile49
        if version == 53:
            print('Found Titanfall2 model_path')
            self.MDL = MDL.SourceMdlFile53(path=file_path)
            self.VVD = self.MDL.VVD
            self.VTX = self.MDL.VTX

        elif version < 53:
            if path:
                self.VVD = VVD.SourceVvdFile49(file_path)
                self.VTX = VTX.SourceVtxFile49(file_path)
                self.MDL = MDL.SourceMdlFile49(file_path)

        self.armature_obj = None
        self.armature = None
        self.create_skeleton(normal_bones)
        if custom_name:
            self.armature_obj.name = custom_name
        self.mesh_obj = None
        self.mesh = None
        self.create_models()
        self.create_attachments()

    def create_skeleton(self, normal_bones=False):

        bpy.ops.object.armature_add(enter_editmode=True)

        self.armature_obj = bpy.context.object
        self.armature_obj.show_x_ray = True
        self.armature_obj.name = self.name + '_ARM'

        self.armature = self.armature_obj.data
        self.armature.name = self.name + "_ARM_DATA"
        self.armature.edit_bones.remove(self.armature.edit_bones[0])

        bpy.ops.object.mode_set(mode='EDIT')
        bones = []
        for se_bone in self.MDL.file_data.bones:  # type: MDL_DATA.SourceMdlBone
            bones.append((self.armature.edit_bones.new(se_bone.name), se_bone))

        for bl_bone, se_bone in bones:  # type: bpy.types.EditBone, MDL_DATA.SourceMdlBone
            if se_bone.parentBoneIndex != -1:
                bl_parent, parent = bones[se_bone.parentBoneIndex]
                bl_bone.parent = bl_parent
            else:
                pass
            bl_bone.tail = Vector([0, 0, 1]) + bl_bone.head

        bpy.ops.object.mode_set(mode='POSE')
        for se_bone in self.MDL.file_data.bones:  # type: MDL_DATA.SourceMdlBone
            bl_bone = self.armature_obj.pose.bones.get(se_bone.name)
            pos = Vector([se_bone.position.x, se_bone.position.y, se_bone.position.z])
            rot = Euler([se_bone.rotation.x, se_bone.rotation.y, se_bone.rotation.z])
            mat = Matrix.Translation(pos) * rot.to_matrix().to_4x4()
            bl_bone.matrix_basis.identity()
            if bl_bone.parent:
                bl_bone.matrix = bl_bone.parent.matrix * mat
            else:
                bl_bone.matrix = mat
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='EDIT')
        if normal_bones:
            for name, bl_bone in self.armature.edit_bones.items():
                if not bl_bone.parent:
                    continue
                parent = bl_bone.parent
                # print("Bone :",name,"parent:",parent.name)
                if len(parent.children) > 1:
                    bl_bone.use_connect = False
                    parent.tail = sum([ch.head for ch in parent.children],
                                      mathutils.Vector()) / len(parent.children)
                else:
                    parent.tail = bl_bone.head
                    bl_bone.use_connect = True
                    if bl_bone.children == 0:
                        par = bl_bone.parent
                        if par.children > 1:
                            bl_bone.tail = bl_bone.head + (par.tail - par.head)
                    if bl_bone.parent == 0 and bl_bone.children > 1:
                        bl_bone.tail = (bl_bone.head + bl_bone.tail) * 2
                if not bl_bone.children:
                    vec = bl_bone.parent.head - bl_bone.head
                    bl_bone.tail = bl_bone.head - vec / 2
            bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
        bpy.ops.object.mode_set(mode='OBJECT')

    @staticmethod
    def get_material(mat_name, model_ob):
        if mat_name:
            mat_name = mat_name
        else:
            mat_name = "Material"
        mat_ind = 0
        md = model_ob.data
        mat = None
        for candidate in bpy.data.materials:  # Do we have this material already?
            if candidate.name == mat_name:
                mat = candidate
        if mat:
            if md.materials.get(mat.name):  # Look for it on this mesh
                for i in range(len(md.materials)):
                    if md.materials[i].name == mat.name:
                        mat_ind = i
                        break
            else:  # material exists, but not on this mesh
                md.materials.append(mat)
                mat_ind = len(md.materials) - 1
        else:  # material does not exist
            # print("- New material: {}".format(mat_name))
            mat = bpy.data.materials.new(mat_name)
            md.materials.append(mat)
            # Give it a random colour
            rand_col = []
            for i in range(3):
                rand_col.append(random.uniform(.4, 1))
            mat.diffuse_color = rand_col

            mat_ind = len(md.materials) - 1

        return mat_ind

    def get_polygon(self, strip_group: VTX_DATA.SourceVtxStripGroup, vtx_index_index: int, _, mesh_vertex_offset,
                    body_part_vertex_offset: int):
        vertex_indices = []
        vn_s = []
        for i in [0, 2, 1]:
            vtx_vertex_index = strip_group.vtx_indexes[vtx_index_index + i]  # type: int
            vtx_vertex = strip_group.vtx_vertexes[vtx_vertex_index]  # type: VTX_DATA.SourceVtxVertex
            vertex_index = vtx_vertex.original_mesh_vertex_index + body_part_vertex_offset + mesh_vertex_offset
            try:
                vn = self.VVD.file_data.vertexes[vertex_index]  # type: GLOBALS.SourceVertex
                vn = vn.normal.as_list
            except IndexError:
                vn = [0, 1, 0]
            vertex_indices.append(vertex_index)
            vn_s.append(vn)
        return vertex_indices, vn_s

    def convert_mesh(self, vtx_model: VTX_DATA.SourceVtxModel, lod_index, model: MDL_DATA.SourceMdlModel,
                     material_indexes):
        vtx_lod = vtx_model.vtx_model_lods[lod_index]  # type: VTX_DATA.SourceVtxModelLod
        indexes = []
        vertex_normals = []
        # small speedup
        i_ex = indexes.extend
        m_ex = material_indexes.extend
        vn_ex = vertex_normals.extend

        for mesh_index, vtx_mesh in enumerate(vtx_lod.vtx_meshes):  # type: int,VTX_DATA.SourceVtxMesh
            material_index = model.meshes[mesh_index].material_index
            mesh_vertex_start = model.meshes[mesh_index].vertex_index_start
            if vtx_mesh.vtx_strip_groups:

                for group_index, strip_group in enumerate(
                        vtx_mesh.vtx_strip_groups):  # type: VTX_DATA.SourceVtxStripGroup
                    # optimisation, because big list - slow append operation
                    strip_indexes = []
                    strip_material = []
                    strip_vertex_normals = []
                    # small speedup
                    sm_app = strip_material.append
                    si_app = strip_indexes.append
                    svn_app = strip_vertex_normals.extend
                    if strip_group.vtx_strips and strip_group.vtx_indexes and strip_group.vtx_vertexes:
                        field = progressBar.Progress_bar('Converting mesh', len(strip_group.vtx_indexes), 20)
                        for vtxIndexIndex in range(0, len(strip_group.vtx_indexes), 3):
                            field.increment(3)
                            if not vtxIndexIndex % 500:
                                field.draw()
                            f, vn = self.get_polygon(strip_group, vtxIndexIndex, lod_index, mesh_vertex_start,
                                                     self.vertex_offset)
                            si_app(f)
                            svn_app(vn)
                            sm_app(material_index)
                        field.is_done = True
                        field.draw()
                    else:
                        print('Strip group is empty')

                    i_ex(strip_indexes)
                    m_ex(strip_material)
                    vn_ex(strip_vertex_normals)
            else:
                print('VTX mesh is empty')
        return indexes, material_indexes, vertex_normals

    @staticmethod
    def convert_vertex(vertex: GLOBALS.SourceVertex):
        return vertex.position.as_list, (vertex.texCoordX, 1 - vertex.texCoordY), vertex.normal.as_list

    def create_model(self, model: MDL_DATA.SourceMdlModel, vtx_model: VTX_DATA.SourceVtxModel):
        name = model.name.replace('.smd', '').replace('.dmx', '')
        if len(vtx_model.vtx_model_lods[0].vtx_meshes) < 1:
            print('No meshes in vtx model_path')
            return
        self.mesh_obj = bpy.data.objects.new(name, bpy.data.meshes.new(name))
        self.mesh_obj.parent = self.armature_obj
        bpy.context.scene.objects.link(self.mesh_obj)
        modifier = self.mesh_obj.modifiers.new(type="ARMATURE", name="Armature")
        modifier.object = self.armature_obj
        self.mesh = self.mesh_obj.data
        [self.get_material(mat.thePathFileName, self.mesh_obj) for mat in self.MDL.file_data.textures]
        material_indexes = []
        weight_groups = {bone.name: self.mesh_obj.vertex_groups.new(bone.name) for bone in
                         self.MDL.file_data.bones}
        vtx_model_lod = vtx_model.vtx_model_lods[0]  # type: VTX_DATA.SourceVtxModelLod
        print('Converting {} mesh'.format(name))
        if vtx_model_lod.meshCount > 0:
            t = time.time()
            polygons, polygon_material_indexes, normals = self.convert_mesh(vtx_model, 0, model,
                                                                            material_indexes)
            print('Mesh generation took {} sec'.format(round(time.time() - t), 2))
        else:
            return
        self.vertex_offset += model.vertex_count
        vertexes = []
        uvs = []
        print('Preparing vertexes')
        for n, vertex in enumerate(self.VVD.file_data.vertexes):
            vert_co, uv, norm = IOMdl.convert_vertex(vertex)
            vertexes.append(vert_co)
            uvs.append(uv)
        self.mesh.from_pydata(vertexes, [], polygons)
        self.mesh.update()
        if self.MDL.file_data.flex_descs:
            print('Adding flexes')
        self.add_flexes(model)
        for n, vertex in enumerate(self.VVD.file_data.vertexes):
            for bone_index, weight in zip(vertex.boneWeight.bone, vertex.boneWeight.weight):
                if weight == 0.0:
                    continue
                weight_groups[self.MDL.file_data.bones[bone_index].name].add([n], weight, 'REPLACE')
        self.mesh.uv_textures.new()
        uv_data = self.mesh.uv_layers[0].data
        print('Applying UV')
        for i in range(len(uv_data)):
            u = uvs[self.mesh.loops[i].vertex_index]
            uv_data[i].uv = u
        for polygon, mat_index in zip(self.mesh.polygons, polygon_material_indexes):
            polygon.material_index = mat_index
        bpy.ops.object.select_all(action="DESELECT")
        self.mesh_obj.select = True
        bpy.context.scene.objects.active = self.mesh_obj
        # print(normals)

        with redirect_stdout(stdout):
            bpy.ops.object.mode_set(mode='EDIT')
            self.mesh.validate()
            self.mesh.validate()
            bpy.ops.object.mode_set(mode='OBJECT')
            # self.mesh.validate()
            # self.mesh.validate()
            bpy.ops.object.shade_smooth()
        self.mesh.normals_split_custom_set(normals)
        self.mesh.use_auto_smooth = True
        with redirect_stdout(stdout):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.delete_loose()
            bpy.ops.object.mode_set(mode='OBJECT')
        return self.mesh_obj

    def create_models(self):
        self.MDL.file_data = self.MDL.file_data  # type: MDL_DATA.SourceMdlFileData
        for bodyparts in self.MDL.file_data.bodypart_frames:
            to_join = []
            for bodypart_index, bodypart in bodyparts:

                for model_index, model in enumerate(bodypart.models):
                    vtx_model = self.VTX.vtx.vtx_body_parts[bodypart_index].vtx_models[model_index]
                    to_join.append(self.create_model(model, vtx_model))
            # print(self.join_clamped,to_join)
            bpy.ops.object.mode_set(mode='OBJECT')
            if self.join_clamped:
                for ob in to_join:
                    if not ob:
                        continue
                    if ob.type == 'MESH':
                        ob.select = True
                        bpy.context.scene.objects.active = ob
                    else:
                        ob.select = False
                bpy.context.scene.objects.active = to_join[0]
                if len(bpy.context.selected_objects)<2:
                    continue
                with redirect_stdout(stdout):
                    bpy.ops.object.join()
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.remove_doubles(threshold=0.00001)
                    bpy.ops.object.mode_set(mode='OBJECT')

    def add_flexes(self, mdlmodel: MDL_DATA.SourceMdlModel):
        # Creating base shape key
        self.mesh_obj.shape_key_add(name='base')

        # Going through all flex frames in SourceMdlModel
        for flex_frame in mdlmodel.flex_frames:

            # Now for every flex and vertex_offset(bodyAndMeshVertexIndexStarts)
            for flex, vertex_offset in zip(flex_frame.flexes, flex_frame.vertex_offsets):

                flex_desc = self.MDL.file_data.flex_descs[flex.flexDescIndex]
                flex_name = flex_desc.name
                # if blender mesh does not have FLEX_NAME - create it,
                # otherwise work with existing
                if not self.mesh_obj.data.shape_keys.key_blocks.get(flex_name):
                    self.mesh_obj.shape_key_add(name=flex_name)

                # iterating over all VertAnims
                for flex_vert in flex.theVertAnims:  # type: MDL_DATA.SourceMdlVertAnim
                    vertex_index = flex_vert.index + vertex_offset  # <- bodyAndMeshVertexIndexStarts
                    vx = self.mesh_obj.data.vertices[vertex_index].co.x
                    vy = self.mesh_obj.data.vertices[vertex_index].co.y
                    vz = self.mesh_obj.data.vertices[vertex_index].co.z
                    fx, fy, fz = flex_vert.theDelta
                    self.mesh_obj.data.shape_keys.key_blocks[flex_name].data[vertex_index].co = (
                        fx + vx, fy + vy, fz + vz)

    def create_attachments(self):
        for attachment in self.MDL.file_data.attachments:
            bone = self.armature.bones.get(self.MDL.file_data.bones[attachment.localBoneIndex].name)

            empty = bpy.data.objects.new("empty", None)
            bpy.context.scene.objects.link(empty)
            empty.name = attachment.name
            pos = Vector([attachment.pos.x, attachment.pos.y, attachment.pos.z])
            rot = Euler([attachment.rot.x, attachment.rot.y, attachment.rot.z])
            empty.matrix_basis.identity()
            empty.parent = self.armature_obj
            empty.parent_type = 'BONE'
            empty.parent_bone = bone.name
            empty.location = pos
            empty.rotation_euler = rot
        # illumination_position
        empty = bpy.data.objects.new("empty", None)
        bpy.context.scene.objects.link(empty)
        empty.name = 'illum position'
        empty.parent = self.armature_obj
        empty.location = Vector(self.MDL.file_data.illumination_position.as_list)
        empty.empty_draw_type = 'SPHERE'


if __name__ == '__main__':
    a = IOMdl(r'test_data\undyne_bigger_nude.mdl', normal_bones=False,join_clamped=True)
    # a = IOMdl(r'test_data\titan_buddy.mdl', normal_bones=False)
    # a = IO_MDL(r'E:\PYTHON\MDL_reader\test_data\nick_hwm.mdl', normal_bones=True)
