import bpy, sys, os

# Parse arguments after --
argv = sys.argv
if '--' in argv:
    argv = argv[argv.index('--') + 1:]
else:
    argv = []

# Parameters (default)
resolution = 512
output_dir = r'C:/Users/Thabang/agent-automation-demo/blender-renders'
product_names = ['Still_500ml', 'Still_750ml', 'Still_1L', 'Sparkling_500ml', 'Sparkling_750ml', 'Sparkling_1L']
colors = {
    'Still_500ml': (200, 230, 255),
    'Still_750ml': (200, 230, 255),
    'Still_1L': (200, 230, 255),
    'Sparkling_500ml': (180, 220, 255),
    'Sparkling_750ml': (180, 220, 255),
    'Sparkling_1L': (180, 220, 255),
}

os.makedirs(output_dir, exist_ok=True)

for i, name in enumerate(product_names):
    # Clear scene
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mat in list(bpy.data.materials):
        bpy.data.materials.remove(mat, do_unlink=True)

    # Create bottle mesh (procedural)
    # Body: cylinder with bevel, neck + cap
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.8, location=(0,0,0))
    bottle = bpy.context.active_object
    bottle.name = name

    # Material
    col = colors[name]
    mat = bpy.data.materials.new(name=f"{name}_mat")
    mat.use_nodes = True
    node_tree = mat.node_tree
    bsdf = node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*col, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.3
    bottle.data.materials.append(mat)

    # Camera
    bpy.ops.object.camera_add(location=(2, -3, 1.5))
    cam = bpy.context.active_object
    cam.name = 'Cam'
    scene = bpy.context.scene
    scene.camera = cam

    # Lighting
    # Key light (Sun)
    bpy.ops.object.light_add(type='SUN')
    key = bpy.context.active_object
    key.name = 'Key'
    key.data.energy = 5
    # Fill light (Area)
    bpy.ops.object.light_add(type='AREA')
    fill = bpy.context.active_object
    fill.name = 'Fill'
    fill.data.energy = 200
    # Rim light (Sun from back)
    bpy.ops.object.light_add(type='SUN')
    rim = bpy.context.active_object
    rim.name = 'Rim'
    rim.data.energy = 3

    # World background white
    world = bpy.data.worlds.get('World')
    if not world:
        world = bpy.data.worlds.new('World')
        bpy.context.scene.world = world
    world.use_nodes = True
    world_node_tree = world.node_tree
    background = world_node_tree.nodes.get('Background')
    if background:
        background.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        background.inputs['Strength'].default_value = 1.0

    # Render settings
    scene.render.engine = 'CYCLES'
    scene.render.resolution_x = resolution
    scene.render.resolution_y = resolution
    scene.render.filepath = os.path.join(output_dir, f'{name}.png')

    # Render
    bpy.ops.render.render(write_still=True)

print(f"Rendered {len(product_names)} bottles")