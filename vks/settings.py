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
    # modules.template
]

MODULES_EXCEPTS = {

}

PROXY = {
    "http": "",
    "https": "",
    "ftp": ""
}

PROXY_FOR_BOT = {
    
}

REQ_FREQUENCY = 0.1

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
      %%%%%%%%% %              %%%%%%%%%             %%%%     %%%   %%% %%%%%%%/  v0.2.4
       %%%%%%    %%*         ,%%%%%%%%%
        %%%%%        %%%%*  %%%%%%%%%%
          /%%%%             %%%%%%%%
              %%%%%%%%%%%%%%%%%%
                     %%%%
"""
