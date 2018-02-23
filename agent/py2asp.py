################################################################################
def dict2asp(p, state):

    aspCode = ''
    for a in p[state]:
        nstates = list()
        for ns in p[state][a]:
            nstates.append(ns)
        aspCode += descState(nstates, a)

    return aspCode


################################################################################
def descState(states, action):
    choiceI = '1{ '
    choiceE = ' }1'
    choiceS = '; '

    sInit = 's('
    sSep = ','
    sEnd = ')'

    cond = ' :- '

    actionI = 'a('
    actionE = ')'

    ruleE = '.\n'


    # generate states list
    s = ''
    size = len(states)
    for i,state in enumerate(states):
        s += sInit + str(state) + sEnd

        # place choices separator
        if(i < size - 1): s += choiceS

    return choiceI + s + choiceE + cond + actionI + action + actionE + ruleE


################################################################################
def restrictStates(states):

    code = ''
    for s in states:
        code += ':- s(' + str(s) + ').\n'

    save('rStates.lp', code)


################################################################################
def restrictActions(actions):

    code = ''
    for a in actions:
        code = ':- a(' + str(a) + ').\n'

    save('rActions.lp', code)

################################################################################
def restrictSApairs(pairs, state):
    code = ''

    for pair in pairs:
        s = pair[0]
        if s == state:
            a = pair[1]
            code += ':- '
            code += 'a(' + str(a) + ').\n'

    name = 's' + s + 'r.lp'
    save(name, code)


################################################################################
def saveStates(states):

    code = ''
    for s in states:
        code += ':- s(' + s + ').\n'

    save('states.lp', code)


################################################################################
def saveActions(actions):
    code = '1{ '

    for a in actions[:-1]:
        code += 'a(' + str(a) + '); '

    code += 'a(' + str(actions[-1]) + ') }1.'

    save('actions.lp', code)

################################################################################
def saveGoalStates(states):

    code = ''
    for s in states:
        code += ':- s(' + s + ').\n'

    save('gStates.lp', code)


################################################################################
def save(fname, text):
    lprogram = open(fname, 'w')
    lprogram.write(text)
    lprogram.close()


################################################################################
def psa2lp(q, state):
    fname = 's' + state + '.lp'
    code = dict2asp(q, state)
    save(fname, code)


################################################################################
