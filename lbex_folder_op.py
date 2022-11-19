import bpy

from bpy.types import Operator

class LBATEX_OT_OpenFolder(Operator):
  
  bl_idname = "object.lbex_ot_openfolder"
  bl_label = "Lazy Open folder."
  bl_description = "Lazy Open the export folder" 
  bl_options = {'REGISTER'}

  def execute(self, context):
    bpy.ops.wm.path_open(filepath=context.scene.export_folder)
    return {'FINISHED'}
