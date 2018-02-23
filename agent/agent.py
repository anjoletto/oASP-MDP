
# for printing Q and P tables
import pprint
pp = pprint.PrettyPrinter(depth=100)

# random methods for action selection and state initialization
from random import random
from random import choice

# learning variables
from exp import *

# online methods of oASP(MDP)
import online

# ASP methods of oASP(MDP)
import asp

# MDP methods of oASP(MDP)
import mdp

# episode variables
tSteps = 0   # total steps in a episode
actions = [] # actions list

rmax = 0     # maximum value for reward
rmin = 0     # minimum value for reward

forbS = []  # list of forbidden states
forbA = []  # list of forbidden actions
forbSA = [] # list of forbidden state-action pairs
goalS = []  # list of goal states


################################################################################
def saveData(qs, diffQ, steps, ret, trial):
    from pickle import dump
    from os import popen

    fname = 'diffQ-' + str(trial) + '.pck'
    with open(fname,'wb') as f:
        dump(diffQ, f)

    fname = 'steps-' + str(trial) + '.pck'
    with open(fname,'wb') as f:
        dump(steps, f)

    fname = 'ret-' + str(trial) + '.pck'
    with open(fname,'wb') as f:
        dump(ret, f)

    fname = 'qsa-' + str(trial) + '.pck'
    with open(fname,'wb') as f:
        dump(qs, f)

    popen('rm *.lp')


################################################################################
def episode(q, p):

    global tSteps
    global rmin, rmax, actions

    # get connection to environment
    socket = online.initSocket(port)

    # receive env information
    rmin, rmax, actions = online.getConf(socket)

    # save actions for ASP calls
    if RUN_ASP:
        asp.saveActionList(actions, forbA)

    # agent's initial configuration
    nstate, end = online.initState(socket)

    # variables to save
    step = 0
    ret = 0

    somethingChanged = False

    # here is the oASP(MDP)
    while not end:

        ### ONLINE
        # update state
        state = nstate

        # choose action
        a = mdp.chooseAction(q, actions, state, choice, forbA, forbSA)

        # perform action in the environment
        online.sendMessage(state, a, socket)

        # receive information from environment
        nstate, rew, end = online.receiveMessage(socket)

        ### END ONLINE

        # UPDATE Q AND P FUNCTIONS AND ASP FILES
        changes = asp.updateASPfiles(q, p,
                state, a, nstate,
                rew, rmin, rmax,
                goalS, forbS, forbSA)
        somethingChanged = somethingChanged or changes
        # END UPDATE

        ### MDP
        # Q(s,a) update

        q[state][a] = mdp.updateQvalue(q, state, a, rew, nstate)


        # variables to send
        step += 1
        ret += rew

        tSteps += 1
        if step == maxSteps:
            end = True
        ### END MDP

        ### ASP CALL
        if RUN_ASP:
            if changes:
                asp.saveStateDesc(p, state)
                print("Something changed...")


        ### END ASP CALL

        if DEBUG: input("Press anykey to continue")


    online.sendEndEpisode(socket)

    if somethingChanged:
        print("Q ASP update")
        q1 = asp.genNewQ(p)

        if DEBUG: pp.pprint(q1)
        q = mdp.updateQwithASP(q, q1)

    return q, p, step, ret


################################################################################
def experiment():

    for t in range(trials):
        print("Trial: %s" % int(t+1))

        p = dict()
        q = dict()

        # variables to be saved
        qs = list()
        steps = list()
        returns = list()
        diffQ = list()
        oldq = q.copy()

        for e in range(nenvs * episodes):
            print("Episode: %s" % int(e))
            q, p, s, r = episode(q, p)

            if e % window == 0:
                d = mdp.rmsd(oldq, q)
                oldq = q.copy()
                qs.append(oldq)
                steps.append(s)
                returns.append(r)
                diffQ.append(d)

        print("Step: %s" % tSteps)

        #print("\n\nP(s,a,s)")
        #pp.pprint(p)

        print("*"*30)
        print("\n\nQ(s,a)")
        pp.pprint(q)
        print("*"*30)
        #input()

        saveData(qs, diffQ, steps, returns, t+1)

    print("\n\n")


################################################################################
experiment()
