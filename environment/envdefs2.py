###############################################################################
## states set

# min and max for dimention
minX = 1
maxX = minX

minY = 1
maxY = maxX

# grid size variation
x = [10, 15, 20]
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
aP = [0.05, 0.05, 0.05]
aN = [0.05, 0.05, 0.05]

###############################################################################
# reward values
rmin  = -100
rmax  = 100
rstep = -1

###############################################################################
episodes = 10
trials   = 1
port = 5002

###############################################################################
