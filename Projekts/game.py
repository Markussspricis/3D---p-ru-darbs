import viz
import vizshape
import vizfx
import math
import random

viz.go()

viz.clearcolor(viz.SKYBLUE)

# Grīda--------------------------------------------------------------------------------------------------------------------------------

# Ielādē textūru
floor_texture = viz.addTexture('https://t3.ftcdn.net/jpg/05/66/99/80/360_F_566998073_5f6ZEkEeJLj2DaVhAOSq0N5TK2apcHWb.jpg')

# Uztaisa grīdu
floor = vizshape.addPlane(size=(80, 80), axis=vizshape.AXIS_Y, cullFace=False)
floor.setPosition(0, 0, 0)
floor.texture(floor_texture)  
floor_size = 30

# Apgaismojums
point_lights = []
light_positions = [(-10, 5, -10), (-10, 5, 10), (10, 5, -10), (10, 5, 10)]
for pos in light_positions:
    point_light = viz.addPointLight()
    point_light.setPosition(pos[0], pos[1], pos[2])
    point_light.intensity(0.6)
    point_lights.append(point_light)

#----------------------------------------------------------------------------------------------------------------------------------------------

# Sienas-----------------------------------------------------------------------------------------------------------------------------------------------------

# Load the textures
stripe_textures = [
    viz.addTexture('https://t4.ftcdn.net/jpg/05/57/93/59/360_F_557935994_qpvh8RhzkbAH8xCRsf81XaBX7zZS0GOx.jpg'),
    viz.addTexture('https://img.freepik.com/premium-photo/red-barn-sits-farm-with-dirt-road-background_14117-11510.jpg'),
    viz.addTexture('https://www.shutterstock.com/shutterstock/videos/17312977/thumb/11.jpg?ip=x480'),
    viz.addTexture('https://img.freepik.com/free-photo/farmland_1112-1235.jpg'),
]

# Create walls
wall_sizes = [(0.2, 10, 30), (0.2, 10, 30), (30, 10, 0.2), (30, 10, 0.2)]  # Sizes of the walls
wall_positions = [(-15, 5, 0), (15, 5, 0), (0, 5, 15), (0, 5, -15)]  # Positions of the walls

for size, pos, texture in zip(wall_sizes, wall_positions, stripe_textures):
    wall = vizshape.addBox(size=size)
    wall.setPosition(*pos)
    wall.texture(texture)  
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Mower model--------------------------------------------------------------------------------------------------------------------------------

tinkercad_model = vizfx.addChild(r'C:\Users\marku\Downloads\Copy of Copy of Massey Ferguson MF 8 Riding Lawn Mower\tinker.obj')
tinkercad_model.setScale(0.025, 0.025, 0.025)
tinkercad_model.setEuler(90, 90, 0)

# Initial color
tinkercad_color = viz.GREEN
tinkercad_model.color(tinkercad_color)

#--------------------------------------------------------------------------------------------------------------------------------------------------

# Grass model random---------------------------------------------------------------------------------------------------------------------------------

# Function to create random positions
def random_position(floor_size, num_positions):
    positions = []
    for _ in range(num_positions):
        x = random.uniform(-floor_size / 2, floor_size / 2)
        z = random.uniform(-floor_size / 2, floor_size / 2)
        positions.append((x, z))
    return positions

# Adding grass models at random positions
num_grass_models = 50  # Adjust number of grass models as needed
grass_model_path = r'C:\Users\marku\Downloads\Copy of Grass\tinker.obj'
grass_model_scale = 0.1

random_positions = random_position(floor_size, num_grass_models)

for pos in random_positions:
    grass_model = vizfx.addChild(grass_model_path)
    grass_model.setScale(grass_model_scale, grass_model_scale, grass_model_scale)
    grass_model.setPosition(pos[0], 0, pos[1])
    grass_model.setEuler(90, 90, 0)
    grass_model.color(viz.GREEN)
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------

# Kustība un krāsu maiņa--------------------------------------------------------------------------------------------------------------------------------------------

MOVE_SPEED = 2.0
CAMERA_DISTANCE = 5.0
CAMERA_HEIGHT = 2.0

keys = {
    'up': False,
    'down': False,
    'left': False,
    'right': False,
    'color': False,  # Key to toggle color change
}

def onKeyDown(key):
    global keys
    if key == viz.KEY_UP:
        keys['up'] = True
    elif key == viz.KEY_DOWN:
        keys['down'] = True
    elif key == viz.KEY_LEFT:
        keys['left'] = True
    elif key == viz.KEY_RIGHT:
        keys['right'] = True
    elif viz.key.isDown(32):  # Check if space key is pressed (ASCII value 32)
        keys['color'] = True
    print("Key pressed:", key)

def onKeyUp(key):
    global keys
    if key == viz.KEY_UP:
        keys['up'] = False
    elif key == viz.KEY_DOWN:
        keys['down'] = False
    elif key == viz.KEY_LEFT:
        keys['left'] = False
    elif key == viz.KEY_RIGHT:
        keys['right'] = False
    elif not viz.key.isDown(32):  # Check if space key is released (ASCII value 32)
        keys['color'] = False
    print("Key released:", key)

available_colors = [viz.RED, viz.BLUE, viz.GREEN, viz.YELLOW, viz.ORANGE]

def updateObject():
    global keys, tinkercad_model, tinkercad_color, color_toggled, available_colors
    euler = tinkercad_model.getEuler()
    pos = tinkercad_model.getPosition()
    move_direction = [0, 0]
    if keys['up']:
        move_direction[1] = 1
    elif keys['down']:
        move_direction[1] = -1
    if keys['left']:
        move_direction[0] = -1
    elif keys['right']:
        move_direction[0] = 1
    new_x = pos[0] + move_direction[0] * MOVE_SPEED * viz.elapsed()
    new_z = pos[2] + move_direction[1] * MOVE_SPEED * viz.elapsed()
    half_size_x = floor_size / 2 - 0.5
    half_size_z = floor_size / 2 - 0.5
    new_x = max(-half_size_x, min(half_size_x, new_x))
    new_z = max(-half_size_z, min(half_size_z, new_z))
    tinkercad_model.setPosition([new_x, pos[1], new_z])
    updateCamera([new_x, pos[1], new_z], euler[0])
    
    # Toggle color change only when spacebar is pressed and color hasn't already been toggled
    if keys['color'] and not color_toggled:
        print("Color change triggered!")
        # Cycle through the available colors
        current_index = available_colors.index(tinkercad_color)
        next_index = (current_index + 1) % len(available_colors)
        tinkercad_color = available_colors[next_index]
        tinkercad_model.color(tinkercad_color)
        color_toggled = True

    # Reset color_toggled when spacebar is released
    if not keys['color']:
        color_toggled = False

def updateCamera(pos, angle):
    camera_pos = [
        pos[0] - CAMERA_DISTANCE * math.sin(math.radians(angle)),
        pos[1] + CAMERA_HEIGHT,
        pos[2] - CAMERA_DISTANCE * math.cos(math.radians(angle))
    ]
    viz.MainView.setPosition(camera_pos)
    viz.MainView.lookAt(pos)

viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
viz.callback(viz.KEYUP_EVENT, onKeyUp)

vizact.ontimer(0, updateObject)

#---------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    viz.go()