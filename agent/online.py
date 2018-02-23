def initSocket(port):
    import zmq

    #print("Connecting to the environment")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    address = "tcp://localhost:"
    address += str(port)
    socket.connect(address)

    return socket

################################################################################
def initState(socket):
    socket.send_string('init')
    state = socket.recv_string()
    end = False

    return state, end


################################################################################
def getConf(socket):
    socket.send_string('conf')
    message = socket.recv_string()
    message = message.split()

    rmax = float(message.pop(-1))

    rmin = float(message.pop(-1))

    actions = message

    return rmax, rmin, actions


################################################################################
def sendMessage(state, a, socket):
    message = ''
    message = state + ' ' + a

    #print("S: %s" % message)
    socket.send_string(message)

    return message


################################################################################
def receiveMessage(socket):
    message = socket.recv_string()
    #print("R: %s " % message)
    nstate, r, t = message.split()
    rew = float(r)
    end = eval(t)

    return nstate, rew, end
################################################################################
def sendEndEpisode(socket):
    message = "END"
    socket.send_string(message)


################################################################################
