import bpy
from bpy.types import Panel

class LBATEX_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Lazy Batch Fbx export"
    bl_category = "Lazy Batex"
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text="Export folder:")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "export_folder", text="")

        col = row.column()
        col.operator('object.lbex_ot_openfolder', text='', icon='FILE_TICK')

        row = layout.row()
        row.prop(context.scene, "center_transform", text="Center transform")

        row = layout.row()
        row.prop(context.scene, "apply_transform", text="Apply transform")

        row = layout.row()
        row.prop(context.scene, "one_material_ID")

        row_smooth = layout.row()
        col_smooth_lbl = row_smooth.column()
        col_smooth_lbl.label(text="Smoothing:")

        col_smooth = row_smooth.column()
        col_smooth.alignment = 'EXPAND'
        col_smooth.prop(context.scene, "export_smoothing", text="")

        row = layout.row()
        row.prop(context.scene, "export_animations")

        row = layout.row()
        row.operator('object.lbex_ot_operator', text='Lazy Export')



