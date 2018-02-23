from exp import RUN_ASP
from exp import lrate, disc, epsilon
from random import random

################################################################################
def updateQvalue(q, state, action, r, nstate):

    qsa = q[state][action]

    if nstate not in q:
        qnsna = 0
    elif not q[nstate]:
        qnsna = 0
    else:
        qnsna = q[nstate][maxA(q, nstate)]

    q = qsa + lrate * (r + disc * qnsna - qsa)

    return q


################################################################################
def maxA(q, state):
    import operator

    qstate = q[state]

    return max(qstate.items(), key=operator.itemgetter(1))[0]


################################################################################
def chooseAction(q, actions, state, rMethod, forbA, forbAS):
    # rMethod is the method for choosing random action
    if RUN_ASP:
        allowedA = allowedActions(state, actions, forbA, forbAS)
    else:
        allowedA = actions

    return eGreedy(q, state, allowedA, rMethod)


################################################################################
def eGreedy(q, state, actions, rMethod):
    r = random()

    if r <= epsilon or state not in q or not q[state]:
        return rMethod(actions)
    else:
        return maxA(q, state)


################################################################################
def allowedActions(state, actions, forbA, forbAS):

    allowed = set(actions) - set(forbA)

    for pair in forbAS:
        pstate, paction = pair
        if state == pstate: allowed.remove(paction)

    return list(allowed)


################################################################################
def updateQwithASP(old, new):
    for s in set(old) & set(new):
        for a in set(old[s]) & set(new[s]):
            new[s][a] += old[s][a]

    return new


################################################################################
def rmsd(old, new):
    from math import pow, sqrt

    diff = 0

    if old != new:

        n = 0

        sBoth = set(old) & set(new)
        sOld = set(old) - sBoth
        sNew = set(new) - sBoth

        for s in sBoth:
            aBoth = set(old[s]) & set(new[s])
            aOld = set(old[s]) - aBoth
            aNew = set(new[s]) - aBoth

            for a in aBoth:
                n += 1
                diff += pow((old[s][a] - new[s][a]),2)

            for a in aOld:
                n += 1
                diff += pow(old[s][a],2)

            for a in aNew:
                n += 1
                diff += pow(new[s][a],2)

        for s in sOld:
            for a in old[s]:
                n += 1
                diff += pow(old[s][a],2)

        for s in sNew:
            for a in new[s]:
                n += 1
                diff += pow(new[s][a],2)

        diff = diff / n

    return diff

################################################################################
