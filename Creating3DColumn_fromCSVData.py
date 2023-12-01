import bpy
import csv

# Path to your CSV file
csv_file_path = "C:/Users/hasan/Desktop/Blenderprivat/collar_BLNEOM.csv"

# Read coordinates from the CSV file
coordinates = []
with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        x, y, z = map(float, row)
        coordinates.append((x, y, z))

# Create a new collection
collection = bpy.data.collections.new(name="ColumnCollection")
bpy.context.scene.collection.children.link(collection)

# Create cylinders at specified coordinates and add them to the collection
for i, coord in enumerate(coordinates):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=8, location=coord)
    cylinder = bpy.context.active_object
    collection.objects.link(cylinder)

    # Assign unique names to cylinders
    cylinder.name = f"Column_{i}"

# Set up camera and lights for visualization
bpy.ops.object.camera_add(location=(5, -5, 5), rotation=(1.0472, 0, 0))
bpy.ops.object.light_add(type='SUN', location=(5, -5, 5))
bpy.ops.view3d.camera_to_view_selected()