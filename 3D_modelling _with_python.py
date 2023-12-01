import bpy
import math

# User-defined column parameters
column_radius = 0.1
column_height = 20.0
num_columns_x = 15
num_columns_y = 15

# User-defined slab parameters
slab_thickness = 0.1

# Clear existing mesh objects and materials
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create a group of columns
columns = bpy.data.collections.new('Columns')
bpy.context.scene.collection.children.link(columns)

for i in range(num_columns_x):
    for j in range(num_columns_y):
        # Create a column mesh
        column_mesh = bpy.data.meshes.new(name=f'Column_{i}_{j}')
        column_obj = bpy.data.objects.new(f'Column_{i}_{j}', column_mesh)

        # Link the column object to the scene
        columns.objects.link(column_obj)
        bpy.context.view_layer.objects.active = column_obj  # Make the object active

        # Create column vertices
        column_vertices = []

        for k in range(32):
            angle = (2 * math.pi / 32) * k
            x = i * 2 * column_radius + column_radius * math.cos(angle)
            y = j * 2 * column_radius + column_radius * math.sin(angle)
            column_vertices.extend([(x, y, 0), (x, y, column_height)])

        # Create column faces and edges
        column_faces = [(k, k + 1, k + 3, k + 2) for k in range(0, len(column_vertices) - 2, 2)]
        column_edges = [(k, k + 1) for k in range(0, len(column_vertices), 2)]

        column_mesh.from_pydata(column_vertices, column_edges, column_faces)

        # Set the origin to the bottom of the column
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

        # Optionally, adjust the scale or other properties
        column_obj.scale = (1, 1, 1)  # Adjust the scale as needed

# Update the scene
bpy.context.view_layer.update()

# Calculate the slab position
slab_position = (
    (num_columns_x - 1) * 2 * column_radius / 2,
    (num_columns_y - 1) * 2 * column_radius / 2,
    column_height + slab_thickness / 2
)

# Create a slab above the group of columns
slab_mesh = bpy.data.meshes.new(name='Slab')
slab_obj = bpy.data.objects.new('Slab', slab_mesh)

# Link the slab object to the scene
bpy.context.scene.collection.objects.link(slab_obj)
bpy.context.view_layer.objects.active = slab_obj  # Make the object active

# Create slab vertices
slab_vertices = [
    (-num_columns_x * column_radius, -num_columns_y * column_radius, 0),
    (-num_columns_x * column_radius, num_columns_y * column_radius, 0),
    (num_columns_x * column_radius, num_columns_y * column_radius, 0),
    (num_columns_x * column_radius, -num_columns_y * column_radius, 0)
]

# Extrude to create the slab
slab_vertices.extend([(x, y, -slab_thickness) for x, y, z in slab_vertices])

# Create slab faces and edges
slab_faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
slab_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

slab_mesh.from_pydata(slab_vertices, slab_edges, slab_faces)

# Set the origin to the bottom of the slab
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

# Set the slab position
slab_obj.location = slab_position

# Optionally, adjust the scale or other properties
slab_obj.scale = (1, 1, 1)  # Adjust the scale as needed

# Update the scene
bpy.context.view_layer.update()