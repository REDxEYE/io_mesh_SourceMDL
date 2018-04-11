import random
from typing import Tuple

import time
import sys

try:
    from . import VVD, VVD_DATA, VTX, MDL, MDL_DATA, VTX_DATA, GLOBALS, progressBar
except:
    sys.path.append(r'E:\PYTHON\MDL_reader\rewrite')
    import VVD, VVD_DATA, VTX, MDL, MDL_DATA, VTX_DATA, GLOBALS, progressBar
# from test_field.V53 import Mdl53
import os.path, struct
import bpy, mathutils
from mathutils import Vector, Matrix, Euler
from contextlib import redirect_stdout
import io

stdout = io.StringIO()


class IO_MDL:
    def __init__(self, path: str = None, import_textures=False, working_directory=None, co=None, rot=False,
                 internal_files=None,
                 custom_name=None, normal_bones=False):

        self.name = os.path.basename(path)[:-4]
        self.co = co
        self.rot = rot
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
        self.create_mesh()

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

    def create_mesh(self):

        def get_polygon(StripGroup: VTX_DATA.SourceVtxStripGroup, vtx_index_index: int, lodIndex, mesh_vertex_offset,
                        body_part_vertex_offset: int, VVD):
            VtxVertexIndex = StripGroup.theVtxIndexes[vtx_index_index]  # type: int
            VtxVertex = StripGroup.theVtxVertexes[VtxVertexIndex]  # type: VTX_DATA.SourceVtxVertex
            vertexIndex = VtxVertex.originalMeshVertexIndex + body_part_vertex_offset + mesh_vertex_offset
            if VVD.vvd.fixupCount == 0:
                Vertex = self.VVD.vvd.theVertexes[vertexIndex]  # type: GLOBALS.SourceVertex
            else:
                Vertex = self.VVD.vvd.theFixedVertexesByLod[0][vertexIndex]

            return vertexIndex

        def convert_mesh(vtx_model: VTX_DATA.SourceVtxModel, lod_index, model: MDL_DATA.SourceMdlModel,
                         body_part_vertex_offset, material_indexes, VVD):
            vtx_lod = vtx_model.theVtxModelLods[lod_index]  # type: VTX_DATA.SourceVtxModelLod
            indexes = []
            vertex_idexes = []
            for mesh_index, vtx_mesh in enumerate(vtx_lod.theVtxMeshes):  # type: VTX_DATA.SourceVtxMesh
                material_index = model.theMeshes[mesh_index].materialIndex
                mesh_vertex_start = model.theMeshes[mesh_index].vertexIndexStart
                if len(vtx_mesh.theVtxStripGroups) > 0:
                    for group_index, strip_group in enumerate(
                            vtx_mesh.theVtxStripGroups):  # type: VTX_DATA.SourceVtxStripGroup
                        if len(strip_group.theVtxStrips) > 0 and len(strip_group.theVtxIndexes) > 0 and len(
                                strip_group.theVtxVertexes) > 0:
                            field = progressBar.Progress_bar('Converting mesh', len(strip_group.theVtxIndexes), 20)

                            for vtxIndexIndex in range(0, len(strip_group.theVtxIndexes), 3):
                                field.increment(3)
                                if vtxIndexIndex % 250 == 0:
                                    field.draw()
                                f = get_polygon(strip_group, vtxIndexIndex, lod_index, mesh_vertex_start,
                                                body_part_vertex_offset, VVD)
                                s = get_polygon(strip_group, vtxIndexIndex + 2, lod_index, mesh_vertex_start,
                                                body_part_vertex_offset, VVD)
                                t = get_polygon(strip_group, vtxIndexIndex + 1, lod_index, mesh_vertex_start,
                                                body_part_vertex_offset, VVD)
                                material_indexes.append(material_index)
                                if vtxIndexIndex not in vertex_idexes:
                                    vertex_idexes.append(vtxIndexIndex)
                                if vtxIndexIndex + 2 not in vertex_idexes:
                                    vertex_idexes.append(vtxIndexIndex + 2)
                                if vtxIndexIndex + 1 not in vertex_idexes:
                                    vertex_idexes.append(vtxIndexIndex + 1)
                                indexes.append((f, s, t))
                        else:
                            print('Strip group is empty')
                else:
                    print('VTX mesh is empty')
            return indexes, material_indexes, vertex_idexes

        def convert_vertex(vertex: GLOBALS.SourceVertex):
            return vertex.position.asList

        def convert_uv(vertex: GLOBALS.SourceVertex):
            return vertex.texCoordX, 1 - vertex.texCoordY

        def convert_custom_normal(vertex: GLOBALS.SourceVertex):
            return vertex.normal.asList

        bodyPartVertexIndexStart = 0
        for bodypart_index, body_part in enumerate(
                self.VTX.vtx.theVtxBodyParts):  # type: VTX_DATA.SourceVtxBodyPart
            if body_part.modelCount > 0:
                for model_index, aVtxModel in enumerate(body_part.theVtxModels):  # type: VTX_DATA.SourceVtxModel
                    if aVtxModel.lodCount > 0:
                        if self.MDL.mdl.theBodyParts[bodypart_index].modelCount < 1:
                            print('Body part number {} don\'t have any models'.format(bodypart_index))
                            continue
                        # try:
                        print(
                            "Trying to load model number {} from body part number {}, total body part count {}".format(
                                model_index, bodypart_index, len(self.MDL.mdl.theBodyParts)))
                        model = self.MDL.mdl.theBodyParts[bodypart_index].theModels[
                            model_index]  # type: MDL_DATA.SourceMdlModel
                        name = model.name if model.name else "mesh_{}-{}".format(bodypart_index, model_index)
                        if len(aVtxModel.theVtxModelLods[0].theVtxMeshes) < 1:
                            print('No meshes in vtx model')
                            continue
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
                        vtxmodellod = aVtxModel.theVtxModelLods[0]  # type: VTX_DATA.SourceVtxModelLod
                        print('Converting {} mesh'.format(name))
                        if vtxmodellod.meshCount > 0:
                            t = time.time()
                            polygons, polygon_material_indexes, vertex_indexes = convert_mesh(aVtxModel, 0, model,
                                                                                              bodyPartVertexIndexStart,
                                                                                              material_indexes,
                                                                                              self.VVD)
                            print('Mesh generation took {}ms'.format(time.time() - t))
                        else:
                            continue
                        bodyPartVertexIndexStart += model.vertexCount
                        vertexes = []
                        uvs = []
                        normals = []
                        # Extracting vertex coordinates,UVs and normals
                        for vertex in self.VVD.vvd.theVertexes:
                            vertexes.append(convert_vertex(vertex))
                            uvs.append(convert_uv(vertex))
                            normals.append(convert_custom_normal(vertex))

                        self.mesh.from_pydata(vertexes, [], polygons)
                        self.mesh.update()
                        self.add_flexes(model)
                        for n, vertex in enumerate(self.VVD.vvd.theVertexes):
                            for bone_index, weight in zip(vertex.boneWeight.bone, vertex.boneWeight.weight):
                                # print("Adding weight to ",self.MDL.mdl.theBones[bone_].name)
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

                        try:
                            self.mesh.create_normals_split()
                            self.mesh.use_auto_smooth = True
                            self.mesh.normals_split_custom_set_from_vertices(normals)
                        except Exception as E:
                            print(E)
                            print('FAILED TO SET CUSTOM NORMALS')
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
                    Vert_index = flex_vert.index + vertex_offset # <- bodyAndMeshVertexIndexStarts
                    vx = self.mesh_obj.data.vertices[Vert_index].co.x
                    vy = self.mesh_obj.data.vertices[Vert_index].co.y
                    vz = self.mesh_obj.data.vertices[Vert_index].co.z
                    fx, fy, fz = flex_vert.theDelta
                    self.mesh_obj.data.shape_keys.key_blocks[flex_name].data[Vert_index].co = (
                        fx + vx, fy + vy, fz + vz)


if __name__ == '__main__':
    a = IO_MDL(r'test_data\veria_v2.mdl', normal_bones=True)
    # a = IO_MDL(r'E:\PYTHON\MDL_reader\test_data\nick_hwm.mdl', normal_bones=True)
