bl_info = {
    "name": "Source Engine model import + textures (.mdl, .file_data, .vtx)",
    "author": "RED_EYE",
    "version": (1, 1),
    "blender": (2, 78, 0),
    "location": "File > Import-Export > SourceEngine MDL (.mdl, .file_data, .vtx) ",
    "description": "Addon allows to import Source Engine models",
    'warning': 'May crash blender',
    # "wiki_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    # "tracker_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    "category": "Import-Export"}

import bpy

from bpy.props import StringProperty, BoolProperty


class MDLImporter(bpy.types.Operator):
    """Load Source Engine MDL models"""
    bl_idname = "import_mesh.mdl"
    bl_label = "Import Mdl"
    bl_options = {'UNDO'}

    filepath = StringProperty(
        subtype='FILE_PATH',
    )
    # WorkDir = StringProperty(name="path to folder with gameinfo.txt", maxlen=1024, default="", subtype='FILE_PATH')
    # Import_textures = BoolProperty(name="Import textures?\nLARGE TEXTURES MAY CAUSE OUT OF MEMORY AND CRASH",
    #                                default=False, subtype='UNSIGNED')
    normal_bones = BoolProperty(name="Make normal skeleton or original from source?", default=False, subtype='UNSIGNED')
    filter_glob = StringProperty(default="*.mdl", options={'HIDDEN'})

    def execute(self, context):
        from . import io_Mdl
        # import_textues = True
        # if self.properties.WorkDir == '':
        #     import_textues = False
        self.WorkDir = ''
        import_textues = False
        self.Import_textures = False
        io_Mdl.IOMdl(self.filepath, working_directory=self.WorkDir,
                     import_textures=import_textues and self.Import_textures,
                     normal_bones=self.normal_bones)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


class VmeshImporter(bpy.types.Operator):
    """Load Source2 Engine VMESH models"""
    bl_idname = "import_mesh.vmesh"
    bl_label = "Import vmehs_c"
    bl_options = {'UNDO'}

    filepath = StringProperty(
        subtype='FILE_PATH',
    )
    filter_glob = StringProperty(default="*.vmesh_c", options={'HIDDEN'})

    def execute(self, context):
        from .Source2 import Vmesh_IO
        # doTexture = True
        # if self.properties.WorkDir == '': doTexture = False
        # io_MDL.IO_MDL(self.filepath, working_directory=self.properties.WorkDir,
        #               import_textures=doTexture and self.properties.Import_textures,
        #               normal_bones=self.properties.normal_bones)
        Vmesh_IO.VMESH_IO(self.filepath).build_meshes()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


class VmdlImporter(bpy.types.Operator):
    """Load Source2 Engine VMESH models"""
    bl_idname = "import_mesh.vmdl"
    bl_label = "Import vmdl_c"
    bl_options = {'UNDO'}

    filepath = StringProperty(
        subtype='FILE_PATH',
    )
    # WorkDir = StringProperty(name="path to folder with gameinfo.txt", maxlen=1024, default="", subtype='FILE_PATH')
    # Import_textures = BoolProperty(name="Import textures?\nLARGE TEXTURES MAY CAUSE OUT OF MEMORY AND CRASH",
    #                                default=False, subtype='UNSIGNED')
    import_meshes = BoolProperty(name="Import meshes", default=False, subtype='UNSIGNED')
    filter_glob = StringProperty(default="*.vmdl_c", options={'HIDDEN'})

    def execute(self, context):
        from .Source2 import Vmdl_IO
        Vmdl_IO.Vmdl_IO(self.filepath, self.import_meshes)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_import(self, context):
    self.layout.operator(MDLImporter.bl_idname, text="MDL mesh (.mdl)")
    self.layout.operator(VmeshImporter.bl_idname, text="Vmesh mesh (.vmesh_c)")
    self.layout.operator(VmdlImporter.bl_idname, text="Vmesh mesh (.vmdl_c)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_import)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_import)


if __name__ == "__main__":
    register()
