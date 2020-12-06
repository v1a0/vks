from loguru import logger
from os import environ as env

"""
        THIS IS MAIN SETTINGS FILE
Enter here your API token and targets ids
"""

API_TOKEN = '__ENTER_YOUR_VK_API_TOKEN_HERE__'
# API_TOKEN = env['VKS_API_TOKEN']

TARGETS = [
    '12345678', '87654321'
]
# TARGETS = [
#     env['VKS_TARGET_1'], env['VKS_TARGET_2']
# ]

"""
                      ADVANCED SETTINGS
(proxy, random proxy mode, debug mode, requests frequency, other)
"""

PROXY = {
    "http": "",
    "https": "",
    "ftp": ""
}

REQ_FREQUENCY = 60

LOG_FILE_NAME = "vks.log"
LOG_MODE = "DEBUG"
MAX_LOG_FILE_SIZE = "10Mb"
COMPRESSION = "zip"

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
      %%%%%%%%% %              %%%%%%%%%             %%%%     %%%   %%% %%%%%%%/  v0.2.2
       %%%%%%    %%*         ,%%%%%%%%%
        %%%%%        %%%%*  %%%%%%%%%%
          /%%%%             %%%%%%%%
              %%%%%%%%%%%%%%%%%%
                     %%%%
"""

"""==================================================================================================
                                    DON'T TOUCH ANYTHING DOWN HERE
=====================================================================================================                         
"""

"""Set log settings
loguru.loger.add(*args, **kwargs)
"""
logger.add(LOG_FILE_NAME, level=LOG_MODE, rotation=MAX_LOG_FILE_SIZE,
           compression=COMPRESSION
           )


"""Converting targets list to string
['123', '456', '789'] to "123,456,789"
"""
temp_ = ''
for target in TARGETS:
    temp_ += ',' + str(target)

TARGETS = temp_[1:]

