###############################################################################
## states set

# min and max for dimention
minX = 0
maxX = minX

minY = 0
maxY = maxX

# grid size variation
x = [9, 9, 9]
y = x.copy()

# initial state
initX = minX
initY = minY
initS = [(initX, initY)]

## obstacles

# hole places
holes = []
#holes = [(i, i) for i in range(minX+1, maxX)]

# walls
wd = [0.25, 0.25, 0.25] # walls density
walls = []

###############################################################################
# actions set
actions = ['up','down','left','right']

###############################################################################
# transition probabilities
oposite = 0
orthopos = 0
orthoneg = 0

aO = [0, 0, 0]
aP = [.25, 0.125, 0.05]
aN = [.25, 0.125, 0.05]

###############################################################################
# reward values
rmin  = -100
rmax  = 100
rstep = -1

###############################################################################
episodes = 1000
trials   = 30
port = 5003

###############################################################################
