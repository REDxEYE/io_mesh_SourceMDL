import bpy
import mathutils
import os
import os.path
import platform
import random
import re
import subprocess
import sys
import traceback
# import pyximport
# pyximport.install()
import time
try:
    import progressBar
except:
    from . import progressBar
from math import pi
import io
from contextlib import redirect_stdout


stdout = io.StringIO()
def getpath() -> str:
    """

    Returns:
        str: path to current file
    """
    script_file = os.path.realpath(__file__)
    return os.path.dirname(script_file)

sys.path.append(r'E:\MDL_reader')
sys.path.append(getpath())

from typing import Tuple, Dict

from mathutils import Vector, Matrix, Euler

import VTX_DATA, MDL_DATA, VTX2, VVD2, MDL2, GLOBALS
from test_field import V53 as MDL53
import struct



class mesh:


    def __init__(self, filepath: str = '', doTexture = False, workdir=None,coords = None,rot = None,files:Dict[str,io.FileIO] = None,forRig = False,sfm_dir = None,customName = None):
        self.forRig = forRig
        self.coords = coords
        self.rot = rot
        self.workdir = workdir
        self.cust_name = customName
        if sfm_dir:
            self.gameinfo = self.parseGameInfo(sfm_dir)
            self.sfm_dir = sfm_dir
        self.armature_object = None
        fileNameWithOutExt = ".".join(filepath.split('.')[:-1]).replace('.dx90', '')
        with open(filepath,'rb') as fp:
            fp.read(4)
            version = struct.unpack('i',fp.read(4))[0]
        if version<53:
            if files is None and filepath!='':
                self.VVD = VVD2.SourceVvdFile49(fileNameWithOutExt + '.vvd')
                self.VTX = VTX2.SourceVtxFile49(fileNameWithOutExt + '.dx90.vtx')
                self.MDL = MDL2.SourceMdlFile49(fileNameWithOutExt + '.mdl')
            else:
                self.VVD = VVD2.SourceVvdFile49(files['VVD'])
                self.VTX = VTX2.SourceVtxFile49(files['VTX'])
                self.MDL = MDL2.SourceMdlFile49(files['MDL'])
        elif version ==53:
            self.MDL = MDL53.Mdl53(open(filepath,'rb'))
            self.VVD = self.MDL.VVD
            self.VTX = self.MDL.VTX
        self.createRig(fileNameWithOutExt.split(os.sep)[-1])
        self.CreateMesh(fileNameWithOutExt.split(os.sep)[-1])
        if coords!=None and rot!=None:
            self.armature_object.location = coords
            self.armature_object.rotation_euler = Euler(rot, 'XYZ')
        # self.processTextures()
        if doTexture:
            try:
                self.processTextures()
            except Exception as E:
                print(E, 'TEXTURE IMPORT ERROR')

    def createRig(self, name):
        # Create armature and object
        if self.coords!=None:
            bpy.ops.object.armature_add(enter_editmode=True,location = self.coords)
        else:
            bpy.ops.object.armature_add(enter_editmode=True)
        ob = bpy.context.object
        if self.coords!=None:
            ob.rotation_euler = self.rot
        self.armature_object = ob
        ob.show_x_ray = True
        if self.cust_name:
            ob.name = self.cust_name
        else:
            ob.name = name
        arm = ob.data

        arm.name = name + '_arm'
        arm.show_axes = True
        self.arm = arm
        # Create bones
        bpy.ops.object.mode_set(mode='EDIT')
        # arm.edit_bones.remove(arm.edit_bones[0])
        bone_list = []
        for bone in self.MDL.theMdlFileData.theBones:  # type: MDL_DATA.SourceMdlBone
            bone_list.append((arm.edit_bones.new(bone.name), bone))
        for bone_, bone in bone_list:  # type: Tuple[bpy.types.EditBone, MDL_DATA.SourceMdlBone]
            if bone.parentBoneIndex != -1:
                parent_, parent = bone_list[bone.parentBoneIndex]
                bone_.parent = parent_
                # bone_.head = Vector([bone.position.x,bone.position.z,bone.position.y])+parent_.head
                bone_.use_connect = False

            else:
                pass
                # bone_.head = Vector([bone.position.x,bone.position.z,bone.position.y])
                # rot = Matrix.Translation([bone.rotation.x,bone.rotation.y,bone.rotation.z])  # identity matrix
            # bone_.tail = rot * Vector([1,1,1]) + bone_.head
            if self.forRig:
                bone_.tail = Vector([0, 0, 1]) + bone_.head
            else:
                bone_.tail = Vector([0, 0, 1])
            # print('bone {0} created\n'
            #       'x {1:.3f},y {2:.3f},z {3:.3f}\n'
            #       'xr {4:.3f}, yr {5:.3f}, zr {6:.3f}'.format(bone.name, bone.position.x, bone.position.z,
            #                                                   bone.position.y, bone.rotation.x, bone.rotation.y,
            #                                                   bone.rotation.z))


        bpy.ops.object.mode_set(mode='POSE')
        for bone_ in self.MDL.theMdlFileData.theBones:  # type: MDL_DATA.SourceMdlBone
            bone = ob.pose.bones.get(bone_.name)
            pos = Vector([bone_.position.x, bone_.position.y, bone_.position.z])
            rot = Euler([bone_.rotation.x, bone_.rotation.y, bone_.rotation.z])
            mat = Matrix.Translation(pos) * rot.to_matrix().to_4x4()
            bone.matrix_basis.identity()
            if bone.parent:
                bone.matrix = bone.parent.matrix * mat
            else:
                bone.matrix = mat
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')
        if self.forRig:
            bpy.ops.object.mode_set(mode='EDIT')
            for bone_, bone in bone_list:
                if bone_.parent:
                    parent = bone_.parent
                    if len(parent.children)>1:
                        bone_.use_connect = False
                        parent.tail = sum([ch.head for ch in parent.children], mathutils.Vector()) / len(parent.children)
                    else:
                        parent.tail = bone_.head
                        bone_.use_connect = True
                    if bone_.children == 0:
                        par = bone_.parent
                        if par.children >1:
                            pass
                        bone_.tail = bone_.head+(par.tail-par.head)
                if bone_.parent == 0 and bone_.children>1:
                    bone_.tail = (bone_.head+bone_.tail)*2
                bone_.select = True
            bpy.ops.armature.calculate_roll(type='GLOBAL_POS_Z')
        bpy.ops.object.mode_set(mode='OBJECT')
        return ob

    def getMeshMaterial(self, mat_name, model_ob):
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

        return mat, mat_ind

    def CreateMesh(self, name):

        def getPoly(StripGroup: VTX_DATA.SourceVtxStripGroup, VtxIndexIndex: int, lodIndex, meshVertexIndexStart,
                    bodyPartVertexIndexStart: int, VVD):
            VtxVertexIndex = StripGroup.theVtxIndexes[VtxIndexIndex]  # type: int
            VtxVertex = StripGroup.theVtxVertexes[VtxVertexIndex]  # type: VTX_DATA.SourceVtxVertex
            vertexIndex = VtxVertex.originalMeshVertexIndex + bodyPartVertexIndexStart + meshVertexIndexStart
            # print('Orig index',VtxVertex.originalMeshVertexIndex,'Body part index',bodyPartVertexIndexStart)
            if VVD.theVvdFileData.fixupCount == 0:
                # print('vert index',vertexIndex,'total vertex',len(self.VVD.theVvdFileData.theVertexes))
                Vertex = self.VVD.theVvdFileData.theVertexes[vertexIndex]  # type: GLOBALS.SourceVertex
            else:
                Vertex = self.VVD.theVvdFileData.theFixedVertexesByLod[0][vertexIndex]
                #Vertex = self.VVD.theVvdFileData.theFixedVertexesByLod[0][vertexIndex]  # type: GLOBALS.SourceVertex
            return vertexIndex, Vertex

        def addVertex(vertex_, vertex_list):

            vertex_list.append((vertex_.positionX, vertex_.positionY, vertex_.positionZ))
            # print('adding vertex {} in loc '.format(vertex_list.__len__()-1), vertex_.positionX, vertex_.positionY, vertex_.positionZ)
            return vertex_list

        def addUv(vertex: GLOBALS.SourceVertex, uv_list: list):
            uv_list.append((vertex.texCoordX, 1 - vertex.texCoordY))
            return uv_list

        def CustomNorms(vertex: GLOBALS.SourceVertex):
            return (vertex.normalX, vertex.normalY, vertex.normalZ)


        def WriteMesh_fallback(VtxModel: VTX_DATA.SourceVtxModel, lodIndex, aModel: MDL_DATA.SourceMdlModel,
                               bodyPartVertexIndexStart, mat_indexes, VVD):
            aVtxLod = VtxModel.theVtxModelLods[lodIndex]  # type: VTX_DATA.SourceVtxModelLod
            indexes = []
            vertex_idexes = []
            for meshIndex, aVtxMesh in enumerate(aVtxLod.theVtxMeshes):  # type: VTX_DATA.SourceVtxMesh
                # print('meshIndex',meshIndex,len(Model.theMeshes))
                materialIndex = aModel.theMeshes[meshIndex].materialIndex
                meshVertexIndexStart = aModel.theMeshes[meshIndex].vertexIndexStart
                # print('stripGroupCount',VtxMesh.stripGroupCount)
                if aVtxMesh.theVtxStripGroups.__len__() > 0:
                    for groupIndex, aStripGroup in enumerate(aVtxMesh.theVtxStripGroups):  # type: VTX_DATA.SourceVtxStripGroup
                        # print('StripGroup.stripCount',StripGroup.stripCount,'StripGroup.indexCount',StripGroup.indexCount,'StripGroup.vertexCount',StripGroup.vertexCount)
                        if aStripGroup.theVtxStrips.__len__() > 0 and aStripGroup.theVtxIndexes.__len__() > 0 and aStripGroup.theVtxVertexes.__len__() > 0:
                            field = progressBar.Progress_bar('Generating mesh',aStripGroup.theVtxIndexes.__len__(),20)

                            for vtxIndexIndex in range(0, aStripGroup.theVtxIndexes.__len__(), 3):
                                field.increment(3)
                                field.draw()
                                f, fv = getPoly(aStripGroup, vtxIndexIndex, lodIndex, meshVertexIndexStart,
                                                bodyPartVertexIndexStart, VVD)
                                s, sv = getPoly(aStripGroup, vtxIndexIndex + 2, lodIndex, meshVertexIndexStart,
                                                bodyPartVertexIndexStart, VVD)
                                t, tv = getPoly(aStripGroup, vtxIndexIndex + 1, lodIndex, meshVertexIndexStart,
                                                bodyPartVertexIndexStart, VVD)
                                mat_indexes.append(materialIndex)
                                if vtxIndexIndex not in vertex_idexes:
                                    vertex_idexes.append(vtxIndexIndex)
                                if vtxIndexIndex + 2 not in vertex_idexes:
                                    vertex_idexes.append(vtxIndexIndex + 2)
                                if vtxIndexIndex + 1 not in vertex_idexes:
                                    vertex_idexes.append(vtxIndexIndex + 1)
                                indexes.append((f, s, t))
                        else:
                            print('ERROR in getPoly')
                else:
                    print('ERROR in theVtxStripGroups')
            return indexes, mat_indexes, vertex_idexes

        bodyPartVertexIndexStart = 0
        for bodypart_index, aBodyPart in enumerate(self.VTX.theVtxFileData.theVtxBodyParts):  # type: VTX_DATA.SourceVtxBodyPart
            if aBodyPart.modelCount > 0:
                for model_index, aVtxModel in enumerate(aBodyPart.theVtxModels):  # type: VTX_DATA.SourceVtxModel
                    if aVtxModel.lodCount > 0:
                        if self.MDL.theMdlFileData.theBodyParts[bodypart_index].modelCount < 1:
                            print('No models here bp{} md{}'.format(bodypart_index, model_index))
                            continue
                        # try:
                        print("Trying to get bodypart N{}/{} and model N{}".format(bodypart_index,model_index,len(self.MDL.theMdlFileData.theBodyParts)))
                        aModel = self.MDL.theMdlFileData.theBodyParts[bodypart_index].theModels[model_index]  # type: MDL_DATA.SourceMdlModel
                        name = aModel.name
                        # print(aModel.name)
                        if aVtxModel.theVtxModelLods[0].theVtxMeshes.__len__() < 1:
                            continue
                        model_mesh = bpy.data.objects.new(name, bpy.data.meshes.new(name))
                        self.MODEL = model_mesh
                        model_mesh.parent = self.armature_object
                        bpy.context.scene.objects.link(model_mesh)
                        modifier = model_mesh.modifiers.new(type="ARMATURE", name="Armature")
                        modifier.object = self.armature_object
                        md = model_mesh.data
                        # Vertex values
                        mat_indexes = []
                        weightsGroups = {}
                        # Face values
                        uvs = []
                        mats = []
                        for mat in self.MDL.theMdlFileData.theTextures:  # type: GLOBALS.SourceMdlTexture
                            mat, mat_ind = self.getMeshMaterial(mat.thePathFileName, model_mesh)
                            mats.append(mat_ind)
                        faceVerts = []
                        for bone in self.MDL.theMdlFileData.theBones:
                            weightsGroups[bone.name] = model_mesh.vertex_groups.new(bone.name)
                        vtxmodellod = aVtxModel.theVtxModelLods[0]  # type: VTX_DATA.SourceVtxModelLod
                        # print('mesh count',vtxmodellod.meshCount)
                        print('Generating {} mesh'.format(aModel.name))
                        if vtxmodellod.meshCount > 0:
                            t = time.time()
                            polys, polys_mat_indexes, vertex_indexes = WriteMesh_fallback(aVtxModel, 0, aModel,
                                                                                          bodyPartVertexIndexStart, mat_indexes,
                                                                                          self.VVD)
                            print('Mesh generation took {}ms'.format(time.time() - t))
                            # print('polys',polys)
                            # print('polys_mat_indexes',polys_mat_indexes)
                            # print('vertex_indexes',vertex_indexes)
                        else:
                            continue
                        bodyPartVertexIndexStart += aModel.vertexCount
                        print('Generating UV')
                        for vert in self.VVD.theVvdFileData.theVertexes:
                            faceVerts = addVertex(vert, faceVerts)
                            uvs = addUv(vert, uvs)
                        print('Generating custom normals')
                        norms = []
                        for vert in self.VVD.theVvdFileData.theVertexes:
                            norms.append(CustomNorms(vert))
                        # print(polys)
                        print(len(faceVerts),len(polys))
                        md.from_pydata(faceVerts, [], polys)
                        # md.from_pydata(faceVerts, [],[])
                        md.update()
                        self.addFlexes(aModel)
                        for n, vertex in enumerate(self.VVD.theVvdFileData.theVertexes):
                            for bone_, weight in zip(vertex.boneWeight.bone, vertex.boneWeight.weight):
                                # print("Adding weight to ",self.MDL.theMdlFileData.theBones[bone_].name)
                                weightsGroups[self.MDL.theMdlFileData.theBones[bone_].name].add([n], weight, 'REPLACE')
                        md.uv_textures.new()
                        uv_data = md.uv_layers[0].data
                        # print("UV LOOPS on model",len(md.loops), "UV loops on mesh",len(uvs))
                        for i in range(len(uv_data)):
                            # print('UV LOOP n',i)
                            u = uvs[md.loops[i].vertex_index]
                            uv_data[i].uv = u
                        for poly, mat_index in zip(model_mesh.data.polygons, polys_mat_indexes):
                            poly.material_index = mat_index
                        bpy.ops.object.select_all(action="DESELECT")
                        model_mesh.select = True
                        bpy.context.scene.objects.active = model_mesh
                        # try:
                        #     print('NORMS', len(norms), len(md.loops))
                        #     md.create_normals_split()
                        #     md.use_auto_smooth = True
                        #     md.normals_split_custom_set_from_vertices(norms)
                        # except Exception as E:
                        #     print(E)
                        #     print('FAILED TO SET CUSTOM NORMALS')
                        with redirect_stdout(stdout):
                            md.validate()
                            md.validate()
                            model_mesh.data.validate()
                            model_mesh.data.validate()
                            bpy.ops.object.mode_set(mode='EDIT')
                            model_mesh.data.validate()
                            model_mesh.data.validate()
                            bpy.ops.mesh.delete_loose()
                            bpy.ops.mesh.normals_make_consistent(inside=False)
                            bpy.ops.mesh.delete_loose()
                            bpy.ops.mesh.remove_doubles(threshold=0.0001)
                            bpy.ops.mesh.normals_make_consistent(inside=False)
                            bpy.ops.object.mode_set(mode='OBJECT')
                            model_mesh.data.validate()
                            model_mesh.data.validate()
                            bpy.ops.object.shade_smooth()
                        print('test9')
                        # except IndexError:
                        #     print('bodypart_index ', bodypart_index, 'out of ', self.VTX.theVtxFileData.bodyPartCount,
                        #           'model_index ', model_index, 'out of ', aBodyPart.modelCount)
                        #     try:
                        #         print('MDL bodypart count', self.MDL.theMdlFileData.theBodyParts.__len__(),
                        #               'MDL model count for BP num {} - {}'.format(bodypart_index,
                        #                                                           self.MDL.theMdlFileData.theBodyParts[
                        #                                                               bodypart_index].theModels.__len__()))
                        #     except:
                        #         print('ANOTHER ERROR')
                        #     continue
                        #     raise Exception('WRONG MODEL INDEX OR BODYPART INDEX')
    def addFlexes(self,mdlmodel:MDL_DATA.SourceMdlModel):
        self.MODEL.shape_key_add(name='BASE')
        for mesh in mdlmodel.theMeshes: #type: MDL_DATA.SourceMdlMesh
            for flex in mesh.theFlexes: #type: MDL_DATA.SourceMdlFlex
                flexDesc = self.MDL.theMdlFileData.theFlexDescs[flex.flexDescIndex]
                flex_name = flexDesc.theName
                self.MODEL.shape_key_add(name=flexDesc.theName)
                for flex_vert in flex.theVertAnims: #type: MDL_DATA.SourceMdlVertAnim
                    Vert_index  = flex_vert.index + mesh.vertexIndexStart
                    vx = self.MODEL.data.vertices[Vert_index].co.x
                    vy = self.MODEL.data.vertices[Vert_index].co.y
                    vz = self.MODEL.data.vertices[Vert_index].co.z
                    fx,fy,fz = flex_vert.theDelta
                    # print('ADDING VERT ANIM vertex #{} for flex {}, COs -  x:{} y:{} z:{}'.format(Vert_index,flex_name,fx+vx,fy+vy,fz+vz))
                    self.MODEL.data.shape_keys.key_blocks[flex_name].data[Vert_index].co  = (fx+vx,fy+vy,fz+vz)

    @staticmethod
    def parseGameInfo(path_to_SFM):
        # print('path_to_GI',path_to_GI)
        path_to_GI = os.path.join(path_to_SFM,'game','usermod','gameinfo.txt')
        gameinfo = open(path_to_GI,'r').read()
        commendstripper = re.compile(r'Game[ \t]+(?P<path>[\w+|.]+)')
        gameinfo = commendstripper.findall(gameinfo)
        gameinfo[0] = os.path.join(path_to_SFM,'game','usermod')
        return gameinfo
    def find_material(self,mat_name:str,texture_paths):
        for game in self.gameinfo:
            for texture_path in texture_paths:
                if texture_path == '':
                    continue
                texture_path = os.path.join(self.sfm_dir,'game',game,'materials',texture_path,mat_name+'.vmt')

                if os.path.isfile(texture_path):
                    return texture_path
        else:
            sys.stderr.write('Can\'t find map {}'.format(mat_name))
            return False

    def find_texture(self,tex_path:str):
        for game in self.gameinfo:
            texture_path = os.path.join(self.sfm_dir,'game',game,'materials',tex_path+'.vtf')
            if os.path.isfile(texture_path):
                return texture_path
        else:
            sys.stderr.write('Can\'t find map {}'.format(tex_path.split(os.sep)[-1]))
            return False

    def processTextures(self):

        import material_builder
        vtf = True
        try:
            if 'VTF' not in globals() or 'VTF' not in locals():
                import VTF
        except:
            print("IO_TEXTURE_VTF NOT INSTALLED!")
            vtf = False
        materials = {}
        textures = []
        if self.workdir!=None:
            material_folder = os.path.join(self.workdir, 'materials')
            model_textures_folders = [os.path.join(material_folder, path) for path in
                                      self.MDL.theMdlFileData.theTexturePaths if
                                      path != '']
            # print('model_textures_folders', model_textures_folders)
            for texture in self.MDL.theMdlFileData.theTextures:  # type: GLOBALS.SourceMdlTexture

                for n, path_ in enumerate(model_textures_folders):
                    files = os.listdir(path_)
                    # print('tofind',texture.thePathFileName + '.vmt'.lower())
                    file = [a for a in files if (texture.thePathFileName + '.vmt').lower() == a.lower()]
                    if file:
                        print(os.path.join(path_, file[0]))
                        materials[texture.thePathFileName] = open(os.path.join(path_, file[0]), 'r')
                        break
            for matName, mat in materials.items():
                print('PARSING MATERIAL {}'.format(matName))
                mat_data = mat.read()
                if 'EyeRefract' in mat_data.lower() or 'eyes' in mat_data.lower():
                    texturePath = re.findall(r'\"?\$Iris\"? ?\"?([\w\\\d/]+)\"?', mat_data, flags=re.IGNORECASE)[0]

                    if vtf:
                        VTF.VTF(os.path.join(material_folder, texturePath + '.vtf'))
                elif 'vertexlitgeneric' in mat_data.lower():
                    texturePath = re.findall(r'\"?\$basetexture\"? ?\"?([\w\\\d/]+)\"?', mat_data, flags=re.IGNORECASE)[0]
                    bumpPath = re.findall(r'\"?\$bumpmap\"? ?\"?([\w\\\d/]+)\"?', mat_data, flags=re.IGNORECASE)
                    if bumpPath:
                        bumpPath = os.path.join(material_folder, bumpPath[0] + '.vtf')
                    detailPath = re.findall(r'\"?\$detail\"? ?\"?([\w\\\d/]+)\"?', mat_data, flags=re.IGNORECASE)
                    if detailPath:
                        detailPath = os.path.join(material_folder, detailPath[0] + '.vtf')

                    texturePath = os.path.join(material_folder, texturePath + '.vtf')
                    material_builder.Mat(matName,diff=texturePath,norm=bumpPath,detail=detailPath)

        else:
            for texture in self.MDL.theMdlFileData.theTextures:
                material = self.find_material(texture.thePathFileName,self.MDL.theMdlFileData.theTexturePaths)
                with open(material) as mat:
                    mat_data = mat.read()
                if 'EyeRefract' in mat_data.lower() or 'eyes' in mat_data.lower():
                    texturePath = re.findall(r'\"?\$Iris\"? ?\"?([\w\\\d/]+)\"?', mat_data, flags=re.IGNORECASE)

                    if vtf and texturePath:
                        VTF.VTF(self.find_texture(texturePath[0]))
                elif 'vertexlitgeneric' in mat_data.lower():
                    texturePath = re.findall(r'\"?\$basetexture\"? ?\"?([\w\\\d/]+)\"?', mat_data, flags=re.IGNORECASE)
                    bumpPath = re.findall(r'\"?\$bumpmap\"? ?\"?([\w\\\d/]+)\"?', mat_data, flags=re.IGNORECASE)
                    if bumpPath:
                        bumpPath = self.find_texture(bumpPath[0])
                    else:
                        bumpPath = None
                    detailPath = re.findall(r'\"?\$detail\"? ?\"?([\w\\\d/]+)\"?', mat_data, flags=re.IGNORECASE)
                    if detailPath:
                        detailPath = self.find_texture(detailPath[0])
                    else:
                        detailPath = None
                    if texturePath:
                        texturePath = self.find_texture(texturePath[0])
                    else:
                        texturePath = None
                    print(texture.thePathFileName,texturePath,bumpPath,detailPath)
                    material_builder.Mat(texture.thePathFileName, diff=texturePath, norm=bumpPath, detail=detailPath)




if __name__ == "__main__":
    test_folder = r'E:\MDL_reader\test_data'
    # a = mesh(':\\SteamLibrary\\SteamApps\\common\\SourceFilmmaker\\game\\usermod\\models\\red_eye\\Yoksaharat\\fn_pyrocynical.mdl',True)
    a = mesh(test_folder+ r'\fn_pyrocynical.mdl', True,
             sfm_dir='D:\\SteamLibrary\\SteamApps\\common\\SourceFilmmaker',customName='TEST')
    # print(a.VTX.theVtxFileData.theVtxBodyParts[0].theVtxModelsp[0].theVtxModelLods[0].theVtxMeshes[0].theVtxStripGroups[0])
    # pprint(a.mesh[0])
    # pprint(a.FACES)
