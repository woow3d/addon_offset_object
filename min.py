bl_info = {
    "name": "Offset Object",
    "author": "Simple Code",
    "version": (1, 3, 0),
    "blender": (3, 0, 0),
    "location": "Object > Transform > Offset Object",
    "description": "Offset objects by name using redo panel (F9)",
    "category": "Object",
}

import bpy




# --------------------------------------------------
# Utils
# --------------------------------------------------
def get_objects_by_active_name(context):
    active = context.active_object
    if not active:
        return []

    base_name = active.name.split('.')[0]

    objs = [
        obj for obj in context.scene.objects
        if obj.name == base_name or obj.name.startswith(base_name + ".")
    ]

    objs.sort(key=lambda o: o.name)
    return objs


def apply_offset(obj, axis, value):
    if axis == 'X':
        obj.location.x += value
    elif axis == 'Y':
        obj.location.y += value
    elif axis == 'Z':
        obj.location.z += value


# --------------------------------------------------
# Operator
# --------------------------------------------------
class OBJECT_OT_offset_object(bpy.types.Operator):
    bl_idname = "object.offset_object"
    bl_label = "Offset Object"
    bl_description = "Offset objects based on active object name"
    bl_options = {'REGISTER', 'UNDO'}

    offset_mm: bpy.props.FloatProperty(
        name="Offset (mm)",
        default=20.0,
        min=0.0,
        precision=2
    )

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
        ],
        default='X'
    )
    multiplier: bpy.props.IntProperty(
        name="Multiplier",
        description="Multiply offset amount for faster adjustments",
        default=1,
        min=1,
        max=100
    )

    offset_first: bpy.props.BoolProperty(
        name="Offset First Object",
        description="Apply offset to the first object as well",
        default=False
    )

    direction: bpy.props.EnumProperty(
        name="Direction",
        items=[
            ('PLUS', "+", "Positive direction"),
            ('MINUS', "-", "Negative direction"),
        ],
        default='PLUS'
    )

    def execute(self, context):
        base_offset = self.offset_mm / 1000.0  # mm → meters
        sign = 1 if self.direction == 'PLUS' else -1

        objects = get_objects_by_active_name(context)

        for i, obj in enumerate(objects):
            index = i + 1 if self.offset_first else i
            final_offset = sign * base_offset * self.multiplier * index
            apply_offset(obj, self.axis, final_offset)

        return {'FINISHED'}




# --------------------------------------------------
# Menu
# --------------------------------------------------
def menu_func(self, context):
    if context.active_object:
        self.layout.operator(
            "object.offset_object.transform",
            icon=''
        )


# --------------------------------------------------
# Register
# --------------------------------------------------
def register():
    bpy.utils.register_class(OBJECT_OT_offset_object)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_offset_object)



if __name__ == "__main__":
    register()
