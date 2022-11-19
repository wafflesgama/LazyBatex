bl_info = {
    "name" : "Lazy Batex",
    "description" : "Lazy Batch export as Fbx",
    "author" : "jayanam & Guilherme Gama",
    "version" : (0, 0, 2),
    "blender" : (2, 80, 0),
    "location" : "Lazy Batex Panel",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "Import-Export"
}

import bpy
from bpy.props import *

from .lbex_panel import *
from .lbex_op import *
from .lbex_folder_op import *

bpy.types.Scene.export_folder = StringProperty(name="Export folder", 
               subtype="DIR_PATH", 
               description="Directory to export the fbx files into")

bpy.types.Scene.center_transform = BoolProperty(name="Center transform",
                default=True,
                description="Set the pivot point of the object to the center")

bpy.types.Scene.apply_transform = BoolProperty(name="Apply transform",
                default=True,
                description="Applies scale and transform (Experimental)")

bpy.types.Scene.export_smoothing = EnumProperty(
    name="Smoothing",
    description="Defines the export smoothing information",
    items=(
        ('EDGE', 'Edge', 'Write edge smoothing',0),
        ('FACE', 'Face', 'Write face smoothing',1),
        ('OFF', 'Normals Only', 'Write normals only',2)
        ),
    default='OFF'
    )

bpy.types.Scene.export_animations = BoolProperty(name="Export Rig & Animations",
                default=False,
                description="Export rig and animations")

bpy.types.Scene.one_material_ID = BoolProperty(name="One material ID",
                default=True,
                description="Export just one material per object")

classes = ( LBATEX_PT_Panel, LBATEX_OT_Operator, LBATEX_OT_OpenFolder)

register, unregister = bpy.utils.register_classes_factory(classes)
    
if __name__ == "__main__":
    register()
