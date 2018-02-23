import asp2py
import py2asp

from exp import RUN_ASP, DETERMINISTIC


################################################################################
def updateASPfiles(q, p, state, action, nstate,
        rew, rmin, rmax,
        goalS, forbS, forbAS):

    somethingChanged = False
    # update restriction list

    # forbidden state-action pairs
    ## criteria: transition to the same state
    if DETERMINISTIC:
        if state == nstate and [state, action] not in forbAS:
            forbAS.append([state, action])
            if RUN_ASP:
                py2asp.restrictSApairs(forbAS, state)
            somethingChanged = True

    # forbidden actions
    # criteria: ???

    # forbidden states
    ## criteria: minimum reward
    if rew == rmin and nstate not in forbS:
        forbS.append(nstate)
        if RUN_ASP:
            py2asp.restrictStates(forbS)
        somethingChanged = True

    # save goal state
    ## criteria: maximum reward
    if rew == rmax and nstate not in goalS:
        goalS.append(nstate)
        if RUN_ASP:
            py2asp.saveGoalStates(goalS)
        somethingChanged = True

    # update Q and P functions
    if state not in p:
        p[state] = dict()
        somethingChanged = True

    if state not in q:
        q[state] = dict()
        somethingChanged = True

    if action not in p[state]:
        p[state][action] = list()
        somethingChanged = True

    if action not in q[state]:
        q[state][action] = 0
        somethingChanged = True

    if nstate not in p[state][action]:
        p[state][action].append(nstate)
        somethingChanged = True

    if somethingChanged:
        if RUN_ASP:
            py2asp.psa2lp(p, state)

    return somethingChanged


################################################################################
def genNewQ(p):
    print("genNewQ")
    return asp2py.genQfromLP(p.keys())


################################################################################
def saveActionList(actions, forbA):
    py2asp.saveActions(actions)
    py2asp.restrictActions(forbA)


################################################################################
def saveStateDesc(p, state):
    py2asp.psa2lp(p, state)


################################################################################
