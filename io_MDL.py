import random
from typing import Tuple

import time
import sys

try:
    from . import VVD, VVD_DATA, VTX, MDL, MDL_DATA, VTX_DATA, GLOBALS, progressBar
    from . import math_utilities
except:
    sys.path.append(r'E:\PYTHON\MDL_reader\rewrite')
    import VVD, VVD_DATA, VTX, MDL, MDL_DATA, VTX_DATA, GLOBALS, progressBar
    import math_utilities
import os.path, struct,numpy
import bpy, mathutils
import bmesh
from mathutils import Vector, Matrix, Euler
from contextlib import redirect_stdout
import io

stdout = io.StringIO()

split = lambda A, n=3: [A[i:i + n] for i in range(0, len(A), n)]
class IO_MDL:
    def __init__(self, path: str = None, import_textures=False, working_directory=None, co=None, rot=False,
                 internal_files=None,
                 custom_name=None, normal_bones=False):

        self.name = os.path.basename(path)[:-4]
        self.co = co
        self.rot = rot
        self.vertex_offset = 0
        with open(path, 'rb') as fp:
            fp.read(4)
            version = struct.unpack('i', fp.read(4))[0]
        file_path = path.replace('.dx90', "")[:-4]
        if version < 53:
            if path:
                self.VVD = VVD.SourceVvdFile49(file_path)
                self.VTX = VTX.SourceVtxFile49(file_path)
                self.MDL = MDL.SourceMdlFile49(file_path)
        elif version == 53:
            self.MDL = MDL.SourceMdlFile53(path=file_path)
            self.VVD = self.MDL.VVD
            self.VTX = self.MDL.VTX
        if custom_name:
            self.armature_obj.name = custom_name
        self.create_skeleton(normal_bones)
        self.create_models()
        self.create_attachments()

    def create_skeleton(self, normal_bones=False):

        bpy.ops.object.armature_add(enter_editmode=True)

        self.armature_obj = bpy.context.object
        self.armature_obj.show_x_ray = True

        self.armature = self.armature_obj.data
        self.armature.name = self.name + "_ARM"
        self.armature.edit_bones.remove(self.armature.edit_bones[0])

        bpy.ops.object.mode_set(mode='EDIT')
        bones = []
        for se_bone in self.MDL.mdl.theBones:  # type: MDL_DATA.SourceMdlBone
            bones.append((self.armature.edit_bones.new(se_bone.name), se_bone))

        for bl_bone, se_bone in bones:  # type: Tuple[bpy.types.EditBone, MDL_DATA.SourceMdlBone]
            if se_bone.parentBoneIndex != -1:
                bl_parent, parent = bones[se_bone.parentBoneIndex]
                bl_bone.parent = bl_parent
            else:
                pass
            bl_bone.tail = Vector([0, 0, 1]) + bl_bone.head

        bpy.ops.object.mode_set(mode='POSE')
        for se_bone in self.MDL.mdl.theBones:  # type: MDL_DATA.SourceMdlBone
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

    def get_material(self, mat_name, model_ob):
        if mat_name:
            mat_name = mat_name
        else:
            mat_name = "Material"

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
            randCol = []
            for i in range(3):
                randCol.append(random.uniform(.4, 1))
            mat.diffuse_color = randCol

            mat_ind = len(md.materials) - 1

        return mat_ind

    def get_polygon(self,StripGroup: VTX_DATA.SourceVtxStripGroup, vtx_index_index: int, lodIndex, mesh_vertex_offset,
                    body_part_vertex_offset: int):
        verts_inds = []
        vn_s = []
        for i in [0,2,1]:
            VtxVertexIndex = StripGroup.theVtxIndexes[vtx_index_index+i]  # type: int
            VtxVertex = StripGroup.theVtxVertexes[VtxVertexIndex]  # type: VTX_DATA.SourceVtxVertex
            vertexIndex = VtxVertex.originalMeshVertexIndex + body_part_vertex_offset + mesh_vertex_offset
            try:
                vn = self.VVD.vvd.theVertexes[vertexIndex].normal.asList  # type: GLOBALS.SourceVertex
            except:
                vn = [0,1,0]
            verts_inds.append(vertexIndex)
            vn_s.append(vn)
        return verts_inds,vn_s

    def convert_mesh(self, vtx_model: VTX_DATA.SourceVtxModel, lod_index, model: MDL_DATA.SourceMdlModel,
                     material_indexes):
        vtx_lod = vtx_model.theVtxModelLods[lod_index]  # type: VTX_DATA.SourceVtxModelLod
        indexes = []
        vertex_indexes = []
        vertex_normals = []
        # small speedup
        v_ex = vertex_indexes.extend
        i_ex = indexes.extend
        m_ex = material_indexes.extend
        vn_ex = vertex_normals.extend

        for mesh_index, vtx_mesh in enumerate(vtx_lod.theVtxMeshes):  # type: int,VTX_DATA.SourceVtxMesh
            material_index = model.theMeshes[mesh_index].materialIndex
            mesh_vertex_start = model.theMeshes[mesh_index].vertexIndexStart
            if vtx_mesh.theVtxStripGroups:

                for group_index, strip_group in enumerate(
                        vtx_mesh.theVtxStripGroups):  # type: VTX_DATA.SourceVtxStripGroup
                    # optimisation, because bigger list - slower append operation
                    strip_vertex_indexes = []
                    strip_indexes = []
                    strip_material = []
                    strip_vertex_normals = []
                    sv_app = strip_vertex_indexes.append
                    sm_app = strip_material.append
                    si_app = strip_indexes.append
                    svn_app = strip_vertex_normals.extend
                    if strip_group.theVtxStrips and strip_group.theVtxIndexes and strip_group.theVtxVertexes:
                        field = progressBar.Progress_bar('Converting mesh', len(strip_group.theVtxIndexes), 20)

                        for vtxIndexIndex in range(0, len(strip_group.theVtxIndexes), 3):
                            field.increment(3)
                            if not vtxIndexIndex % 500:
                                field.draw()
                            f,vn = self.get_polygon(strip_group, vtxIndexIndex, lod_index, mesh_vertex_start,
                                                    self.vertex_offset)
                            si_app(f)
                            svn_app(vn)
                            sm_app(material_index)
                            if vtxIndexIndex not in vertex_indexes:
                                sv_app(vtxIndexIndex)
                            if vtxIndexIndex + 2 not in vertex_indexes:
                                sv_app(vtxIndexIndex + 2)
                            if vtxIndexIndex + 1 not in vertex_indexes:
                                sv_app(vtxIndexIndex + 1)
                        field.isDone = True
                        field.draw()
                    else:
                        print('Strip group is empty')

                    v_ex(strip_vertex_indexes)
                    i_ex(strip_indexes)
                    m_ex(strip_material)
                    vn_ex(strip_vertex_normals)
            else:
                print('VTX mesh is empty')
        return indexes, material_indexes, vertex_indexes,vertex_normals

    @staticmethod
    def convert_vertex(vertex: GLOBALS.SourceVertex):
        return vertex.position.asList, (vertex.texCoordX, 1 - vertex.texCoordY), vertex.normal.asList

    def create_model(self, model: MDL_DATA.SourceMdlModel, vtx_model: VTX_DATA.SourceVtxModel):
        name = model.name
        if len(vtx_model.theVtxModelLods[0].theVtxMeshes) < 1:
            print('No meshes in vtx model')
            return
        self.mesh_obj = bpy.data.objects.new(name, bpy.data.meshes.new(name))
        self.mesh_obj.parent = self.armature_obj
        bpy.context.scene.objects.link(self.mesh_obj)
        modifier = self.mesh_obj.modifiers.new(type="ARMATURE", name="Armature")
        modifier.object = self.armature_obj
        self.mesh = self.mesh_obj.data
        materials = [self.get_material(mat.thePathFileName, self.mesh_obj) for mat in
                     self.MDL.mdl.theTextures]
        material_indexes = []
        weight_groups = {bone.name: self.mesh_obj.vertex_groups.new(bone.name) for bone in
                         self.MDL.mdl.theBones}
        vtxmodellod = vtx_model.theVtxModelLods[0]  # type: VTX_DATA.SourceVtxModelLod
        print('Converting {} mesh'.format(name))
        if vtxmodellod.meshCount > 0:
            t = time.time()
            polygons, polygon_material_indexes, vertex_indexes,normals= self.convert_mesh(vtx_model, 0, model,
                                                                                          material_indexes)
            print('Mesh generation took {} sec'.format(round(time.time() - t),2))
        else:
            return
        self.vertex_offset += model.vertexCount
        vertexes = []
        uvs = []
        # normals = []
        for vertex in self.VVD.vvd.theVertexes:
            vert_co, uv, norm = IO_MDL.convert_vertex(vertex)
            vertexes.append(vert_co)
            uvs.append(uv)
            # normals.append(norm)
        # for vertex_index in vertex_indexes:
        #     try:
        #         normals.append(self.VVD.vvd.theVertexes[vertex_index].normal.asList)
        #     except:
        #         print('fail on',vertex_index)
        # print(polygons)
        # input()
        self.mesh.from_pydata(vertexes, [], polygons)
        self.mesh.update()
        self.add_flexes(model)
        for n, vertex in enumerate(self.VVD.vvd.theVertexes):
            for bone_index, weight in zip(vertex.boneWeight.bone, vertex.boneWeight.weight):
                weight_groups[self.MDL.mdl.theBones[bone_index].name].add([n], weight, 'REPLACE')
        self.mesh.uv_textures.new()
        uv_data = self.mesh.uv_layers[0].data
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
            # bpy.ops.object.mode_set(mode='EDIT')
            # self.mesh.validate()
            # self.mesh.validate()
            # bpy.ops.mesh.delete_loose()
            # bpy.ops.mesh.normals_make_consistent(inside=False)
            # bpy.ops.mesh.delete_loose()
            # bpy.ops.mesh.remove_doubles(threshold=0.0001)
            # bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            # self.mesh.validate()
            # self.mesh.validate()
            bpy.ops.object.shade_smooth()
        self.mesh.normals_split_custom_set(normals)
        self.mesh.use_auto_smooth = True

    def create_models(self):
        self.MDL.mdl = self.MDL.mdl  # type: MDL_DATA.SourceMdlFileData
        for bodyparts in self.MDL.mdl.bodyparts:
            for bodypart_index, bodypart in bodyparts:
                for model_index, model in enumerate(bodypart.theModels):
                    vtx_model = self.VTX.vtx.theVtxBodyParts[bodypart_index].theVtxModels[model_index]
                    self.create_model(model, vtx_model)

    def add_flexes(self, mdlmodel: MDL_DATA.SourceMdlModel):
        # Creating base shape key
        self.mesh_obj.shape_key_add(name='base')

        # Going through all flex frames in SourceMdlModel
        for flex_frame in mdlmodel.flex_frames:

            # Now for every flex and vertex_offset(bodyAndMeshVertexIndexStarts)
            for flex, vertex_offset in zip(flex_frame.flexes, flex_frame.vertex_offsets):

                flex_desc = self.MDL.mdl.theFlexDescs[flex.flexDescIndex]
                flex_name = flex_desc.theName
                # if blender mesh does not have FLEX_NAME - create it,
                # otherwise work with existing
                if not self.mesh_obj.data.shape_keys.key_blocks.get(flex_name):
                    self.mesh_obj.shape_key_add(name=flex_name)

                # iterating over all VertAnims
                for flex_vert in flex.theVertAnims:  # type: MDL_DATA.SourceMdlVertAnim
                    Vert_index = flex_vert.index + vertex_offset  # <- bodyAndMeshVertexIndexStarts
                    vx = self.mesh_obj.data.vertices[Vert_index].co.x
                    vy = self.mesh_obj.data.vertices[Vert_index].co.y
                    vz = self.mesh_obj.data.vertices[Vert_index].co.z
                    fx, fy, fz = flex_vert.theDelta
                    self.mesh_obj.data.shape_keys.key_blocks[flex_name].data[Vert_index].co = (
                        fx + vx, fy + vy, fz + vz)

    def create_attachments(self):
        # MathModule.ConvertRotationMatrixToDegrees(anAttachment.localM11, anAttachment.localM21, anAttachment.localM31,
        #                                           anAttachment.localM12, anAttachment.localM22, anAttachment.localM32,
        #                                           anAttachment.localM33, angleX, angleY, angleZ)
        # offsetX = Math.Round(anAttachment.localM14, 2)
        # offsetY = Math.Round(anAttachment.localM24, 2)
        # offsetZ = Math.Round(anAttachment.localM34, 2)
        # angleX = Math.Round(angleX, 2)
        # angleY = Math.Round(angleY, 2)
        # angleZ = Math.Round(angleZ, 2)

        for attachment in self.MDL.mdl.theAttachments:
            bone = self.armature.bones.get(self.MDL.mdl.theBones[attachment.localBoneIndex].name)

            empty = bpy.data.objects.new("empty", None)
            bpy.context.scene.objects.link(empty)
            empty.name = attachment.name
            pos = Vector([attachment.pos.x, attachment.pos.y, attachment.pos.z])
            rot = Euler([attachment.rot.x, attachment.rot.y, attachment.rot.z])
            # mat = Matrix.Translation(pos) * rot.to_matrix().to_4x4()
            empty.matrix_basis.identity()
            empty.parent = self.armature_obj
            empty.parent_type = 'BONE'
            empty.parent_bone = bone.name
            empty.location = pos
            empty.rotation_euler = rot

            # if empty.parent:
            #     empty.matrix = empty.parent.matrix * mat
            # else:
            #     empty.matrix = mat
            # empty.location = bone.head+Vector(attachment.pos.asList)
            # empty.parent = bone


if __name__ == '__main__':
    a = IO_MDL(r'test_data\veria_v2.mdl', normal_bones=True)
    # a = IO_MDL(r'E:\PYTHON\MDL_reader\test_data\nick_hwm.mdl', normal_bones=True)
