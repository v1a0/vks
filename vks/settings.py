"""
        THIS IS MAIN SETTINGS FILE
Enter here your API token and targets ids
"""

API_TOKEN = '__ENTER_YOUR_VK_API_TOKEN_HERE__'

TARGETS = [
    '123', '23456'
]


""" 
            ADVANCED SETTINGS [NOT AVAILABLE NOW]
(proxy, random proxy mode, debug mode, requests frequency, other)
"""

PROXY = [
    None
]

RAND_PROXY = False

DEBUG = True

REQ_FREQUENCY = 60


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
      %%%%%%%%% %              %%%%%%%%%             %%%%     %%%   %%% %%%%%%%/  v0.2
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



"""Converting targets list to string
['123', '456', '789'] to "123,456,789"
"""
temp_ = ''
for target in TARGETS:
    temp_ += ',' + str(target)

TARGETS = temp_[1:]
