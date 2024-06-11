def updateObject():
    global keys, tinkercad_model, tinkercad_color, color_toggled, available_colors
    euler = tinkercad_model.getEuler()
    pos = tinkercad_model.getPosition()
    move_direction = [0, 0, 0]
    if keys['up']:
        move_direction[2] = 1
    elif keys['down']:
        move_direction[2] = -1
    if keys['left']:
        move_direction[0] = -1
    elif keys['right']:
        move_direction[0] = 1
    
    new_x = pos[0] + move_direction[0] * MOVE_SPEED * viz.elapsed()
    new_z = pos[2] + move_direction[2] * MOVE_SPEED * viz.elapsed()
    half_size_x = floor_size / 2 - OBJECT_SIZE_X / 2
    half_size_z = floor_size / 2 - OBJECT_SIZE_Z / 2
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
    # Calculate the camera position based on the object's position and orientation
    camera_pos = [
        pos[0] - CAMERA_DISTANCE * math.sin(math.radians(angle)),
        pos[1] + CAMERA_HEIGHT,  # Place the camera a little above the object
        pos[2] - CAMERA_DISTANCE * math.cos(math.radians(angle))
    ]

    # Check if the camera is going through the walls
    half_size = floor_size / 2
    if camera_pos[0] < -half_size:
        camera_pos[0] = -half_size
    elif camera_pos[0] > half_size:
        camera_pos[0] = half_size
    if camera_pos[2] < -half_size:
        camera_pos[2] = -half_size
    elif camera_pos[2] > half_size:
        camera_pos[2] = half_size

    viz.MainView.setPosition(camera_pos)
    viz.MainView.lookAt(pos)
    
viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
viz.callback(viz.KEYUP_EVENT, onKeyUp)

vizact.ontimer(0, updateObject)