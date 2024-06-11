#Sienas--------------------------------------------------------------------------


    
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
#-------------------------------------------------------------------------------