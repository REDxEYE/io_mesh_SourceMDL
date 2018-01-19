bl_info = {
    "name": "Source Engine model import + textures (.mdl, .vvd, .vtx)",
    "author": "RED_EYE",
    "version": (1, 1),
    "blender": (2, 78, 0),
    "location": "File > Import-Export > SourceEngine MDL (.mdl, .vvd, .vtx) ",
    "description": "Addon allows to import Source Engine models",
    'warning': 'May crash blender',
    # "wiki_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    # "tracker_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    "category": "Import-Export"}
from . import io_MDL

if "bpy" in locals():
    import importlib

    # if "export_json" in locals():
    #    importlib.reload(export_json)
    if "MDL_import" in locals():
        importlib.reload(io_MDL)
else:
    import bpy

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper


class MDLImporter(bpy.types.Operator):
    """Load Source Engine MDL models"""
    bl_idname = "import_mesh.mdl"
    bl_label = "Import Mdl"
    bl_options = {'UNDO'}

    filepath = StringProperty(
        subtype='FILE_PATH',
    )
    WorkDir = StringProperty(name="path to folder with gameinfo.txt", maxlen=1024, default="", subtype='FILE_PATH')
    Import_textures = BoolProperty(name="Import textures?\nLARGE TEXTURES MAY CAUSE OUT OF MEMORY AND CRASH",
                                   default=False, subtype='UNSIGNED')
    forrig = BoolProperty(name="Make normal skeleton or original from source?", default=False, subtype='UNSIGNED')
    filter_glob = StringProperty(default="*.mdl", options={'HIDDEN'})

    def execute(self, context):
        from . import io_MDL
        doTexture = True
        if self.properties.WorkDir == '': doTexture = False
        io_MDL.IO_MDL(self.filepath, working_directory=self.properties.WorkDir,
                      import_textures=doTexture and self.properties.Import_textures,
                      normal_bones=self.properties.forrig)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_import(self, context):
    self.layout.operator(MDLImporter.bl_idname, text="MDL mesh (.mdl)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_import)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_import)


if __name__ == "__main__":
    register()
