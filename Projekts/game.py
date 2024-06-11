#Grída--------------------------------------------------------------


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

#---------------------------------------------------------------------------