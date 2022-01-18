def loadRobot(children, config, translation = [0, 0.01, 0]):
    # creates robotString from config setting, creates robot and returns robot node
    controllerArgs = '['
    args = ''
    translation_string = str(translation[0]) + " " + str(translation[1]) + " " + str(translation[2])
    config['translation'] = translation_string
    for key,value in config['controllerArgs'].items():
        controllerArgs += '\"{}\", '.format(value)
    controllerArgs += ']'
    for key,value in config.items():
        if key != 'controllerArgs' and key != 'type':
            args += key + ' ' + value + ', '
    args += 'controllerArgs ' + str(controllerArgs)
    robotString = '{0} {{{1}}}'.format(config['type'], args)
    children.importMFNodeFromString(-1, robotString)
    return children.getMFNode(-1)
    