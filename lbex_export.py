import bpy
import bmesh
import os
from .lbex_utils import *

class LBatEx_Export:

  def __init__(self, context):
    self.__context = context
    
    self.__export_folder = context.scene.export_folder
    if self.__export_folder.startswith("//"):
      self.__export_folder = os.path.abspath(bpy.path.abspath(context.scene.export_folder))

    self.__center_transform = context.scene.center_transform
    self.__apply_transform = context.scene.apply_transform
    self.__one_material_id = context.scene.one_material_ID
    self.__export_objects = context.selected_objects
    self.__export_animations = context.scene.export_animations
    self.__mat_faces = {}
    self.__materials = []
  
  def do_center(self, obj):
    if self.__center_transform:
      loc = get_object_loc(obj)
      set_object_to_loc(obj, (0,0,0))
      return loc

    return None

  def remove_materials(self, obj):
    if obj.type == 'ARMATURE':
      return False

    mat_count = len(obj.data.materials)

    if mat_count > 1 and self.__one_material_id:

      # Save material ids for faces
      bpy.ops.object.mode_set(mode='EDIT')

      bm = bmesh.from_edit_mesh(obj.data)

      for face in bm.faces:
        self.__mat_faces[face.index] = face.material_index

      # Save and remove materials except the last one
      # so that we keep this as material id
      bpy.ops.object.mode_set(mode='OBJECT')
      self.__materials.clear()

      for idx in range(mat_count):
        self.__materials.append(obj.data.materials[0])
        if idx < mat_count - 1:
          obj.data.materials.pop(index=0)

      return True
    else:
      return False

  def restore_materials(self, obj):

    # Restore the materials for the object
    obj.data.materials.clear()

    for mat in self.__materials:
      obj.data.materials.append(mat)

    obj.data.update()

    # Reassign the material ids to the faces of the mesh
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(obj.data)

    for face in bm.faces:
        mat_index = self.__mat_faces[face.index]
        face.material_index = mat_index

    bmesh.update_edit_mesh(obj.data)

    bpy.ops.object.mode_set(mode='OBJECT')

  def do_export(self):

    bpy.ops.object.mode_set(mode='OBJECT')

    collections=[]
    #print(self.__export_objects)
    #print("-- objects to export")
    for obj in self.__export_objects:
      bpy.ops.object.select_all(action='DESELECT') 
      obj.select_set(state=True)

      if obj.data == None : 
        continue
       
      #print("Exporting object -- "+obj.name) 
      # Select children if exist
      for child in get_children(obj):
        child.select_set(state=True)

      # Remove materials except the last one
      materials_removed = self.remove_materials(obj)

      ex_object_types = { 'MESH' }

      if(self.__export_animations):
        ex_object_types.add('ARMATURE')
      
      # If there is a collection wrapping the object - export the collection
      if len(obj.users_collection) > 0 and obj.users_collection[0].name != "Scene Collection" :
        
        parentCollection =  obj.users_collection[0]
        if not "_" in  parentCollection.name :
          raise Exception(parentCollection.name+" is a wrong collection format to be exported")
        
        # If this collection was already exported - skip
        if parentCollection.name in collections :
          continue

        names=parentCollection.name.split("_")
        
        # If collection has an empty define it as the collection pivot
        center = None
        for child in parentCollection.all_objects :
          if child.data == None :
            center= child
            break
          
        # Apply the collection pivot axis
        if center != None :
          #print("Applying the collection pivot axis")
          parentCollection.instance_offset = center.location
          
          for child in parentCollection.all_objects :
            # Skip Empties
            if child.data == None :
              continue
            # Calculate offset between axis & object
            offsetPosX= child.location.x - center.location.x
            offsetPosY= child.location.y - center.location.y
            offsetPosZ= child.location.z - center.location.z
            
            # Set Pos to zero axis to be exported accordingly
            child.location = [offsetPosX,offsetPosY,offsetPosZ]
            
        # If folder path does not exist create it 
        basePath=self.__export_folder + "\\" + names[0] 
        if not os.path.exists(basePath):
          os.mkdir(basePath)
          
        # Set the parent collection active to be exported
        bpy.context.view_layer.active_layer_collection = getLayerCollection(parentCollection)
        # Export the selected object as fbx
        bpy.ops.export_scene.fbx(check_existing=False,
        # filepath=self.__export_folder + "/" + obj.name + ".fbx",
        filepath=basePath + "\\" + obj.users_collection[0].name  + ".fbx",
        filter_glob="*.fbx",
        use_selection=False,
        use_active_collection=True,
        object_types=ex_object_types,
        bake_anim=self.__export_animations,
        bake_anim_use_all_bones=self.__export_animations,
        bake_anim_use_all_actions=self.__export_animations,
        use_armature_deform_only=True,
        bake_space_transform=self.__apply_transform,
        mesh_smooth_type=self.__context.scene.export_smoothing,
        add_leaf_bones=False,
        path_mode='ABSOLUTE')

        #print("Exported collection- " + parentCollection.name)

        if materials_removed:
          self.restore_materials(obj)
          
        collections.append(parentCollection.name)  
        
        if center != None :
          #print("Restoring to original pos")
          for child in parentCollection.all_objects :
            # Skip Empties
            if child.data == None :
              continue
            # Restore to original pos
            child.location.x += center.location.x
            child.location.y += center.location.y
            child.location.z += center.location.z
      
      # Else - export the single object
      else:
        
        # Center selected object
        old_pos = self.do_center(obj)
      
        names=obj.name.split("_")
        # If folder path does not exist create it 
        basePath=self.__export_folder + "\\" + names[0] 
        if not os.path.exists(basePath):
          os.mkdir(basePath)
          
                # Export the selected object as fbx
        bpy.ops.export_scene.fbx(check_existing=False,
        # filepath=self.__export_folder + "/" + obj.name + ".fbx",
        filepath=basePath + "\\" + obj.name + ".fbx",
        filter_glob="*.fbx",
        use_selection=True,
        use_active_collection=False,
        object_types=ex_object_types,
        bake_anim=self.__export_animations,
         bake_anim_use_all_bones=self.__export_animations,
        bake_anim_use_all_actions=self.__export_animations,
        use_armature_deform_only=True,
        bake_space_transform=self.__apply_transform,
        mesh_smooth_type=self.__context.scene.export_smoothing,
        add_leaf_bones=False,
        path_mode='ABSOLUTE')
        
        print("Exported single- "+ obj.name)

        if materials_removed:
          self.restore_materials(obj)

        if old_pos is not None:
          set_object_to_loc(obj, old_pos)

def getLayerCollection(collection):
    layer_collection = bpy.context.view_layer.layer_collection
    return recurLayerCollection(layer_collection, collection.name)
  
# Recursively transverse layer_collection for a particular name
def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
      return layerColl
    for layer in layerColl.children:
      found = recurLayerCollection(layer, collName)
      if found:
        return found