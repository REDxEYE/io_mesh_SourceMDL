import os.path
import sys

sys.path.append(r'E:\PYTHON\io_mesh_SourceMDL')
from Source2.ValveFile import ValveFile
from Source2.Vmesh_IO import VMESH_IO
import bpy, mathutils
from mathutils import Vector, Matrix, Euler, Quaternion


class Vmdl_IO:

    def __init__(self, vmdl_path,import_meshes):
        self.valve_file = ValveFile(vmdl_path)
        self.valve_file.read_block_info()
        self.valve_file.check_external_resources()

        self.name = str(os.path.basename(vmdl_path).split('.')[0])
        # print(self.valve_file.data.data.keys())
        self.remap_table = self.valve_file.data.data['PermModelData_t']['m_remappingTable']
        self.model_skeleton = self.valve_file.data.data['PermModelData_t']['m_modelSkeleton']
        self.bone_names = self.model_skeleton['m_boneName']
        self.bone_positions = self.model_skeleton['m_bonePosParent']
        self.bone_rotations = self.model_skeleton['m_boneRotParent']
        self.bone_parents = self.model_skeleton['m_nParent']
        for res,path in self.valve_file.available_resources.items():
            if 'vmesh' in res and import_meshes:
                vmesh = VMESH_IO(path)
                vmesh.build_meshes(self.bone_names,self.remap_table)
        self.build_armature()

    def build_armature(self):

        bpy.ops.object.armature_add(enter_editmode=True)

        self.armature_obj = bpy.context.object
        self.armature_obj.show_x_ray = True

        self.armature = self.armature_obj.data
        self.armature.name = self.name + "_ARM"
        self.armature.edit_bones.remove(self.armature.edit_bones[0])

        bpy.ops.object.mode_set(mode='EDIT')
        bones = []
        for se_bone in self.bone_names:  # type:
            bones.append((self.armature.edit_bones.new(se_bone), se_bone))

        for n, (bl_bone, se_bone) in enumerate(bones):
            bone_pos = self.bone_positions[n]
            # y = bone_pos.y
            # bone_pos.y = bone_pos.z
            # bone_pos.z = y
            if self.bone_parents[n] != -1:
                bl_parent, parent = bones[self.bone_parents[n]]
                bl_bone.parent = bl_parent
                bl_bone.tail = Vector([0, 0, 0]) + bl_bone.head
                bl_bone.head = Vector(bone_pos.as_list) - bl_parent.head  # + bl_bone.head
                bl_bone.tail = bl_bone.head + Vector([0, 0, 1])
            else:
                pass
                bl_bone.tail = Vector([0,0,0])+ bl_bone.head
                bl_bone.head = Vector(bone_pos.as_list) #+ bl_bone.head
                bl_bone.tail = bl_bone.head + Vector([0,0,1])

        # bpy.ops.object.mode_set(mode='POSE')
        # for bone_name, bone_parent, bone_pos, bone_rot in zip(self.bone_names, self.bone_parents,self.bone_positions,
        #                                                       self.bone_rotations):
        #     bl_bone = self.armature_obj.pose.bones.get(bone_name)
        #     # y = bone_pos.y
        #     # bone_pos.y = bone_pos.z
        #     # bone_pos.z = y
        #
        #     # y = bone_rot.y
        #     # bone_rot.y = bone_rot.z
        #     # bone_rot.z = y
        #     # if bl_bone.parent:
        #     #     pass
        #     #     bone_pos.z *= -1
        #     #     bone_pos.y *= -1
        #     pos = Vector(bone_pos.asList)
        #     rot = Quaternion(bone_rot.asList)
        #     mat = Matrix.Translation(pos) * rot.to_matrix().to_4x4()
        #     bl_bone.matrix_basis.identity()
        #     if bl_bone.parent:
        #
        #         # bl_bone.matrix = mat
        #         bl_bone.matrix_basis = bl_bone.parent.matrix * mat
        #     else:
        #         bl_bone.matrix_basis = mat
        # bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='EDIT')
        # if normal_bones:
        #     for name, bl_bone in self.armature.edit_bones.items():
        #         if not bl_bone.parent:
        #             continue
        #         parent = bl_bone.parent
        #         # print("Bone :",name,"parent:",parent.name)
        #         if len(parent.children) > 1:
        #             bl_bone.use_connect = False
        #             parent.tail = sum([ch.head for ch in parent.children],
        #                               mathutils.Vector()) / len(parent.children)
        #         else:
        #             parent.tail = bl_bone.head
        #             bl_bone.use_connect = True
        #             if bl_bone.children == 0:
        #                 par = bl_bone.parent
        #                 if par.children > 1:
        #                     bl_bone.tail = bl_bone.head + (par.tail - par.head)
        #             if bl_bone.parent == 0 and bl_bone.children > 1:
        #                 bl_bone.tail = (bl_bone.head + bl_bone.tail) * 2
        #         if not bl_bone.children:
        #             vec = bl_bone.parent.head - bl_bone.head
        #             bl_bone.tail = bl_bone.head - vec / 2
        #     bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
        bpy.ops.object.mode_set(mode='OBJECT')

if __name__ == '__main__':
    a = Vmdl_IO(r'E:\PYTHON\io_mesh_SourceMDL/test_data/source2/sniper.vmdl_c')