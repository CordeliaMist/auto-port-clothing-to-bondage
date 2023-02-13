bl_info = {
	"name": "CK Helper Tools",
	"author": "Cordelia Mist",
	"version": (1, 1, 0),
	"blender": (3, 2, 0),
	"location": "View3D",
	"description": "Only Use this tool for CK Tutorial uses, I cannot garentee how it will act outside of them. As in it could possibly start adding modifiers to random objects if used outside of the purpose of the tutorials they are made for.",
	"category": "All"
}

import bpy
from . import ui
from . import operators
	
def register():
	ui.register()
	operators.register()
	
def unregister():
	ui.unregister()
	operators.unregister()

if __name__ == "__main__":
    register()
