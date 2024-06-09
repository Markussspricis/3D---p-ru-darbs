#Grída--------------------------------------------------------------


# Ielādē textūru
floor_texture = viz.addTexture('https://previews.123rf.com/images/ratsadapong/ratsadapong1506/ratsadapong150600084/41746076-old-dirty-cement-floor-use-as-a-background.jpg')

# Uztaisa grīdu
floor = vizshape.addPlane(size=(30, 30), axis=vizshape.AXIS_Y, cullFace=False)
floor.setPosition(0, 0, 0)
floor.texture(floor_texture)  


# Apgaismojums
point_lights = []
light_positions = [(-10, 5, -10), (-10, 5, 10), (10, 5, -10), (10, 5, 10)]
for pos in light_positions:
    point_light = viz.addPointLight()
    point_light.setPosition(pos[0], pos[1], pos[2])
    point_light.intensity(0.6)
    point_lights.append(point_light)

#---------------------------------------------------------------------------

# Kustība un limits līdz grīdas malām------------------------------------------------------------------------------------------

# Grīdas izmērs
floor_size = 30

# Tinker objekts
tinkercad_model = vizfx.addChild(r'C:\Users\marku\Downloads\Tremendous Crift\tinker.obj')
tinkercad_model.setScale(0.025, 0.025, 0.025)
tinkercad_model.setEuler(90, 90, 0)
tinkercad_model.color(viz.GREEN)

# Kustības parametri
MOVE_SPEED = 2.0
CAMERA_DISTANCE = 5.0
CAMERA_HEIGHT = 2.0

# Taustiņu stāvokļa izsekošana
keys = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

# Apakšējā taustiņa darbība
def onKeyDown(key):
    if key == viz.KEY_UP:
        keys['up'] = True
    elif key == viz.KEY_DOWN:
        keys['down'] = True
    elif key == viz.KEY_LEFT:
        keys['left'] = True
    elif key == viz.KEY_RIGHT:
        keys['right'] = True

# Augšējā taustiņa darbība
def onKeyUp(key):
    if key == viz.KEY_UP:
        keys['up'] = False
    elif key == viz.KEY_DOWN:
        keys['down'] = False
    elif key == viz.KEY_LEFT:
        keys['left'] = False
    elif key == viz.KEY_RIGHT:
        keys['right'] = False

# Objekta pozīcijas atjaunināšana
def updateObject():
    global tinkercad_model
    euler = tinkercad_model.getEuler()
    pos = tinkercad_model.getPosition()

    # Kustības virziena aprēķināšana
    move_direction = [0, 0]
    if keys['up']:
        move_direction[1] = 1
    elif keys['down']:
        move_direction[1] = -1
    if keys['left']:
        move_direction[0] = -1
    elif keys['right']:
        move_direction[0] = 1

    # Jaunās pozīcijas aprēķināšana
    new_x = pos[0] + move_direction[0] * MOVE_SPEED * viz.elapsed()
    new_z = pos[2] + move_direction[1] * MOVE_SPEED * viz.elapsed()

    # Ierobežo kustību līdz grīdas malām
    half_size_x = floor_size / 2 - 0.5
    half_size_z = floor_size / 2 - 0.5
    new_x = max(-half_size_x, min(half_size_x, new_x))
    new_z = max(-half_size_z, min(half_size_z, new_z))

    # Iestata jauno pozīciju
    tinkercad_model.setPosition([new_x, pos[1], new_z])

    # Atjauno kameras pozīciju
    updateCamera([new_x, pos[1], new_z], euler[0])

# Kamera seko objektam
def updateCamera(pos, angle):
    # Kameras pozīcijas aprēķināšana aiz objekta
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

#-------------------------------------------------------------------------------------------------------