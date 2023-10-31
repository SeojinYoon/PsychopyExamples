
"""Display images from a specified folder and present them to the subject."""
# GoNoGoTask_d1.py
# Created 10/05/17 by DJ based on SampleExperiment_d1.py
# Updated 7/9/20 by DJ - updated param file extensions (pickle->psydat)

from psychopy import core, gui, data, event, sound, logging 
# from psychopy import visual # visual causes a bug in the guis, so it's declared after all GUIs run.
from psychopy.tools.filetools import fromFile, toFile # saving and loading parameter files
import time as ts, numpy as np # for timing and array operations
from screeninfo import get_monitors
import os, glob # for monitor size detection, files

import sys
prj_home = os.popen("git rev-parse --show-toplevel").read()
prj_home = prj_home.rstrip()
sys.path.append(os.path.join(prj_home, "GeneralTools"))

import BasicPromptTools # for loading/presenting prompts and questions
import random, math # for randomization of trials, math

# ====================== #
# ===== PARAMETERS ===== #
# ====================== #

# Data path
data_dir_path = os.path.join(prj_home, "Datas", "GoNoGoTask_d1")
os.makedirs(data_dir_path, exist_ok = True)

# Save the parameters declared below?
saveParams = True
newParamsFilename = 'GoNoGoParams.psydat'

# Declare primary task parameters.
params = {
# Declare stimulus and response parameters
    'nTrials': 10,            # number of trials in this session
    'minCueDur': 1,           # minimum duration of cue (seconds)
    'maxCueDur': 3,           # maximum duration of cue (seconds)
    'stimDur': 1,             # time when stimulus is presented (in seconds)
    'ISI': 2,                 # time between when one stimulus disappears and the next appears (in seconds)
    'tStartup': 2,            # pause time before starting first stimulus
    'tCoolDown': 2,           # pause time after end of last stimulus before "the end" text
    'triggerKey': 't',        # key from scanner that says scan is starting
    'respKeys': ['r'],           # keys to be used for responses (mapped to 1,2,3,4)
    'cueStim': 'circle',          # shape signaling oncoming trial
    'goStim': 'square',       # shape signaling respond
    'noGoStim': 'diamond',    # shape signaling don't respond
    'goStimProb': 0.8,        # probability of a given trial being a 'go' trial
    'respAdvances': False,    # should response make stimulus disappear?
# declare prompt and question files
    'skipPrompts': False,     # go right to the scanner-wait page
    'promptDir': 'Prompts/',  # directory containing prompts and questions files
    'promptFile': 'GoNoGoPrompts.txt', # Name of text file containing prompts 
# declare display parameters
    'fullScreen': True,       # run in full screen mode?
    'screenToShow': 0,        # display on primary screen (0) or secondary (1)?
    'fixCrossSize': 50,       # size of cross, in pixels
    'fixCrossPos': [0,0],     # (x,y) pos of fixation cross displayed before each stimulus (for gaze drift correction)
    'screenColor':(128,128,128) # in rgb255 space: (r,g,b) all between 0 and 255
}

# save parameters
if saveParams:
    dlgResult = gui.fileSaveDlg(prompt='Save Params...',
                                initFilePath = data_dir_path, 
                                initFileName = newParamsFilename,
        allowed="PICKLE files (.psydat)|.psydat|All files (.*)|")
    newParamsFilename = dlgResult
    if newParamsFilename is None: # keep going, but don't save
        saveParams = False
    else:
        toFile(newParamsFilename, params) # save it!

# ========================== #
# ===== SET UP LOGGING ===== #
# ========================== #
scriptName = "GoNoGoTask_d1"
expParamPath = os.path.join(data_dir_path, '%s-lastExpInfo.psydat'%scriptName)

try: # try to get a previous parameters file
    expInfo = fromFile(expParamPath)
    expInfo['session'] +=1 # automatically increment session number
    expInfo['paramsFile'] = [expInfo['paramsFile'],'Load...']
except: # if not there then use a default set
    expInfo = {
        'subject':'1', 
        'session': 1, 
        'skipPrompts':False, 
        'paramsFile':['DEFAULT','Load...']}
# overwrite params struct if you just saved a new parameter set
if saveParams:
    expInfo['paramsFile'] = [newParamsFilename,'Load...']

#present a dialogue to change select params
dlg = gui.DlgFromDict(expInfo, title=scriptName, order=['subject','session','skipPrompts','paramsFile'])
if not dlg.OK:
    core.quit() # the user hit cancel, so exit

# find parameter file
if expInfo['paramsFile'] == 'Load...':
    dlgResult = gui.fileOpenDlg(prompt = 'Select parameters file',
                                tryFilePath = data_dir_path,
                                allowed = "PICKLE files (.psydat)|.psydat|All files (.*)|")
    expInfo['paramsFile'] = dlgResult[0]
# load parameter file
if expInfo['paramsFile'] not in ['DEFAULT', None]: # otherwise, just use defaults.
    # load params file
    params = fromFile(expInfo['paramsFile'])


# transfer skipPrompts from expInfo (gui input) to params (logged parameters)
params['skipPrompts'] = expInfo['skipPrompts']

# print params to Output
print('params = {')
for key in sorted(params.keys()):
    print("   '%s': %s"%(key,params[key])) # print each value as-is (no quotes)
print('}')
    
# save experimental info
toFile(expParamPath, expInfo)#save params to file for next time

#make a log file to save parameter/event  data
dateStr = ts.strftime("%b_%d_%H%M", ts.localtime()) # add the current time
filename = '%s-%s-%d-%s'%(scriptName,expInfo['subject'], expInfo['session'], dateStr) # log filename
logPath = os.path.join(data_dir_path, filename) + '.log'
logging.LogFile(logPath, level=logging.INFO)#, mode='w') # w=overwrite
logging.log(level=logging.INFO, msg='---START PARAMETERS---')
logging.log(level=logging.INFO, msg='filename: %s'%filename)
logging.log(level=logging.INFO, msg='subject: %s'%expInfo['subject'])
logging.log(level=logging.INFO, msg='session: %s'%expInfo['session'])
logging.log(level=logging.INFO, msg='date: %s'%dateStr)
# log everything in the params struct
for key in sorted(params.keys()): # in alphabetical order
    logging.log(level=logging.INFO, msg='%s: %s'%(key,params[key])) # log each parameter

logging.log(level=logging.INFO, msg='---END PARAMETERS---')


# ========================== #
# ===== GET SCREEN RES ===== #
# ========================== #

# kluge for secondary monitor
if params['fullScreen']: 
    mon = get_monitors()[int(params['screenToShow'])]
    screenRes = (mon.width, mon.height)
    params['fullScreen'] = False
    if params['screenToShow']>0:
        params['fullScreen'] = False
else:
    screenRes = [800,600]

print("screenRes = [%d,%d]"%screenRes)


# ========================== #
# ===== SET UP STIMULI ===== #
# ========================== #
from psychopy import visual

# Initialize deadline for displaying next frame
tNextFlip = [0.0] # put in a list to make it mutable (weird quirk of python variables) 

#create clocks and window
globalClock = core.Clock()#to keep track of time
trialClock = core.Clock()#to keep track of time
win = visual.Window(screenRes, fullscr=params['fullScreen'], allowGUI=False, monitor='testMonitor', screen=params['screenToShow'], units='deg', name='win',color=params['screenColor'],colorSpace='rgb255')
# create fixation cross
fCS = params['fixCrossSize'] # size (for brevity)
fCP = params['fixCrossPos'] # position (for brevity)
fixation = visual.ShapeStim(win,lineColor='#000000',lineWidth=3.0,vertices=((fCP[0]-fCS/2,fCP[1]),(fCP[0]+fCS/2,fCP[1]),(fCP[0],fCP[1]),(fCP[0],fCP[1]+fCS/2),(fCP[0],fCP[1]-fCS/2)),units='pix',closeShape=False,name='fixCross');
# create text stimuli
message1 = visual.TextStim(win, pos=[0,+.5], wrapWidth=1.5, color='#000000', alignHoriz='center', name='topMsg', text="aaa",units='norm')
message2 = visual.TextStim(win, pos=[0,-.5], wrapWidth=1.5, color='#000000', alignHoriz='center', name='bottomMsg', text="bbb",units='norm')

# draw stimuli
fCS_rt2 = fCS/math.sqrt(2);
stims = {'square':[],'diamond':[],'circle':[]}
stims['square'] = visual.ShapeStim(win,lineColor='#000000',lineWidth=3.0,vertices=((fCP[0]-fCS/2,fCP[1]-fCS/2),(fCP[0]+fCS/2,fCP[1]-fCS/2),(fCP[0]+fCS/2,fCP[1]+fCS/2),(fCP[0]-fCS/2,fCP[1]+fCS/2),(fCP[0]-fCS/2,fCP[1]-fCS/2)),units='pix',closeShape=False,name='square');
stims['diamond'] = visual.ShapeStim(win,lineColor='#000000',lineWidth=3.0,vertices=((fCP[0],fCP[1]-fCS_rt2),(fCP[0]-fCS_rt2,fCP[1]),(fCP[0],fCP[1]+fCS_rt2),(fCP[0]+fCS_rt2,fCP[1]),(fCP[0],fCP[1]-fCS_rt2)),units='pix',closeShape=False,name='diamond');
stims['circle'] = visual.Circle(win,lineColor='#000000',lineWidth=3.0,radius=fCS_rt2,edges=32,units='pix')

# read questions and answers from text files
[topPrompts,bottomPrompts] = BasicPromptTools.ParsePromptFile(params['promptDir']+params['promptFile'])
print('%d prompts loaded from %s'%(len(topPrompts),params['promptFile']))

# ============================ #
# ======= SUBFUNCTIONS ======= #
# ============================ #

# increment time of next window flip
def AddToFlipTime(tIncrement=1.0):
    tNextFlip[0] += tIncrement

# flip window as soon as possible
def SetFlipTimeToNow():
    tNextFlip[0] = globalClock.getTime()

def RunTrial(iTrial):
    
    # Decide Trial Params
    isGoTrial = random.random()<params['goStimProb']
    cueDur = random.randrange(params['minCueDur'], params['maxCueDur'])
    
    # display info to experimenter
    print('Running Trial %d: isGo = %d, cueDur = %.1f'%(iTrial,isGoTrial,cueDur)) 
    
    # Draw cue
    stims[params['cueStim']].draw()
    # Wait until it's time to display
    while (globalClock.getTime()<tNextFlip[0]):
        pass
    # log & flip window to display image
    win.logOnFlip(level=logging.EXP, msg='Display cue (%s)'%params['cueStim'])
    win.flip()
    tStimStart = globalClock.getTime() # record time when window flipped
    # set up next win flip time after this one
    AddToFlipTime(cueDur) # add to tNextFlip[0]
    
    # Draw stim
    if isGoTrial:
        stims[params['goStim']].draw()
        win.logOnFlip(level=logging.EXP, msg='Display go stim (%s)'%params['goStim'])
    else:
        stims[params['noGoStim']].draw()
        win.logOnFlip(level=logging.EXP, msg='Display no-go stim (%s)'%params['noGoStim'])
    # Wait until it's time to display
    while (globalClock.getTime()<tNextFlip[0]):
        pass
    # log & flip window to display image
    win.flip()
    tStimStart = globalClock.getTime() # record time when window flipped
    # set up next win flip time after this one
    AddToFlipTime(params['stimDur']) # add to tNextFlip[0]
        
    # Flush the key buffer and mouse movements
    event.clearEvents()
    # Wait for relevant key press or 'stimDur' seconds
    respKey = None
    while (globalClock.getTime()<tNextFlip[0]): # until it's time for the next frame
        # get new keys
        newKeys = event.getKeys(keyList=params['respKeys']+['q','escape'],timeStamped=globalClock)
        # check each keypress for escape or response keys
        if len(newKeys)>0:
            for thisKey in newKeys: 
                if thisKey[0] in ['q','escape']: # escape keys
                    CoolDown() # exit gracefully
                elif thisKey[0] in params['respKeys'] and respKey == None: # only take first keypress
                    respKey = thisKey # record keypress
                    if params['respAdvances']: # if response should advance to next stimulus
                        fixation.draw() # show fixation but don't change flip time
                        # SetFlipTimeToNow() # reset flip time
        
    # Display the fixation cross
    if params['ISI']>0:# if there should be a fixation cross
        fixation.draw() # draw it
        win.logOnFlip(level=logging.EXP, msg='Display Fixation')
        win.flip()
        
    return 

# Handle end of a session
def CoolDown():
    
    # display cool-down message
    message1.setText("That's the end! ")
    message2.setText("Press 'q' or 'escape' to end the session.")
    win.logOnFlip(level=logging.EXP, msg='Display TheEnd')
    message1.draw()
    message2.draw()
    win.flip()
    thisKey = event.waitKeys(keyList=['q','escape'])
    
    # exit
    core.quit()


# =========================== #
# ======= RUN PROMPTS ======= #
# =========================== #

# display prompts
if not params['skipPrompts']:
    BasicPromptTools.RunPrompts(topPrompts,bottomPrompts,win,message1,message2)

# wait for scanner
message1.setText("Waiting for scanner to start...")
message2.setText("(Press '%c' to override.)"%params['triggerKey'].upper())
message1.draw()
message2.draw()
win.logOnFlip(level=logging.EXP, msg='Display WaitingForScanner')
win.flip()
event.waitKeys(keyList=params['triggerKey'])
tStartSession = globalClock.getTime()
AddToFlipTime(tStartSession+params['tStartup'])

# wait before first stimulus
fixation.draw()
win.logOnFlip(level=logging.EXP, msg='Display Fixation')
win.flip()




# =========================== #
# ===== MAIN EXPERIMENT ===== #
# =========================== #

# log experiment start and set up
logging.log(level=logging.EXP, msg='---START EXPERIMENT---')

# run trials
for iTrial in range(0,params['nTrials']):
    # display text
    RunTrial(iTrial)
    if iTrial < params['nTrials']:
        # pause
        AddToFlipTime(params['ISI'])
    else: 
        AddToFlipTime(params['tCoolDown'])

# wait before 'the end' text
fixation.draw()
win.flip()
while (globalClock.getTime()<tNextFlip[0]):
        pass

# Log end of experiment
logging.log(level=logging.EXP, msg='--- END EXPERIMENT ---')

# exit experiment
CoolDown()
