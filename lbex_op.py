import bpy

from bpy.types import Operator

from .lbex_export import *
	
class LBATEX_OT_Operator(Operator):
    bl_idname = "object.lbex_ot_operator"
    bl_label = "Lazy Batch Export"
    bl_description = "Lazy Export selected objects as fbx" 
    bl_options = {'REGISTER'}
    
    def execute(self, context):

        bat_export = LBatEx_Export(context)
        bat_export.do_export()
        
        self.report({'INFO'}, "Exported to " + context.scene.export_folder)
        return {'FINISHED'}


