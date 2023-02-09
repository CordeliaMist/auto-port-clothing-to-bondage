bl_info = {
	"name": "CK Helper Tools",
	"author": "Cordelia Mist",
	"version": (1, 0, 0),
	"blender": (3, 2, 0),
	"location": "View3D",
	"description": "Only Use this tool for CK Tutorial uses, I cannot garentee how it will act outside of them. As in it could possibly start adding modifiers to random objects if used outside of the purpose of the tutorials they are made for.",
	"category": "All"
}

import bpy

# I know this class is messy, I have yet to learn how to funtionalize inside the prompt of a addon
''' Clean up a collection of its objects '''
class ClothingToBondageOperator(bpy.types.Operator):
	bl_idname = "object.fix_clothing_to_bondage"
	bl_label = "Clothing To Bondage"
	bl_description= "For this to work, you must have:\n\
					<> A Collection named 'Bondage Addon Helpers' for POSE SOURCE & MODIFIER SOURCE\n\
					<> A Collection named 'Downloaded Bondage Parts'\n\
					<> A Collection named 'Clothing Mod' for the gear Mod"
	def execute(self, context):
		# if not in object mode already, default to it
		bpy.ops.object.mode_set(mode='OBJECT')
		''' Function 1: Apply all transforms, Fix Alpha Blends, and Toggle Bones'''
		collection = bpy.data.collections.get("Clothing Mod")
		# Select all objects under the collection and its hierarchy
		for obj in collection.all_objects:
			obj.select_set(True)
		# Apply all transformations
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		
		# Iterate through each object in the collection
		for obj in collection.objects:
			# If the object is a mesh and not an armature
			if obj.type == 'MESH':
				# change its material to alpha-hashed
				for mat in obj.data.materials:
					mat.blend_method = 'HASHED'

			# Iterate through all objects in the scene
			for obj in bpy.context.scene.objects:
				# Check if the object is an armature
				if obj.type == 'ARMATURE':
					# Toggle the x-ray of the armature
					obj.display_type = 'WIRE'
					
		# remove n_root modifiers from download bondage parts collection if any
		collection = bpy.data.collections.get("Downloaded Bondage Parts")
		# Iterate through each object in the collection
		for obj in collection.objects:
			bpy.context.view_layer.objects.active = obj
			while obj.modifiers:
				bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)

		# Function 2: Copies the pose from an object with the keyword SOURCE to an armature with the keyword DEST '''
		# Function 2 name: armature_to_bondagepose()
		# Locate the POSE_SOURCE in the Addon Helpers
		pose_source = None
		for obj in bpy.data.objects:
			if obj.type == 'ARMATURE' and "POSE SOURCE" in obj.name:
				pose_source = obj
				break
		# Make the source armature the active object
		bpy.context.view_layer.objects.active = pose_source
		# Enter pose mode
		bpy.ops.object.mode_set(mode='POSE')
		# Select all bones in the source armature
		bpy.ops.pose.select_all(action='SELECT')
		# Copy the pose
		bpy.ops.pose.copy()
		# Enter object mode
		bpy.ops.object.mode_set(mode='OBJECT')

		# Next, Locate the clothing Mod collection
		destcollection = bpy.data.collections.get("Clothing Mod")
		if destcollection:
			# Iterate through each object in the collection
			for obj in destcollection.objects:
				if obj.type == 'ARMATURE':
					pose_dest = obj
				break
		else:
			print("Clothing Mod collection not found")

		# Make the destination armature the active object
		bpy.context.view_layer.objects.active = pose_dest
		# Enter pose mode
		bpy.ops.object.mode_set(mode='POSE')
		# Select all bones in the destination armature
		bpy.ops.pose.select_all(action='SELECT')
		# Paste the pose
		bpy.ops.pose.paste()
		# Enter object mode
		bpy.ops.object.mode_set(mode='OBJECT')
		
		'''Function 3: Cleans up the bones and resets to rest A-Pose after the modifier applies'''
		# Function 3 Name: def cleanup_bondagepose_transfer():
		# Apply the armature modifier to each objects in the clothing mod
		collection = bpy.data.collections.get("Clothing Mod")
		if collection:
			# Iterate through each object in the collection
			for obj in collection.objects:
				if obj.type == 'MESH':
					# Convert all objects to meshes
					bpy.context.view_layer.objects.active = obj
					while obj.modifiers:
						bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)

			# Next, reset the pose
			for obj in collection.objects:
				if obj.type == 'ARMATURE':  
					# sets object to active selection
					bpy.context.view_layer.objects.active = obj
					# Sets it to pose mose
					bpy.ops.object.mode_set(mode='POSE')
					# Select all bones in the source armature
					bpy.ops.pose.select_all(action='SELECT')
					# reset the pose to rest
					obj.data.pose_position = 'REST'
					# Enter object mode
					bpy.ops.object.mode_set(mode='OBJECT')
		else:
			print("Clothing Mod Collection not Found")
		
					
		'''Function 4: Update all weights of the clothing mod to the newly bound state'''
		# Function 4 Name: def update_weights_for_bondage():
		# Locate the modifier source OBJ and store it
		modifiersource_obj = None
		for obj in bpy.data.objects:
			if obj.type == 'MESH' and "MODIFIER SOURCE" in obj.name:
				modifiersource_obj = obj

		# Store the armature n_root object and the object list for the children under n_root
		collection = bpy.data.collections.get("Clothing Mod")
		armature_obj = collection.objects['n_root'] # Creating the n_root armature object
		mesh_objs = [obj for obj in armature_obj.children if obj.type == 'MESH'] # appending list objects under it

		# For each object under n_root
		for mesh_obj in mesh_objs:
			# for each modifier in the source object      
			# Select the current object as the active mesh so we can apply modifiers from it
			bpy.context.view_layer.objects.active = mesh_obj
			# This FOR-loop will create the same number of modifiers that the MODIFIER SOURCE mesh object has
			# and then perform the actions within for each modifier
			for modif in modifiersource_obj.modifiers:
				# Create the modifier (referencing to add the same modifier as the one in MODIFIER SOURCE
				mesh_obj.modifiers.new(modif.name, modif.type)
				# declare the modifier we are now interfacing with will be Part 0.0's "i'th" modifier
				# This modifier index[-1] means the top modifier on the list. [-2] would mean the second to top
				dest_mod = mesh_obj.modifiers[-1]

				#next, check if the modifier used to anchor the bondage is a vertex group in the mesh
				if modif.vertex_group_a not in mesh_obj.vertex_groups:
					# then append the bondage bone to it
					mesh_obj.vertex_groups.new(name=modif.vertex_group_a)

				#then for each propertiy in the mod keys set the attributes
				dest_mod.vertex_group_a = modif.vertex_group_a
				dest_mod.vertex_group_b = modif.vertex_group_b

				tmp_vertgroup = None
				# check if the vertex group B applied
				if dest_mod.vertex_group_b == modif.vertex_group_b:
					# assign tmpvertgroup so it is retained after modifier is applied. 
					tmp_vertgroup = modif.vertex_group_b
				# set remaining properties for the modifier
				dest_mod.mix_set = modif.mix_set
				dest_mod.mix_mode = modif.mix_mode

				# apply the modifier we just worked on
				bpy.ops.object.modifier_apply(modifier=dest_mod.name)

				# then if it applied new weights from a vertex, remove that vertex group from the mesh
				if tmp_vertgroup != None:
					mesh_obj.vertex_groups.remove(mesh_obj.vertex_groups[tmp_vertgroup])

		'''Function 5: Prepare newly bound cloth for export'''
		# Function 5 Name: def prep_export():
		# Finally add back the n_root armature modifier for export
		collection = bpy.data.collections["Clothing Mod"]
		armature_obj = collection.objects['n_root'] # Creating the n_root armature object
		mesh_objs = [obj for obj in armature_obj.children if obj.type == 'MESH'] # appending list objects under it
		for mesh_obj in mesh_objs:
			# Add armature modifier to the mesh object
			armature_modifier = mesh_obj.modifiers.new(type='ARMATURE', name="Armature Modifier")
			armature_modifier.object = armature_obj # set the object to the parent

		collection2 = bpy.data.collections["Downloaded Bondage Parts"]
		# After this, move the bondage part objects into the clothing mod collection and parent them to n_root
		for obj in collection2.objects:
			# move it to the clothing mod collection
			collection2.objects.unlink(obj)
			collection.objects.link(obj)
			# set its parent
			obj.parent = armature_obj
			
		### ADD N_ROOT TO ALL [Downloaded Bondage Parts] COLLECTION OBJECTS ###        
		# Iterate through each object in the collection
		for obj in collection.objects:
			if obj.type == 'MESH':
				# apply all modifiers
				bpy.context.view_layer.objects.active = obj
				while obj.modifiers:
					bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)

				# Then add armature modifier with clothing mods n_root as the source
				armature_modifier = obj.modifiers.new(type='ARMATURE', name="Armature Modifier")
				armature_modifier.object = armature_obj # set the object to the parent



		### HIDE ALL OBJECTS IN [Bondage Addon Helpers] COLLECTION ###
		for obj in bpy.data.collections["Bondage Addon Helpers"].objects:
			obj.hide_set(True)
			
			
		return {'FINISHED'}

class FixSkinSeamsOperator(bpy.types.Operator):
	bl_idname = "object.fix_skin_seams"
	bl_label = "Fix Skin Seams"
	bl_description= "Be sure to do this BEFORE you use auto-port to bondage!\n\
					If you already have, just CTRL+Z to before you pressed the button and use this first!\n\
					IMPORTANT NOTE: your skin group MUST be in Part 0.X for this to work!"
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')
		# typical get full list under n_root, but this time only put Part 0.0 objects in it.
		collection = bpy.data.collections.get("Clothing Mod")
		armature_obj = collection.objects['n_root'] # Creating the n_root armature object
		mesh_objs = [obj for obj in armature_obj.children if obj.type == 'MESH' and 'Part 0.' in obj.name]
		
		# for all Part 0.X objects
		for i in mesh_objs:
			i.select_set(True)
		# Merge the selected objects to the first
		bpy.context.view_layer.objects.active = mesh_objs[0]
		bpy.ops.object.join()
		
		# merge by distance after joining
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action='SELECT')
		bpy.ops.mesh.remove_doubles(threshold=0.00001)
		# set it back to object mode
		bpy.ops.object.mode_set(mode='OBJECT')
		
		# return done.
		return {'FINISHED'}
		
class PrepBondagePartsOperator(bpy.types.Operator):
	bl_idname = "object.prep_bondage_parts"
	bl_label = "Prep Bondage Parts"
	bl_description= "Applies the transformations to the bondage mod so it wont fall on the floor when you delete parts"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')
		collection = bpy.data.collections.get("Downloaded Bondage Parts")
		# Select all objects under the collection and its hierarchy
		for obj in collection.all_objects:
			obj.select_set(True)
		# Apply all transformations
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		
		# return done.
		return {'FINISHED'}
	
class ClothingToBondagePanel(bpy.types.Panel):
	bl_idname = "object.clothing_to_bondage_panel"
	bl_label = "CK Helper Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = 'UI'
	bl_category = "CK Helpers"

	def draw(self, context):
		layout = self.layout
		scene = context.scene

		row = layout.row()
		row.scale_y = 1.0
		layout.label(text = "Auto-Port Clothing To Bondage:")
		
		row = layout.row()
		row.operator(
			"wm.url_open",
			text="Guide for Further Details",
			icon="HELP"
		).url = "https://docs.google.com/document/d/1dAYyE5sBWvKKXOktDmMmRR4xP8z7yPLQf3uj3ZxxkFs/edit?usp=sharing"   
				
		row = layout.row()
		row.scale_y = 1.0
		row.operator("object.prep_bondage_parts", text="Prep Bondage Parts", icon="BRUSH_DATA")
		
		row = layout.row()
		row.scale_y = 1.0
		row.operator("object.fix_skin_seams", text="Fix Skin Seams", icon="INVERSESQUARECURVE")
		
		row = layout.row()
		row.scale_y = 2.0
		row.operator("object.fix_clothing_to_bondage", text="Auto-Port to Bondage", icon="MOD_CLOTH")
		
		row = layout.row()
		row.scale_y = 1.0
		layout.label(text = "More Helper tools TBD!..")        

def register():
	bpy.utils.register_class(ClothingToBondageOperator)
	bpy.utils.register_class(FixSkinSeamsOperator)
	bpy.utils.register_class(PrepBondagePartsOperator)
	bpy.utils.register_class(ClothingToBondagePanel)
	
def unregister():
	bpy.utils.unregister_class(ClothingToBondagePanel)
	bpy.utils.unregister_class(FixSkinSeamsOperator)
	bpy.utils.unregister_class(PrepBondagePartsOperator)
	bpy.utils.unregister_class(ClothingToBondageOperator)

if __name__ == "__main__":
    register()