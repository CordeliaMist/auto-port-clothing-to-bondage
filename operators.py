import bpy
from bpy.props import StringProperty

# spesified collection import
class ImportGearmod(bpy.types.Operator):
	bl_idname = "object.import_gearmod"
	bl_label = "Import Gear Mod"
	bl_description= "Import Gear Mod"
	filepath: bpy.props.StringProperty(subtype="FILE_PATH")
	def execute(self, context):
		bpy.ops.import_scene.fbx(filepath=self.filepath)
		# Transfer to right collection
		clothingmodcollection = bpy.data.collections["Clothing Mod"]
		for obj in bpy.context.selected_objects:
			collections = obj.users_collection
			linked = False
			for collection in collections:
				if collection.name != "Clothing Mod":
					collection.objects.unlink(obj)
				else:
					linked = True
			if not linked:
				clothingmodcollection.objects.link(obj)
		return {'FINISHED'}
	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
###############################################################
class ImportBondage(bpy.types.Operator): # Import Bondage Class
	bl_idname = "object.import_bondage"
	bl_label = "Import Bondage"
	bl_description= "Import Bondage"
	filepath: bpy.props.StringProperty(subtype="FILE_PATH")
	def execute(self, context):
		bpy.ops.import_scene.fbx(filepath=self.filepath)
		# Transfer to right collection
		bondagemodcollection = bpy.data.collections["Downloaded Bondage Parts"]
		for obj in bpy.context.selected_objects:
			collections = obj.users_collection
			linked = False
			for collection in collections:
				if collection.name != "Downloaded Bondage Parts":
					collection.objects.unlink(obj)
				else:
					linked = True
			if not linked:
				bondagemodcollection.objects.link(obj)
		return {'FINISHED'}
	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}
###############################################################
class ExportBoundGearmod(bpy.types.Operator): # Export Class
	bl_idname = "object.export_bound_gearmod"
	bl_label = "Export Bound Gearmod"
	bl_description= "Export Bound Gearmod"
	filepath: bpy.props.StringProperty(subtype="FILE_PATH")
	def execute(self, context):
				
		# Select all objects for export
		bpy.ops.object.select_all(action='DESELECT')
		collection = bpy.data.collections.get("Clothing Mod")
		for obj in collection.all_objects:
			obj.select_set(True)
		# This part is left out because i spent hours trying to get it to work & it wouldnt.
		''' 
		# Export the file
		bpy.ops.export_scene.fbx(filepath=self.filepath, use_selection = True, add_leaf_bones = False)
		'''
		# Done
		return {'FINISHED'}

	#def invoke(self, context, event):
	#	context.window_manager.fileselect_add(self)
	#	return {'RUNNING_MODAL'}

###############################################################
# A quick function to be called to make sure we are in object mode each time a button is pressed.
def set_object_mode():
	if bpy.context.object and bpy.context.object.mode != 'OBJECT':
		bpy.ops.object.mode_set(mode='OBJECT')

###############################################################
class PrepModels(bpy.types.Operator):
	bl_idname = "object.prep_models"
	bl_label = "Prepare Models"
	bl_description= "Should automatically locate the bondage parts based on the mod imported / preset scene used"
	
	def execute(self, context):
		# check to see if in object mode and/or set to object mode.
		set_object_mode()
		
		# First nesessity, change all materials to alpha-hashed over alpha-blend
		for mtrl in bpy.data.materials:
			mtrl.blend_method = 'HASHED'
		
		# Second nesessity, Make all armatures be in wireframe mode
		for obj in bpy.context.scene.objects:
			if obj.type == 'ARMATURE':
				obj.display_type = 'WIRE'
				
		# Next, select all objects under CLOTHING MOD collection & apply all transforms
		collection = bpy.data.collections.get("Clothing Mod")
		for obj in collection.all_objects:
			obj.select_set(True)
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		
		# Go through it again, but this time clearing the groups
		for obj in collection.objects:
			if "Group" in obj.name:
				for child in obj.children:
					bpy.data.objects.remove(child)
				bpy.data.objects.remove(obj)
		
		# Finally, remove the n_root modifiers from download bondage parts collection if any
		collection = bpy.data.collections.get("Downloaded Bondage Parts")
		# Iterate through collection twice, once for apply transforms, another for modifiers
		for obj in collection.all_objects:
			obj.select_set(True)
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		
		for obj in collection.objects:
			bpy.context.view_layer.objects.active = obj
			while obj.modifiers:
				bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)
		
		# Quickly ensure that the Clothing Mod's n_root is named n_root
		for obj in bpy.data.collections["Clothing Mod"].objects:
			if obj.type == 'ARMATURE':
				if obj.name != "n_root":
					obj.name = "n_root"
					break
				break
				
		# Deselect
		bpy.ops.object.select_all(action='DESELECT')
		
		return {'FINISHED'}
###############################################################
# Function for the enum, will run when called and only return 
def get_names_list(option):
	if option == "MOD_1":
		# leather armbinder
		return ["Part 1.0", "Part 1.1"]
	elif option == "MOD_2":
		# Box Tie Bondage
		return ["Part 1.0", "Part 1.1"]
	elif option == "MOD_3":
		# Rope Harness + Armbinder
		return ["Part 1.0", "Part 1.1", "Part 1.2", "Part 1.3", "Part 1.4", "Part 1.5"]
	elif option == "MOD_4":
		# (Gen3) Rope Leg Bondage
		return ["Part 1.0", "Part 1.1", "Part 1.2", "Part 1.3", "Part 1.4", "Part 1.5"]
	elif option == "MOD_5":
		# (Bibo+) Rope Leg Bondage
		return ["Part 3.0", "Part 3.1", "Part 3.2", "Part 3.3", "Part 3.4", "Part 3.5"]
	elif option == "MOD_6":
		# (Gen3) Frogtie Bondage
		return ["Part 1.0"]
	elif option == "MOD_7":
		# (Bibo+) Frogtie Bondage
		return ["Part 3.0"]
	elif option == "MOD_8":
		# Bondage Tape Chest Wrap
		return ["Part 2.0", "Part 2.1", "Part 2.2", "Part 2.3", "Part 2.4"]
	elif option == "MOD_9":
		# (Gen3) Bondage Tape Leg Wrap
		return ["Part 2.0", "Part 2.1", "Part 2.2", "Part 2.3", "Part 2.4", "Part 2.5"]
	elif option == "MOD_10":
		# (Bibo+) Bondage Tape Leg Wrap
		return ["Part 3.0", "Part 3.1", "Part 3.2", "Part 3.3", "Part 3.4", "Part 3.5"]
	elif option == "MOD_11":
		# Metal Stock
		return ["Part 1.0", "Part 1.1", "Part 1.2"]
	elif option == "MOD_12":
		# (Gen3) Spreader Bar
		return ["Part 2.0", "Part 2.1", "Part 2.2", "Part 2.3", "Part 3.0", "Part 3.1", "Part 3.2", "Part 3.3",]
	elif option == "MOD_13":
		# (Bibo+) Spreader Bar
		return ["Part 1.0", "Part 1.1", "Part 1.2", "Part 1.3", "Part 2.0", "Part 2.1", "Part 2.2", "Part 2.3",]
	else:
		return []
###############################################################
class IsolateBondage(bpy.types.Operator):
	bl_idname = "object.isolate_bondage"
	bl_label = "Located Parts"
	bl_description= "Should automatically isolate bondage parts from the rest of the model"
		
	def execute(self, context):
		# Prepare to remove parts from the downloaded bondage parts collection
		scene = context.scene
		# make selected_option == the current selection in dropdown
		selected_option = scene.autoport_mod_selector
		# get a list named partname_list, which will get the correct part whitelist for the spesified mod
		partname_list = get_names_list(selected_option)
		
		collection = bpy.data.collections["Downloaded Bondage Parts"]
		# Iterate over each object in the collection:
		for obj in collection.objects:
			# Initialize a flag to keep track of whether any of the names are a part of the object's name:
			is_part = False
			# Iterate over each name in the list:
			for partname in partname_list:
				# Check if the current name is a part of the object's name:
				if partname in obj.name:
					# If it is, set the flag and break out of the loop:
					is_part = True
					break
			# If none of the names are a part of the object's name, remove the object:
			if not is_part:
				bpy.data.objects.remove(obj)
		
		# Deselect
		bpy.ops.object.select_all(action='DESELECT')
		
		# return done.
		return {'FINISHED'}
###############################################################	
class BatchRenameBondage(bpy.types.Operator):
	bl_idname = "object.batch_rename_bondage"
	bl_label = "Batch Rename Bondage"
	bl_description= "Batch renames all bondage mods conprised of a single group"
		
	def execute(self, context):
		collection = bpy.data.collections["Clothing Mod"]
		armature_obj = collection.objects['n_root'] # Creating the n_root armature object
		mesh_objs = [obj for obj in armature_obj.children if obj.type == 'MESH'] # appending list objects under it
		# Before transferring the objects over, give them an appropriate group, which is one higher than the highest part X.#
		lastobjname = mesh_objs[len(mesh_objs) - 1].name
		
		# once we have identified the lastobjname, batch rename all objects in Downloaded Bondage Parts collection:
		collection2 = bpy.data.collections["Downloaded Bondage Parts"]
		for obj in collection2.objects:
			if "Part 1." in lastobjname:
				helper_replace_name(obj,"Part 2.")			
			elif "Part 2." in lastobjname:
				helper_replace_name(obj,"Part 3.")
			elif "Part 3." in lastobjname:
				helper_replace_name(obj,"Part 4.")
			elif "Part 4." in lastobjname:
				helper_replace_name(obj,"Part 5.")
			else:
				# Last object is part 5:
				helper_replace_name(obj,"Part 6.")
				
		# Deselect
		bpy.ops.object.select_all(action='DESELECT')
		
		# Done				
		return {'FINISHED'}
###############################################################
class BlendSkinGroupZero(bpy.types.Operator):
	bl_idname = "object.blend_skin_groupzero"
	bl_label = "Fix Skin Seams"
	bl_description= "Be sure to do this BEFORE you use auto-port to bondage!\n\
					If you already have, just CTRL+Z to before you pressed the button and use this first!\n\
					IMPORTANT NOTE: your skin group MUST be in Part 0.X for this to work!"
	def execute(self, context):
		# check to see if in object mode and/or set to object mode.
		set_object_mode()
		
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
		
		# Deselect
		bpy.ops.object.select_all(action='DESELECT')
		
		# return done.
		return {'FINISHED'}
##############################################################
''' Func 1: Copies the pose from an object with the keyword SOURCE to an armature with the keyword DEST '''
def transfer_to_locked_pose():
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

''' Func 2: Cleans up the bones and resets to rest A-Pose after the modifier applies'''
def transfer_cleanup():
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

''' Func 3: Update all weights of the clothing mod to the newly bound state'''
def perform_locked_weight_transfers():
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
			# Set a tmp vert group for later
			tmp_vertgroup = None
			# Call this statement to see if the modifiers vert group is even in the obj's verts
			if modif.vertex_group_b in mesh_obj.vertex_groups:
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
	
''' Func 4: Prepare newly bound cloth for export'''
# helper function
def helper_replace_name(obj, new_partname):
	if "Part 1." in obj.name:
		obj.name = obj.name.replace("Part 1.",new_partname)
	elif "Part 2." in obj.name:
		obj.name = obj.name.replace("Part 2.",new_partname)
	elif "Part 3." in obj.name:
		obj.name = obj.name.replace("Part 3.",new_partname)
	else:
		obj.name = obj.name.replace("Part 4.",new_partname)

def prep_export():
	# Finally add back the n_root armature modifier for export
	collection = bpy.data.collections["Clothing Mod"]
	armature_obj = collection.objects['n_root'] # Creating the n_root armature object
	mesh_objs = [obj for obj in armature_obj.children if obj.type == 'MESH'] # appending list objects under it
	for mesh_obj in mesh_objs:
		# Add armature modifier to the mesh object
		armature_modifier = mesh_obj.modifiers.new(type='ARMATURE', name="Armature Modifier")
		armature_modifier.object = armature_obj # set the object to the parent

	# After this, move the bondage part objects into the clothing mod collection and parent them to n_root
	collection2 = bpy.data.collections["Downloaded Bondage Parts"]
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

''' Auto-Port Process'''
class AutoPortCtB(bpy.types.Operator):
	bl_idname = "object.autoport_ctb"
	bl_label = "Clothing To Bondage"
	bl_description= "If you get an error, you have probably done something wrong, so CTRL+Z until you get back to normal if you do"
	def execute(self, context):
		# check to see if in object mode and/or set to object mode.
		set_object_mode()
		
		# If any objects in the bondage Addon Helpers are disabled, re-enable them
		for obj in bpy.data.collections["Bondage Addon Helpers"].objects:
			obj.hide_set(False)
		
		# Copies the pose from an object with the keyword SOURCE to an armature with the keyword DEST
		transfer_to_locked_pose()
		
		# Clean up the bones and resets to rest A-Pose 
		transfer_cleanup()
		
		# automatic weight transfer from modifier source to clothing to update locked state.
		perform_locked_weight_transfers()
		
		prep_export()
		
		# Deselect
		bpy.ops.object.select_all(action='DESELECT')
		# Done
		return {'FINISHED'}

# Helper function to do the same for the selected hand object
def perform_locked_weight_transfers_hands(mesh_obj):
	# Locate the modifier source OBJ and store it
	for obj in bpy.data.collections["Bondage Addon Helpers"].objects:
		obj.hide_set(False)
	
	modifiersource_obj = None
	for obj in bpy.data.objects:
		if obj.type == 'MESH' and "HAND MODIF SOURCE" in obj.name:
			modifiersource_obj = obj
			
	bpy.context.view_layer.objects.active = mesh_obj
	# This FOR-loop will create the same number of modifiers that the MODIFIER SOURCE mesh object has
	# and then perform the actions within for each modifier
	for modif in modifiersource_obj.modifiers:
		# Set a tmp vert group for later
		tmp_vertgroup = None
		# Call this statement to see if the modifiers vert group is even in the obj's verts
		if modif.vertex_group_b in mesh_obj.vertex_groups:
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

	for obj in bpy.data.collections["Bondage Addon Helpers"].objects:
		obj.hide_set(True)
class TransferHandFeet(bpy.types.Operator):
	bl_idname = "object.transfer_handfeet"
	bl_label = "Transfer HandFeet"
	bl_description= "Transfer teh hands or teh feet"
	def execute(self, context):
		# check to see if in object mode and/or set to object mode.
		set_object_mode()
	
		# get armature data
		collection = bpy.data.collections["Clothing Mod"]
		armature_obj = collection.objects['n_root'] # Creating the n_root armature object
		
		# Get the currently selected hands
		scene = context.scene
		# Get ENUM for selected option
		cur_handfeet_opt = scene.handfeet_selector

		# NameIncludeKey
		handfeet_name = None
		# If Gen3
		if cur_handfeet_opt == 'HANDFEET1':
			handfeet_name = "T&F"
		# If Bibo+
		elif cur_handfeet_opt == 'HANDFEET2':
			handfeet_name = "Bibo+"
		# If Vanilla
		else:
			handfeet_name = "Vanilla"
		
		handfeet_collection = bpy.data.collections['Hands/Feet']
		# Show the hands
		for obj in bpy.data.collections["Hands/Feet"].objects:
			obj.hide_set(False)
		# Transer the object over if the right name, then break
		for obj in handfeet_collection.objects:
			# find the right hand/feet object
			if handfeet_name in obj.name:
				# Get the armature from the bondage addon helpers
				helper_armature = None
				for obj2 in bpy.data.objects:
					if obj2.type == 'ARMATURE' and "POSE SOURCE" in obj2.name:
						helper_armature = obj2
						break
				# Add new armature modifier and set it to pose source.
				armature_modifier = obj.modifiers.new(type='ARMATURE', name="Armature Modifier")
				armature_modifier.object = helper_armature
				# Do the weight transfers to it after applying the modifier
				bpy.context.view_layer.objects.active = obj
				while obj.modifiers: # Apply the modifier to set the pose
					bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)
				# Do weight transfers
				perform_locked_weight_transfers_hands(obj)
				
				# Add armature modifier with clothing mods n_root as the source
				armature_modifier = obj.modifiers.new(type='ARMATURE', name="Armature Modifier")
				armature_modifier.object = armature_obj # set the object to the parent
				# Then move it to the clothing mod collection
				handfeet_collection.objects.unlink(obj)
				collection.objects.link(obj)
				# And set its parent to n_root
				obj.parent = armature_obj
				break
		# Deselect
		bpy.ops.object.select_all(action='DESELECT')	

		# Hide hand/feet again
		for obj in bpy.data.collections["Hands/Feet"].objects:
			obj.hide_set(True)
		# Done
		return {'FINISHED'}
		
classes = [
	ImportGearmod,
	ImportBondage,
	ExportBoundGearmod,
	PrepModels,
	IsolateBondage,
	BatchRenameBondage,
	BlendSkinGroupZero,
	AutoPortCtB,
	TransferHandFeet
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
