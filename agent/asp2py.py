from exp import DEBUG

################################################################################
def findAS(lp='*.lp'):
    from os import popen

    for f in lp.split():
        arg = 'touch ' + f
        popen(arg)

    models = list()

    args = 'clingo ' + lp + ' 0 '
    print("clingo call")
    output = [s for s in popen(args)]
    print("clingo over")

    for i, s in enumerate(output):
        if('Answer' in s):
            models.append(output[i + 1])

    return models


################################################################################
def statesAnSets(state):
    s = 's' + state + '.lp '
    s += 'actions.lp rActions.lp rStates.lp '
    s += 's' + state + 'r.lp '

    return findAS(s)


################################################################################
def genQfromLP(states):
    q = dict()

    for state in states:
        q[state] = dict()
        print("clingo call for state ", state)
        asets = statesAnSets(state)

        for aset in asets:
            action = aset.split(" ")
            action.sort()
            action = action[0]
            i = action.find("(") + 1
            e = action.find(")")
            action = action[i:e]
            q[state][action] = 0.0

    print("End genQfromLP")

    return q


################################################################################
