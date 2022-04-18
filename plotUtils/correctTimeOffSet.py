from asyncio import threads


def correctTimeOffSet(cedarSounds, webotsSounds):
    """Corrects the time offset between measurments in Webots and in Cedar. This can only be done approximatley since simulation time in Webots 
    varies depending on the number of simulated Objects and load tasks. Maybe use real time for this instead-> that should run in sync with cedar
    ::args::
        cedarSounds: Dataframe of heard sounds
        cedarComm: Dataframe of recorded sounds in webots

    ::return::
        lookUpFunction: function transforming cedar time to webots time
    """
    threshold = 0.1
    cedar_T = list(cedarSounds.loc[lambda cedarSounds: (cedarSounds['S1']>threshold) | (cedarSounds['S2']>threshold) | (cedarSounds['S3']>threshold), ['T']]['T'])
    first_cedar_sound = cedar_T[0]
    last_cedar_sound = cedar_T[-1]
    cedar_duration = last_cedar_sound - first_cedar_sound

    
    webotsSounds['sound'] = webotsSounds['sound'].apply(lambda s: sum(s))
    webots_T = list(webotsSounds.loc[lambda webotsSounds: webotsSounds['sound']>threshold, ['T']]['T'])
    first_webots_sound = webots_T[0]
    last_webots_sound = webots_T[-1]
    webots_duration = last_webots_sound - first_webots_sound

    start_offset = first_webots_sound - first_cedar_sound
    end_offset = last_webots_sound - last_cedar_sound

    print("first sound cedar: {}".format(first_cedar_sound))
    print("last sound cedar: {}".format(last_cedar_sound))
    print("first sound webots: {}".format(first_webots_sound))
    print("last sound webots: {}".format(last_webots_sound))

    return lambda t_ced: webots_duration/cedar_duration * t_ced + start_offset