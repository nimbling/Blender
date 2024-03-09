bl_info = {
    "name": "Mode Color Bar",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Adds a colored bar to the 3D Viewport according to mode",
    "author": "Herman van Boeijen, nimbling.com",
    "version": (0, 5),
    "blender": (3, 0, 0),
    "location": "Preferences > Add-ons > Mode Color Preferences",
    "category": "Interface",
}

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from typing import Dict

# Global variable to store the draw handler reference
draw_handler = {}

# Actual table of all the colors used:
mode_color_map: Dict[str, tuple[float, float, float, float]] = {
    'OBJECT': (0.5, 0.25, 0, 0.5), # Brown
    'EDIT_MESH': (0.0, 0.2, 0, 0.5), # Dark Green
    'VERT': (0, 0.5, 0, 0.5), # Green
    'EDGE': (0, 0.0, 0.5, 0.5), # Blue
    'FACE': (0.5, 0, 0.5, 0.5), # Purple
    'POSE': (0.5, 0, 0.7, 0.5), # Blueish Purple
    'SCULPT': (0.5, 0, 0.5, 0.5), # Purple
    'PAINT_VERTEX': (0.5, 0, 0.5, 0.5), # Magenta
    'PAINT_WEIGHT': (0, 0.5, 0.5, 0.5), # Cyan
    'PAINT_TEXTURE': (0.3, 0.3, 0, 0.5), # Olive
    'PARTICLE': (0.5, 0.2, 0.3, 0.5), # Plum
    'EDIT_CURVE': (0.4, 0.4, 0.1, 0.5), # Brown
    'EDIT_SURFACE': (0.3, 0.3, 0.3, 0.5), # Dark Grey
    'EDIT_TEXT': (0.5, 0.2, 0, 0.5), # Rust
    'EDIT_ARMATURE': (0, 0.3, 0, 0.5), # Dark Green
    'EDIT_GPENCIL': (0, 0, 0.5, 0.5), # Blue
    'SCULPT_GPENCIL': (0.5, 0.4, 0.3, 0.5), # Mauve
    'WEIGHT_GPENCIL': (0.3, 0.15, 0, 0.5), # Brown
    'PAINT_GPENCIL': (0.35, 0.35, 0.35, 0.5), # Grey
}

# Function to draw the actual rectangle:
def draw_callback_px():
    width = bpy.context.area.width
    height = 54
    coords = [(0, bpy.context.area.height-54), (width, bpy.context.area.height-54), 
              (width, bpy.context.area.height - height-54), (0, bpy.context.area.height - height-54)]
    indices = [(0, 1, 2), (2, 3, 0)]

    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": coords}, indices=indices)

    if bpy.context.mode == 'EDIT_MESH':
        if bpy.context.tool_settings.mesh_select_mode[0]:
            color = mode_color_map.get('VERT')
        elif bpy.context.tool_settings.mesh_select_mode[1]:
            color = mode_color_map.get('EDGE')
        elif bpy.context.tool_settings.mesh_select_mode[2]:
            color = mode_color_map.get('FACE')
    else:
        color = mode_color_map.get(bpy.context.mode)

    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

# Ui to configure the colors in the Add-On panel:
class ModeColorPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    color_object: bpy.props.FloatVectorProperty(
        name="Object Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('OBJECT'),
        update=lambda s, c: update_mode_color(s, c, 'OBJECT'),
        description="Color for Object Mode"
    )

    color_edit_mesh: bpy.props.FloatVectorProperty(
        name="Edit Mesh Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('EDIT_MESH'),
        update=lambda s, c: update_mode_color(s, c, 'EDIT_MESH'),
        description="Color for Edit Mesh Mode"
    )

    color_edit_mesh_vertex: bpy.props.FloatVectorProperty(
        name="Edit Vertex Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('VERT'),
        update=lambda s, c: update_mode_color(s, c, 'VERT'),
        description="Color for Edit Vertex Mode"
    )

    color_edit_mesh_edge: bpy.props.FloatVectorProperty(
        name="Edit Edge Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('EDGE'),
        update=lambda s, c: update_mode_color(s, c, 'EDGE'),
        description="Color for Edit Edge Mode"
    )
    color_edit_mesh_face: bpy.props.FloatVectorProperty(
        name="Edit Face Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('FACE'),
        update=lambda s, c: update_mode_color(s, c, 'FACE'),
        description="Color for Edit Face Mode"
    )

    color_pose: bpy.props.FloatVectorProperty(
        name="Pose Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('POSE'),
        update=lambda s, c: update_mode_color(s, c, 'POSE'),
        description="Color for Pose Mode"
    )

    color_sculpt: bpy.props.FloatVectorProperty(
        name="Sculpt Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('SCULPT'),
        update=lambda s, c: update_mode_color(s, c, 'SCULPT'),
        description="Color for Sculpt Mode"
    )

    color_vertex_paint: bpy.props.FloatVectorProperty(
        name="Vertex Paint Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('PAINT_VERTEX'),
        update=lambda s, c: update_mode_color(s, c, 'PAINT_VERTEX'),
        description="Color for Vertex Paint Mode"
    )
    
    color_weight_paint: bpy.props.FloatVectorProperty(
        name="Weight Paint Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('PAINT_WEIGHT'),
        update=lambda s, c: update_mode_color(s, c, 'PAINT_WEIGHT'),
        description="Color for Weight Paint Mode"
    )

    color_texture_paint: bpy.props.FloatVectorProperty(
name="Texture Paint Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('PAINT_TEXTURE'),
        update=lambda s, c: update_mode_color(s, c, 'PAINT_TEXTURE'),
        description="Color for Texture Paint Mode"
    )

    color_particle_edit: bpy.props.FloatVectorProperty(
        name="Particle Edit Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('PARTICLE'),
        update=lambda s, c: update_mode_color(s, c, 'PARTICLE'),
        description="Color for Particle Edit Mode"
    )

    color_edit_curve: bpy.props.FloatVectorProperty(
        name="Edit Curve Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('EDIT_CURVE'),
        update=lambda s, c: update_mode_color(s, c, 'EDIT_CURVE'),
        description="Color for Edit Curve Mode"
    )

    color_edit_surface: bpy.props.FloatVectorProperty(
        name="Edit Surface Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('EDIT_SURFACE'),
        update=lambda s, c: update_mode_color(s, c, 'EDIT_SURFACE'),
        description="Color for Edit Surface Mode"
    )

    color_edit_text: bpy.props.FloatVectorProperty(
        name="Edit Text Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('EDIT_TEXT'),
        update=lambda s, c: update_mode_color(s, c, 'EDIT_TEXT'),
        description="Color for Edit Text Mode"
    )

    color_edit_armature: bpy.props.FloatVectorProperty(
        name="Edit Armature Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('EDIT_ARMATURE'),
        update=lambda s, c: update_mode_color(s, c, 'EDIT_ARMATURE'),
        description="Color for Edit Armature Mode"
    )

    color_gpencil_edit: bpy.props.FloatVectorProperty(
        name="Grease Pencil Edit Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('EDIT_GPENCIL'),
        update=lambda s, c: update_mode_color(s, c, 'EDIT_GPENCIL'),
        description="Color for Grease Pencil Edit Mode"
    )

    color_gpencil_sculpt: bpy.props.FloatVectorProperty(
        name="Grease Pencil Sculpt Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('SCULPT_GPENCIL'),
        update=lambda s, c: update_mode_color(s, c, 'SCULPT_GPENCIL'),
        description="Color for Grease Pencil Sculpt Mode"
    )

    color_gpencil_weight: bpy.props.FloatVectorProperty(
        name="Grease Pencil Weight Paint Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('WEIGHT_GPENCIL'),
        update=lambda s, c: update_mode_color(s, c, 'WEIGHT_GPENCIL'),
        description="Color for Grease Pencil Weight Paint Mode"
    )

    color_gpencil_paint: bpy.props.FloatVectorProperty(
        name="Grease Pencil Paint Mode Color",
        subtype='COLOR_GAMMA',
        size=4,
        min=0.0, max=1.0,
        default=mode_color_map.get('PAINT_GPENCIL'),
        update=lambda s, c: update_mode_color(s, c, 'PAINT_GPENCIL'),
        description="Color for Grease Pencil Paint Mode"
    )
    def draw(self, context):
        layout = self.layout
        layout.label(text="Custom Mode Colors:")

        row = layout.row()
        row.prop(self, "color_object")
        row = layout.row()
        row.prop(self, "color_edit_mesh")
        row = layout.row()
        row.prop(self, "color_edit_mesh_vertex")
        row = layout.row()
        row.prop(self, "color_edit_mesh_edge")
        row = layout.row()
        row.prop(self, "color_edit_mesh_face")
        row = layout.row()
        row.prop(self, "color_pose")
        row = layout.row()
        row.prop(self, "color_sculpt")
        row = layout.row()
        row.prop(self, "color_vertex_paint")
        row = layout.row()
        row.prop(self, "color_weight_paint")
        row = layout.row()
        row.prop(self, "color_texture_paint")
        row = layout.row()
        row.prop(self, "color_particle_edit")
        row = layout.row()
        row.prop(self, "color_edit_curve")
        row = layout.row()
        row.prop(self, "color_edit_surface")
        row = layout.row()
        row.prop(self, "color_edit_text")
        row = layout.row()
        row.prop(self, "color_edit_armature")
        row = layout.row()
        row.prop(self, "color_gpencil_edit")
        row = layout.row()
        row.prop(self, "color_gpencil_sculpt")
        row = layout.row()
        row.prop(self, "color_gpencil_weight")
        row = layout.row()
        row.prop(self, "color_gpencil_paint")


def update_mode_color(self, context, mode):
    mode_color_map[mode] = getattr(self, f"color_{mode.lower()}")

def register():
    global draw_handler
    draw_handler['handle'] = bpy.types.SpaceView3D.draw_handler_add(
                                 draw_callback_px, (), 'WINDOW', 'POST_PIXEL')
    bpy.utils.register_class(ModeColorPreferences)

def unregister():
    global draw_handler
    if draw_handler.get('handle'):
        bpy.types.SpaceView3D.draw_handler_remove(draw_handler['handle'], 'WINDOW')
        draw_handler['handle'] = None
    bpy.utils.unregister_class(ModeColorPreferences)

if __name__ == "__main__":
    register()