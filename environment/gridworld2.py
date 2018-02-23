### Gridworld
exp = 2

if exp == 1:
    from envdefs1 import *
elif exp == 2:
    from envdefs2 import *
elif exp == 3:
    from envdefs3 import *
else:
    from envdefs import *

from random import random

################################################################################
def nextState(state, a):
    terminal = False
    rew  = rstep

    ay = 0
    ax = 0
    a = str(a)

    x, y = state[1:].split("y")
    x = int(x)
    y = int(y)

    r = random()

    if a == 'up':
        if r < orthopos:
            ax = +1
        elif r < orthoneg:
            ax = -1
        elif r < oposite:
            ay = -1
        else:
            ay = +1

    elif a == 'down':
        if r < orthopos:
            ax = +1
        elif r < orthoneg:
            ax = -1
        elif r < oposite:
            ay = +1
        else:
            ay = -1

    elif a == 'left':
        if r < orthopos:
            ay = +1
        elif r < orthoneg:
            ay = -1
        elif r < oposite:
            ax = +1
        else:
            ax = -1

    elif a == 'right':
        if r < orthopos:
            ay = +1
        elif r < orthoneg:
            ay = -1
        elif r < oposite:
            ax = -1
        else:
            ax = +1

    nx = x + ax
    if nx > maxX: nx = maxX
    if nx < minX: nx = minX

    ny = y + ay
    if ny > maxY: ny = maxY
    if ny < minY: ny = minY

    nstate = tuple([nx,ny])
    if nstate not in walls:
        state = nstate

    if state in holes:
        rew = rmin
        terminal = True
    elif state in goalS:
        rew = rmax
        terminal = True

    return nx, ny, rew, terminal


################################################################################
def initState():
  # from random import randint

  # while True:
  #     x = randint(minX, maxX)
  #     y = randint(minX, maxX)

  #     if((x,y) not in holes and (x,y) not in goalS):
  #         break

  # message = 'x' + str(x)+'y' + str(y)

    message = 'x0y0'
    return message


################################################################################
def envConf():
    message = ''

    for action in actions:
        message += action + ' '

    message += str(rmax) + ' ' + str(rmin)

    return message


################################################################################
def printGrid(state, action, nstate):

    times = 30
    print("*" * times)
    print(state, action, nstate)

    for y in range(maxY, minY-1,-1):
        for x in range(minX, maxX+1):
            if (x, y) in holes:
                print('H', end=' ')
            elif (x, y) in walls:
                print('W', end=' ')
            elif (x, y) in goalS:
                print('G', end=' ')
            elif (x, y) in initS:
                print('S', end=' ')
            elif (x, y) == state:
                if action == 'up':
                    print('^', end=' ')
                elif action == 'down':
                    print('v', end=' ')
                elif action == 'left':
                    print('<', end=' ')
                elif action == 'right':
                    print('>', end=' ')
                else:
                    print("E", end=' ')
            elif (x, y) == nstate:
                print('s' , end=' ')
            else:
                print('_', end=' ')

        print()


    print("*" * times)


################################################################################
def printGridConf():

    times = 30
    print("*" * times)

    for y in range(maxY, minY-1,-1):
        for x in range(minX, maxX+1):
            if (x, y) in holes:
                print('H', end=' ')
            elif (x, y) in walls:
                print('W', end=' ')
            elif (x, y) in goalS:
                print('G', end=' ')
            elif (x, y) in initS:
                print('S', end=' ')
            else:
                print('_', end=' ')

        print()


    print("*" * times)


################################################################################
def genGridworld(xsize, ysize, densw):
    from random import randint

    goal = [(xsize, ysize)]

    walls = list()

    if densw < 0: densw = 0
    if densw > 1: densw = 1
    nwalls = int(xsize * ysize * densw)

    while len(walls) < nwalls:
        x = randint(0, xsize)
        y = randint(0, ysize)
        w = (x, y)

        if w not in goal and w not in walls and w not in initS:
            walls.append(w)

    return goal, walls


################################################################################
def sendDimentions(xsize, ysize):
    return str(xsize) + ' ' + str(ysize)


################################################################################
def stationaryEnvironment(socket, xsize, ysize, densw, maxEpisodes):

    print("Gridworld")
    global maxX, maxY
    maxX = minX + xsize
    maxY = minY + ysize

    global goalS, walls
    goalS, walls = genGridworld(xsize, ysize, densw)

    print("Gridworld generated")
    print("Size: ", xsize, " ", ysize)
    print("Walls density: ", densw)
    printGridConf()

    e = 0
    for _ in range(maxEpisodes):
        end = False

        while not end:
            message = socket.recv_string()
            print("R: %s" % message)

            if message == 'init':
                message = initState()

            elif message == 'dims':
                message = sendDimentions(maxX, maxY)

            elif message == 'conf':
                message = envConf()
                e += 1

            elif message == 'END':
                end = True

            else:
                state, a = message.split()
                a = str(a)

                nx, ny, r, t = nextState(state, a)
                message  = 'x' + str(nx) + 'y' + str(ny) + ' '
                message += str(r)  + ' ' + str(t)

                x, y = state[1:].split("y")
                state = (int(x), int(y))
                printGrid(state, a, (nx, ny))

            print("S: %s" % message)
            socket.send_string(message)



################################################################################
def runEnvironment(episodes, trials):
    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    conn = "tcp://*:" + str(port)
    socket.bind(conn)
    print("Environment is up")

    global oposite, orthopos, orthoneg


    for t in range(trials):
        print("Trial: ", t)
        for xsize, ysize, densw, ao, ap, an in zip(x, y, wd, aO, aP, aN):
            oposite = ao
            orthopos = ao + ap
            orthoneg = orthopos + an

            stationaryEnvironment(socket, xsize, ysize, densw, episodes)



################################################################################
if __name__ == '__main__':
    runEnvironment(episodes, trials)


################################################################################
