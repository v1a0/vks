from os import environ as env
import modules

"""
            THIS IS MAIN SETTINGS FILE
    Enter here your API token(s) and target(s) ids
"""

API_TOKENS = [
    '__ENTER_YOUR_VK_API_TOKEN_HERE__',
]

TARGETS_IDS = [
    '12345678', '87654321'
]


"""
==============================================================================
                        ADVANCED SETTINGS (Optional)
            Don't touch it if you don't know what are you doing!
(proxy settings, modules to use, modules excepts, requests frequency, other)
==============================================================================
"""

MODULES = [
    modules.onliner,
    modules.hidden_friends,
    # modules.template,
]

MODULES_TIMEOUTS = {
    modules.onliner: 60,            # 60 seconds
    modules.hidden_friends: 13E7,   # only once after run
    # modules.template: 0,
}

MODULES_EXCEPTS = {
    MODULES[1]: [TARGETS_IDS[1], TARGETS_IDS[2], TARGETS_IDS[3]]
}

PROXY = {
    "http": "",
    "https": "",
    "ftp": ""
}


REQ_FREQUENCY = 0.01

GREETING_ART = """
                 #%%%%%%%%%%%
            ,%%%%%#         %%%%%%
          %%%%%%               %%%%%
        %%%%%%%                  %%%%%
      ,%%%%%%%                    %%%%%%         %%%      %%  %%%  %%%  /%%%%%%%
      %%%%%%%%                    %%%%%%.         %%%    %%#  %%%%%%    %%%.
     %%%%%%%%%       %%%  %%%   %%%%%%%%%          %%%  %%%   %%%%%       %%%%%
     %%%%%%%%%%       %%% %%% %%%%%%%%%%%           %%%%%%    %%%%%%          %%%
     %%%%%%%%%%%       %%%%% %%%(%%%%%%%%            %%%%%    %%%  %%%  %    %%%%
      %%%%%%%%% %              %%%%%%%%%             %%%%     %%%   %%% %%%%%%%/  v0.2.6
       %%%%%%    %%*         ,%%%%%%%%%
        %%%%%        %%%%*  %%%%%%%%%%
          /%%%%             %%%%%%%%
              %%%%%%%%%%%%%%%%%%
                     %%%%
"""
