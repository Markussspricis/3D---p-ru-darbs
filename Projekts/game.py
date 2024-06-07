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