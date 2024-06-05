import viz
import vizshape
import vizcam
import vizfx
import math
import vizact
import time
import random

viz.go()

viz.clearcolor(viz.SKYBLUE)

floor = vizshape.addPlane(size=(20, 20), axis=vizshape.AXIS_Y, cullFace=False)
floor.setPosition(0, 0, 0)
floor.color(viz.GRAY)

score = 0
score_text = viz.addText('Score: 0', parent=viz.SCREEN, pos=(0.1, 0.9, 0))
score_text.fontSize(32)
score_text.color(viz.WHITE)

tinkercad_model = vizfx.addChild(r'C:\Users\marku\Downloads\Tremendous Crift\tinker.obj')
tinkercad_model.setPosition(0, 0, 0)
tinkercad_model.setScale(0.025, 0.025, 0.025)
tinkercad_model.setEuler(0, 90, 0)
tinkercad_model.color(viz.GREEN)

# Balls setup
balls = []

positive_sound = viz.addAudio(r'C:\Users\marku\Downloads\ball.mp3')
negative_sound = viz.addAudio(r'C:\Users\marku\Downloads\cube.mp3')

def createBall(radius, position, color, points):
    ball = vizshape.addSphere(radius=radius)
    ball.setPosition(position)
    ball.color(color)
    ball.points = points
    balls.append(ball)

createBall(0.5, (5, 0.5, 5), viz.RED, 3)
createBall(0.7, (-5, 0.7, 3), viz.GREEN, 5)
createBall(0.3, (3, 0.3, -7), viz.BLUE, 1)
createBall(0.4, (-3, 0.4, -4), viz.YELLOW, 2)
createBall(0.6, (7, 0.6, -5), viz.PURPLE, 4)

time_limit = 30
start_time = time.time()
time_text = viz.addText(f'Time: {time_limit}', parent=viz.SCREEN, pos=(0.9, 0.9, 0))
time_text.fontSize(32)
time_text.color(viz.WHITE)

timer_running = True
game_over = False
white_cube_count = 0
max_white_cubes = 3
white_cube = None

def updateTime():
    global time_limit, timer_running, game_over
    if timer_running and time_limit > 0:
        time_limit -= 1
        time_text.message(f'Time: {time_limit}')
    if time_limit == 0 and not game_over:
        gameOver()

timer_action = vizact.ontimer(1, updateTime)

def stopTimer():
    global timer_running
    timer_running = False

def updateScore(points):
    global score
    score += points
    score_text.message(f'Score: {score}')

def displayWinningMessage():
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    message = f'You win\nScore: {score}\nTime: {seconds} sec'
    win_text = viz.addText(message, parent=viz.SCREEN, pos=(0.5, 0.5, 0))
    win_text.fontSize(48)
    win_text.setBackdrop(viz.BACKDROP_OUTLINE)

def displayGameOverMessage():
    global score
    message = f'Game over\nScore: {score}'
    game_over_text = viz.addText(message, parent=viz.SCREEN, pos=(0.5, 0.4, 0))
    game_over_text.fontSize(48)
    game_over_text.setBackdrop(viz.BACKDROP_OUTLINE)
    time_up_message = viz.addText("You ran out of time", parent=viz.SCREEN, pos=(0.5, 0.3, 0))
    time_up_message.fontSize(36)
    time_up_message.color(viz.RED)

def checkCollisions():
    global balls, game_over
    if game_over:
        return
    model_position = tinkercad_model.getPosition()
    for ball in balls[:]:
        ball_position = ball.getPosition()
        distance = math.sqrt((model_position[0] - ball_position[0])**2 +
                             (model_position[1] - ball_position[1])**2 +
                             (model_position[2] - ball_position[2])**2)
        if distance < 1:
            updateScore(ball.points)
            positive_sound.play()
            ball.remove()
            balls.remove(ball)
            if not balls:
                stopTimer()
                displayWinningMessage()
                game_over = True

def handleWhiteCube():
    global score, white_cube, white_cube_count, game_over
    if game_over or white_cube is None:
        return
    model_position = tinkercad_model.getPosition()
    cube_position = white_cube.getPosition()
    distance = math.sqrt((model_position[0] - cube_position[0])**2 +
                         (model_position[1] - cube_position[1])**2 +
                         (model_position[2] - cube_position[2])**2)
    if distance < 1:
        score -= 3
        score_text.message(f'Score: {score}')
        negative_sound.play()
        white_cube.remove()
        white_cube = None
        white_cube_count -= 1

def onUpdate():
	checkCollisions()
	handleWhiteCube()

vizact.ontimer(0, onUpdate)

def gameOver():
    global game_over
    displayGameOverMessage()
    navigator.remove()
    stopTimer()
    game_over = True

head_light = viz.MainView.getHeadLight()
head_light.intensity(0.8)

dir_light = viz.addDirectionalLight()
dir_light.direction(0, -1, 0)
dir_light.intensity(0.8)

colors_points = {
    viz.BLUE: 1,
    viz.YELLOW: 2,
    viz.RED: 3,
    viz.PURPLE: 4,
    viz.GREEN: 5
}

for i, (color, points) in enumerate(colors_points.items()):
    if color == viz.BLUE:
        text_points = viz.addText(f'{points} point', parent=viz.SCREEN, pos=(0.15, 0.8 - i * 0.06, 0))
    else:
        text_points = viz.addText(f'{points} points', parent=viz.SCREEN, pos=(0.15, 0.8 - i * 0.06, 0))
    text_points.fontSize(24)
    text_points.color(viz.WHITE)
    circle = vizshape.addCircle(radius=0.025, color=color, pos=(0.1, 0.8 - i * 0.06, 0), parent=viz.SCREEN)

def placeWhiteCube():
    global white_cube, white_cube_count
    if white_cube_count >= max_white_cubes:
        return
    x = random.uniform(-9, 9)
    z = random.uniform(-9, 9)
    white_cube = vizshape.addCube(0.5, color=viz.WHITE)
    white_cube.setPosition(x, 0.25, z)
    white_cube_count += 1

def updateWhiteCube():
    if white_cube is None and white_cube_count < max_white_cubes:
        placeWhiteCube()
    if white_cube_count < max_white_cubes:
        vizact.ontimer2(random.uniform(5, 15), 1, updateWhiteCube)

updateWhiteCube()

MOVE_SPEED = 2
ROTATE_SPEED = 60

movement = {
    'forward': False,
    'backward': False,
    'left': False,
    'right': False
}

rotation = {
    'left': False,
    'right': False
}

def moveModel():
    global movement, rotation, game_over

    if game_over:
        return

    elapsed = viz.elapsed()
    pos = tinkercad_model.getPosition()
    euler = tinkercad_model.getEuler()

    move_x = 0
    move_z = 0

    if movement['forward']:
        move_x += MOVE_SPEED * elapsed * math.sin(math.radians(euler[0]))
        move_z += MOVE_SPEED * elapsed * math.cos(math.radians(euler[0]))
    if movement['backward']:
        move_x -= MOVE_SPEED * elapsed * math.sin(math.radians(euler[0]))
        move_z -= MOVE_SPEED * elapsed * math.cos(math.radians(euler[0]))
    if movement['left']:
        move_x -= MOVE_SPEED * elapsed * math.cos(math.radians(euler[0]))
        move_z += MOVE_SPEED * elapsed * math.sin(math.radians(euler[0]))
    if movement['right']:
        move_x += MOVE_SPEED * elapsed * math.cos(math.radians(euler[0]))
        move_z -= MOVE_SPEED * elapsed * math.sin(math.radians(euler[0]))

    new_pos = (pos[0] + move_x, pos[1], pos[2] + move_z)
    tinkercad_model.setPosition(new_pos)

    if rotation['left']:
        tinkercad_model.setEuler(euler[0] + ROTATE_SPEED * elapsed, euler[1], euler[2])
    if rotation['right']:
        tinkercad_model.setEuler(euler[0] - ROTATE_SPEED * elapsed, euler[1], euler[2])

def onKeyDown(key):
    if key == 'w':
        movement['forward'] = True
    elif key == 's':
        movement['backward'] = True
    elif key == 'a':
        movement['left'] = True
    elif key == 'd':
        movement['right'] = True
    elif key == viz.KEY_LEFT:
        rotation['left'] = True
    elif key == viz.KEY_RIGHT:
        rotation['right'] = True

def onKeyUp(key):
    if key == 'w':
        movement['forward'] = False
    elif key == 's':
        movement['backward'] = False
    elif key == 'a':
        movement['left'] = False
    elif key == 'd':
        movement['right'] = False
    elif key == viz.KEY_LEFT:
        rotation['left'] = False
    elif key == viz.KEY_RIGHT:
        rotation['right'] = False

viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
viz.callback(viz.KEYUP_EVENT, onKeyUp)

vizact.ontimer(0, moveModel)

if __name__ == "__main__":
    viz.go()