import bpy

# main panel class
class CK_HelperToolsPanel(bpy.types.Panel):
	bl_idname = "object.ck_helper_tools_panel"
	bl_label = "CK Helper Tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = 'UI'
	bl_category = "CK Helpers"

	def draw(self, context):
		layout = self.layout
		scene = context.scene
		
		row = layout.row()
		row.operator(
			"wm.url_open",
			text="Guide for Further Details",
			icon="HELP"
		).url = "https://docs.google.com/document/d/1dAYyE5sBWvKKXOktDmMmRR4xP8z7yPLQf3uj3ZxxkFs/edit?usp=sharing"
		
		# Import components
		row = layout.row(align=True)
		row.scale_y = 0.5
		layout.label(text = "Import Models:")
		row = layout.row(align=True)
		row.scale_y = 1.5
		row.operator("object.import_gearmod", text = "Gear Mod", icon= "IMPORT")
		row.operator("object.import_bondage",  text = "Bondage", icon= "IMPORT")
	
		# Prep options
		row = layout.row()
		row.scale_y = 1.0
		layout.label(text = "Auto-Port Preperations:")
	
		row = layout.row()
		row.scale_y = 1.0
		row.operator("object.prep_models", text="Prepare Models", icon="BRUSH_DATA")
		
		row = layout.row()
		row.scale_y = 1.0
		layout.prop(scene, "autoport_mod_selector", text="") #references to functions below class
		
		row = layout.row()
		row.scale_y = 1.0
		row.operator("object.isolate_bondage", text="Isolate Bondage Parts", icon="VIEWZOOM")
		
		# No reason to warn if mentioned in documentation
		#row = layout.row()
		#row.scale_y = 1.0
		#layout.label(text = "Only use IF > 1 [Part #.]'s:")
		row = layout.row()
		row.scale_y = 1.0
		row.operator("object.batch_rename_bondage", text="Rename Bondage Parts", icon="FONT_DATA")
				
		row = layout.row()
		row.scale_y = 1.0
		row.operator("object.blend_skin_groupzero", text="Merge Skin Group 0", icon="INVERSESQUARECURVE")
		
		row = layout.row()
		row.scale_y = 1.5
		row.operator("object.autoport_ctb", text="Auto-Port to Bondage", icon="MOD_CLOTH")
		
		# Touch Up options
		row = layout.row()
		row.scale_y = 0.5
		layout.label(text = "Touch-Up & Export:")
		
		row = layout.row(align=True)
		row.scale_y = 1.0
		row.prop(scene, "handfeet_selector", text="")
		row.operator("object.transfer_handfeet", text="Add Hands", icon="VIEW_PAN")# <-- UI Space issue
		
		# Select & Export buttons (fix when you know how)
		row = layout.row()
		row.scale_y = 1.0
		row.operator("object.export_bound_gearmod", text = "Select All For Export", icon= "CHECKBOX_HLT")
		row = layout.row()
		row.scale_y = 1.0
		row.operator("export_scene.fbx", text = "Export FBX", icon= "EXPORT").use_selection = True
		
# helper functions and enums for dropdown
# Define the list of items to be used in the dropdown menu
dropdown_items = [
	("MOD_1", "Armbinder Restraint", "", 1),
	("MOD_2", "Box Tie Bondage", "", 2),
	("MOD_3", "Rope Harness + Armbinder", "", 3),
	("MOD_4", "(Gen3) Rope Leg Bondage", "", 4),
	("MOD_5", "(Bibo+) Rope Leg Bondage", "", 5),
	("MOD_6", "(Gen3) Frogtie Bondage", "", 6),
	("MOD_7", "(Bibo+) Frogtie Bondage", "", 7),
	("MOD_8", "Tape Chest Wrap", "", 8),
	("MOD_9", "(Gen3) Tape Leg Wrap", "", 9),
	("MOD_10", "(Bibo+) Tape Leg Wrap", "", 10),
	("MOD_11", "Metal Stock", "", 11),
	("MOD_12", "(Gen3) Spreader Bar", "", 12),
	("MOD_13", "(Bibo+) Spreader Bar", "", 13)
]

handfeet_list = [
	("HANDFEET1", "Gen3", "", 1),
	("HANDFEET2", "Bibo+", "", 2),
	("HANDFEET3", "Vanilla", "", 3)
]

# Register the /autoport_mod_selector/ dropdown property
bpy.types.Scene.autoport_mod_selector = bpy.props.EnumProperty(
	items=dropdown_items,
	description="Choose an option",
	default="MOD_1"
)

# Register 2nd dropdown for hand transfer
bpy.types.Scene.handfeet_selector = bpy.props.EnumProperty(
	items=handfeet_list,
	description="Choose an option",
	default="HANDFEET1"
)
		
classes = [
    CK_HelperToolsPanel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
