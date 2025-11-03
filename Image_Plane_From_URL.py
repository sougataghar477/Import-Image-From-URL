bl_info = {
    "name": "Import Image From URL",
    "author": "Sougata Ghar, Florian Meyer",
    "version": (1,1),
    "blender": (3, 0, 1),
    "location": "VIEW3D > UI",
    "description": "Import Image from URL",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import",
}

import bpy
import urllib.request
import os
import random
import addon_utils
from pathlib import Path
from os import getcwd

addon_utils.enable("io_import_images_as_planes", default_set=True, persistent=True)


class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Image Images From URL"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Image Images From URL'

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "string_prop_for_referrence")
        row = layout.row()
        row.operator("mesh.ref_operator")

        layout.prop(context.scene, "string_prop_for_plane")
        row2 = layout.row()
        row2.operator("mesh.plane_operator")


class MyOperator(bpy.types.Operator):
    bl_idname = "mesh.ref_operator"
    bl_label = "Import Ref Image"

    def execute(self, context):
        generate_image("object.load_reference_image")
        return {"FINISHED"}


class MyOperator2(bpy.types.Operator):
    bl_idname = "mesh.plane_operator"
    bl_label = "Import Image Plane"

    def execute(self, context):
        generate_image("import_image.to_plane")
        return {"FINISHED"}


def generate_image(image_type):
    parentFolder = Path(getcwd())
    tempDir = Path(bpy.app.tempdir)
    string_input = ''
    urls = []
    if(image_type == "object.load_reference_image"):
        string_input = bpy.context.scene.string_prop_for_referrence.strip()
    else:
        string_input = bpy.context.scene.string_prop_for_plane.strip() 
    string_inputs = string_input.split('https://')
    for s in string_inputs:
        if(s!=''):
            urls.append('https://'+s.strip())
    for url in urls:        
        filename = url.split('/')[-1]
        shortenedName = filename[:5]
        isImageinFormat = True

        if not (
            filename.endswith('.jpg')
            or filename.endswith('.jpeg')
            or filename.endswith('.png')
            or filename.endswith('.webp')
            or filename.endswith('.cms')
            or filename.endswith('.tiff')
            or filename.endswith('.bmp')
            or filename.endswith('.svg')

        ):
            isImageinFormat = False

        if not isImageinFormat:
            if 'jpg' in filename:
                filename = shortenedName + '.jpg'
            elif 'png' in filename:
                filename = shortenedName + '.png'
            elif 'jpeg' in filename:
                filename = shortenedName + '.jpg'
            elif 'webp' in filename:
                filename = shortenedName + '.webp'
            elif 'cms' in filename:
                filename = shortenedName + '.cms'
            elif 'tiff' in filename:
                filename = shortenedName + '.tiff'
            elif 'bmp' in filename:
                filename = shortenedName + '.bmp'
            elif 'svg' in filename:
                filename = shortenedName + '.svg' 
        sub_name = 'images'
        subfolder = tempDir / sub_name
        subfolder.mkdir(exist_ok=True)

        filename_path = subfolder / filename
        urllib.request.urlretrieve(url, filename_path)
        if(image_type=="object.load_reference_image"):
            bpy.ops.object.load_reference_image(filepath=str(filename_path))
        else:
            bpy.ops.import_image.to_plane(files=[{"name":str(filename_path)}], directory=str(parentFolder))
def register():
    bpy.types.Scene.string_prop_for_referrence = bpy.props.StringProperty(name="URL")
    bpy.types.Scene.string_prop_for_plane = bpy.props.StringProperty(name="URL")
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(MyOperator)
    bpy.utils.register_class(MyOperator2)


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(MyOperator)
    del bpy.types.Scene.string_prop_for_referrence
    del bpy.types.Scene.string_prop_for_plane

MyOperator2
if __name__ == "__main__":
    register()
