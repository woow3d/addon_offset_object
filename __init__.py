bl_info = {
    "name": "Offset Object",
    "author": "Jackal",
    "version": [1, 1, 0],
    "blender": [4, 0, 0],
    "category": "Mesh",
    "description": {
        "en": "Offset objects along an axis with mm precision, by name or selection order.",
        "ar": "يزاح المجسمات على محور معين بالملليمتر حسب الاسم أو ترتيب التحديد."
    },
    "license": "GPL-3.0",
    "online_access": False
}
import bpy

# --------------------------------------------------
# Utils
# --------------------------------------------------
def get_objects(context, method='NAME'):
    if method == 'NAME':
        active = context.active_object
        if not active:
            return []
        base_name = active.name.split('.')[0]
        objs = [obj for obj in context.scene.objects
                if obj.name == base_name or obj.name.startswith(base_name + ".")]
        objs.sort(key=lambda o: o.name)
        return objs
    elif method == 'SELECTION':
        # نحتفظ فقط بالمجسمات المحددة
        return [obj for obj in context.selected_objects if obj.type == 'MESH']



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
        default=100,
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
    order_type: bpy.props.EnumProperty(
        name="Offset Method",
        description="Choose how to determine the order of objects",
        items=[
            ('NAME', "By Name", "Offset objects based on base name"),
            ('SELECTION', "By Selection", "Offset objects based on selection order"),
        ],
        default='NAME'
    )

    def execute(self, context):
            base_offset = self.offset_mm / 1000.0
            sign = 1 if self.direction == 'PLUS' else -1

            # نختار طريقة الترتيب حسب الخيار
            objects = get_objects(context, method=self.order_type)

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
        self.layout.separator()
        self.layout.operator(
            "object.offset_object"
        )


# --------------------------------------------------
# Register
# --------------------------------------------------
def register():
    bpy.utils.register_class(OBJECT_OT_offset_object)
    bpy.types.VIEW3D_MT_transform_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_transform_object.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_offset_object)





if __name__ == "__main__":
    register()
