import bpy

# المدى الذي تريد الحركة به (20 ملي = 0.02 متر)
offset = 0.02

# العنصر المحدد حاليًا
selected_obj = bpy.context.active_object

if selected_obj:
    # استخراج الاسم الأساسي قبل النقطة الأولى (مثال: a.001 -> a)
    base_name = selected_obj.name.split('.')[0]

    # جلب كل العناصر التي تبدأ بنفس الاسم الأساسي
    objects = [obj for obj in bpy.context.scene.objects if obj.name.startswith(base_name + ".")]

    # ترتيب العناصر حسب الاسم
    objects.sort(key=lambda x: x.name)

    # تحريك كل عنصر على محور X بالاتجاه المعاكس
    for index, obj in enumerate(objects):
        obj.location.x -= offset * (index + 1)

    print(f"{len(objects)} عناصر تم تحريكها للخلف.")
else:
    print("لم يتم تحديد أي عنصر.")
