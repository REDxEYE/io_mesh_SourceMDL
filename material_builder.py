import bpy
import os.path
op = os.path.join

materials = bpy.data.materials

class Mat:


    def getName(self,filepath:str):
        return filepath.split(os.sep)[-1][:-4]


    def hasAlready(self,name):
        for img in bpy.data.images:
            if img.name == self.getName(name):
                return img
        return False

    def __init__(self,material:str,diff = None,spec = None,glos = None,norm = None, detail = None,detail_scale = 0):
        vtf = True
        try:
            if 'VTF' not in globals() or 'VTF' not in locals():
                import VTF
        except:
            print("IO_TEXTURE_VTF NOT INSTALLED!")
            vtf = False
        material = materials.get(material) or materials.new(material)
        material.use_nodes = True
        self.links = material.node_tree.links
        self.material = material
        self.nodes = material.node_tree.nodes
        self.diff = diff
        self.spec = spec
        self.glos = glos
        self.norm = norm
        self.detail = detail
        self.detail_scale = detail_scale
        if vtf:
            for n in self.nodes:
                self.nodes.remove(n)
            if self.diff:
                self.diff_t = self.hasAlready(self.diff) or VTF.VTF(self.diff).import_texture()
            if self.spec:
                self.spec_t = self.hasAlready(self.spec) or VTF.VTF(self.spec).import_texture()
            if self.glos:
                self.glos_t = self.hasAlready(self.glos) or VTF.VTF(self.glos).import_texture()
            if self.norm:
                self.norm_t = self.hasAlready(self.norm) or VTF.VTF(self.norm).import_texture()
            if self.detail:
                self.detail_t = self.hasAlready(self.detail) or VTF.VTF(self.detail).import_texture()

        matout = self.nodes.new(type='ShaderNodeOutputMaterial')
        principled = self.nodes.new(type="ShaderNodeBsdfPrincipled")
        principled.location = -200, 0

        self.links.new(matout.inputs['Surface'],principled.outputs['BSDF'])

        normal_map = self.nodes.new(type="ShaderNodeNormalMap")
        normal_map.location = -400, -390

        self.links.new(principled.inputs['Normal'], normal_map.outputs['Normal'])

        if self.diff!=None:

            diff_node = self.nodes.new(type="ShaderNodeTexImage")
            diff_node.location = -600, -20
            if vtf:
                diff_node.image = self.diff_t
            self.links.new(diff_node.outputs['Color'],principled.inputs['Base Color'])

        if self.norm!=None:

            norm_node = self.nodes.new(type="ShaderNodeTexImage")
            norm_node.location = -600, -350
            if vtf:
                norm_node.image = self.norm_t
            norm_node.color_space = 'NONE'

            self.links.new(norm_node.outputs['Color'],normal_map.inputs['Color'])

        if self.glos!=None:

            glos_node = self.nodes.new(type="ShaderNodeTexImage")
            glos_node.location = -600, -250
            if vtf:
                glos_node.image = self.glos_t
            glos_node.color_space = 'NONE'

            self.links.new(glos_node.outputs['Color'],principled.inputs['Roughness'])

        elif self.spec!=None:

            spec_node = self.nodes.new(type="ShaderNodeTexImage")
            spec_node.location = -600, -250
            if vtf:
                spec_node.image = self.spec_t
            spec_node.color_space = 'NONE'
            inv_node = self.nodes.new(type="ShaderNodeInvert")
            inv_node.location = -400, -200

            self.links.new(spec_node.outputs['Color'],inv_node.inputs['Color'])

            self.links.new(inv_node.outputs['Color'],principled.inputs['Roughness'])




if __name__ == '__main__':
    p = r'E:\PYTHON\VTF_reader\test_data'
    a = Mat('test',op(p,'belly.vtf'),norm = op(p,'N.vtf'),spec= op(p,'test.vtf'))
