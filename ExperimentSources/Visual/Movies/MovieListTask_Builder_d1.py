#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.90.1),
    on Tue May  8 15:02:31 2018

Created 5/8/18 by DJ.
Updated 5/8/18 by DJ - added NetStationEEG code from https://github.com/imnotamember/PyNetstation (per Pete's instructions)
Updated 6/8/18 by DJ - made into list of movie files instead of single movie files
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Declare movie params
params = {
    'movieFileList': u'/Users/clmn/Downloads/PsychoPyParadigms-master/BasicExperiments/Movies/MovieList.txt', # text file with spaces/linebreaks between movies
    'imiDur': 5.0, # time between movies.
    'warmUpTime': 6.0, # time before first movie
    'coolDownTime': 6.0, # time after last movie
    'movieSize': (640.0*3,360.0*3), # for Boldscreen
    'fixCrossHeight': 0.5,
    # eeg params
    'isEegConnected': False, # is an EGI EEG system connected?
    'tcpipAddress': '10.10.10.42',
    'tcpipPort': 55513
}

# Load movies
fid = open(params['movieFileList'],'r')
movieFileText = fid.read()
movieFiles = movieFileText.split()
fid.close()

print("%d movie files read."%(len(movieFiles)))
print(movieFiles)

# === EEG === #
# === Initialize
if params['isEegConnected'] == False:
    # # This will import the debugging version of the PyNetStation module,
    # #  which will not actually attempt a connection but will check to make sure
    # #  your code is properly functioning.
    import egi.fake as egi  # FOR TESTING WITHOUT CONNECTION TO NETSTATION COMPUTER
else:
    # # This will import the single-threaded version of the PyNetStation module
    import egi.simple as egi # FOR RUNNING CONNECTED TO NETSTATION COMPUTER -- USE THIS IN A REAL EXPERIMENT

# === Timing Obj
# # Create a proper timing object to reference. To retrieve the time you want later,
# #  call this method using ms_localtime(), it returns the time in a millisecond format
# #  appropriate for the NetStation TCP/IP protocol.
# # This is only necessary if you are in need of direct contact with the clock object that NetStation is utilizing,
# #  which you don't actually need since it's working behind the scenes in the egi module.
# ms_localtime = egi.ms_localtime

# === Netstation Obj
# # Create the NetStation event-sending object. After this you can call
# #  the methods via the object instance, in this case 'ns'.
ns = egi.Netstation()

# === Establish Cxn
# # The next line is for connecting the actual, single-threaded module version to the computer.
if params['isEegConnected']:
    ns.connect(params['tcpipAddress'], params['tcpipPort'])  # sample address and port -- change according to your network settings

# === Link Expt to Session
# # This sends some initialization info to NetStation for recording events.
ns.BeginSession()
# # This synchronizes the clocks of the stim computer and the NetStation computer.
ns.sync()

# === END EEG === #


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = u'MovieListTask_Builder_d1'  # Name of experiment
expInfo = {'session': '001', 'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/jangrawdc/Documents/Python/PsychoPyParadigms/BasicExperiments/TEST.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "Trigger"
TriggerClock = core.Clock()
TriggerText = visual.TextStim(win=win, name='TriggerText',
    text=u'Waiting for trigger...\n\n(Experimenter: press t to override.)',
    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "Fixation"
fixationClock = core.Clock()
fixCross = visual.TextStim(win=win, name='fixCross',
    text=u'+',
    font=u'Arial',
    pos=(0, 0), height=params['fixCrossHeight'], wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "Movie"
MovieClock = core.Clock()
movie = []
movieDur = [0]*len(movieFiles)
for i in range(len(movieFiles)):
    movie.append(visual.MovieStim3(
        win=win, name='movie',
        noAudio = False,
        filename=movieFiles[i],
        ori=0, pos=(0, 0), size=params['movieSize'], opacity=1,
        depth=0.0,
        ))
    # save out duration of this movie
    movieDur[i] = movie[i].duration
    # print results for debugging
    print('Movie %d: loaded %s'%(i, movieFiles[i]))
    print('duration: %f'%movieDur[i]);

ImiText = fixCross

# Initialize components for Routine "WaitForEnd"
WaitForEndClock = core.Clock()
WaitForEndText = visual.TextStim(win=win, name='WaitForEndText',
    text=u'Please stay still until\nthe scanner noise stops.',
    font=u'Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 


# === EEG === #
# # This starts the recording in NetStation acquisition. Equivalent to pressing the Record button.
# # If at some point you pause the experiment using the "StopRecording()" method,
# #  just call this method again to restart the recording.
ns.StartRecording()

# === END EEG === #



# ------Prepare to start Routine "Trigger"-------
t = 0
TriggerClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
TriggerKey = event.BuilderKeyResponse()
# keep track of which components have finished
TriggerComponents = [TriggerText, TriggerKey]
for thisComponent in TriggerComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# === EEG === #
# # This re-aligns the clocks between the stim computer and the NetStation computer.
# # Best to put at the start of each trial for maximal timing accuracy.
ns.sync()
# Send Message to EEG
win.callOnFlip(ns.send_event, key='WAIT', timestamp=None, label="WaitForTrigger", description="Waiting for Trigger from fMRI", pad=False)

# === END EEG === #


# -------Start Routine "Trigger"-------
while continueRoutine:
    # get current time
    t = TriggerClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *TriggerText* updates
    if t >= 0.0 and TriggerText.status == NOT_STARTED:
        # keep track of start time/frame for later
        TriggerText.tStart = t
        TriggerText.frameNStart = frameN  # exact frame index
        TriggerText.setAutoDraw(True)
    
    # *TriggerKey* updates
    if t >= 0.0 and TriggerKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        TriggerKey.tStart = t
        TriggerKey.frameNStart = frameN  # exact frame index
        TriggerKey.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(TriggerKey.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if TriggerKey.status == STARTED:
        theseKeys = event.getKeys(keyList=['t'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            TriggerKey.keys = theseKeys[-1]  # just the last key pressed
            TriggerKey.rt = TriggerKey.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in TriggerComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Trigger"-------
for thisComponent in TriggerComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if TriggerKey.keys in ['', [], None]:  # No response was made
    TriggerKey.keys=None
thisExp.addData('TriggerKey.keys',TriggerKey.keys)
if TriggerKey.keys != None:  # we had a response
    thisExp.addData('TriggerKey.rt', TriggerKey.rt)
thisExp.nextEntry()
# the Routine "Trigger" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()




# ------Prepare to start Routine "fixation"-------
t = 0
fixationClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(params['warmUpTime'])
# update component parameters for each repeat
# keep track of which components have finished
fixationComponents = [fixCross]
for thisComponent in fixationComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# === EEG === #
# # This re-aligns the clocks between the stim computer and the NetStation computer.
# # Best to put at the start of each trial for maximal timing accuracy.
ns.sync()
# Send Message to EEG
win.callOnFlip(ns.send_event, key='FIX', timestamp=None, label="Fixation", description="Fixation Cross", pad=False)
# === END EEG === #

# -------Start Routine "fixation"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = fixationClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *fixCross* updates
    if t >= 0.0 and fixCross.status == NOT_STARTED:
        # keep track of start time/frame for later
        fixCross.tStart = t
        fixCross.frameNStart = frameN  # exact frame index
        fixCross.setAutoDraw(True)
    frameRemains = 0.0 + params['warmUpTime'] - win.monitorFramePeriod * 0.75  # most of one frame period left
    if fixCross.status == STARTED and t >= frameRemains:
        fixCross.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in fixationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "fixation"-------
for thisComponent in fixationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)



# ------Prepare to start Routine "Movie"-------
# update component parameters for each repeat
# keep track of which components have finished
MovieComponents = movie + [ImiText]
for thisComponent in MovieComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# ------Start Movie Loop-------
for i in range(len(movie)):
    # initialize vars
    t = 0
    MovieClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # Update timer
    if i<(len(movie)-1):
        routineTimer.add(movieDur[i]+params['imiDur'])
    else:
        routineTimer.add(movieDur[i])
        
    # Make sure repeated-use ImiText object is listed as "not started"
    ImiText.status = NOT_STARTED
            
    # === EEG === #
    # # This re-aligns the clocks between the stim computer and the NetStation computer.
    # # Best to put at the start of each trial for maximal timing accuracy.
    ns.sync()
    # Send Message to EEG
    win.callOnFlip(ns.send_event, key='MOVI', timestamp=None, label="StartMovie%d"%i, description="Started Movie %d"%i, pad=False)
    # === END EEG === #
    
    # -------Start Routine "Movie"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = MovieClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie* updates
        if t >= 0.0 and movie[i].status == NOT_STARTED:
            # keep track of start time/frame for later
            movie[i].tStart = t
            movie[i].frameNStart = frameN  # exact frame index
            movie[i].setAutoDraw(True)
        frameRemains = 0.0 + movieDur[i]- win.monitorFramePeriod * 0.75  # most of one frame period left
        if movie[i].status == STARTED and t >= frameRemains:
            movie[i].setAutoDraw(False)
            
        # *ImiText* updates
        if t >= movieDur[i] and ImiText.status == NOT_STARTED and i<(len(movie)-1):
            # keep track of start time/frame for later
            ImiText.tStart = t
            ImiText.frameNStart = frameN  # exact frame index
            ImiText.setAutoDraw(True)
            # === EEG === #
            # # This re-aligns the clocks between the stim computer and the NetStation computer.
            # # Best to put at the start of each trial for maximal timing accuracy.
            ns.sync()
            # Send Message to EEG
            win.callOnFlip(ns.send_event, key='IMI', timestamp=None, label="Inter-Movie Interval", description="Inter-Movie Interval", pad=False)
            # === END EEG === #
            
        frameRemains = movieDur[i] + params['imiDur']- win.monitorFramePeriod * 0.75  # most of one frame period left
        if ImiText.status == STARTED and t >= frameRemains:
            ImiText.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in MovieComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    

# -------Ending Routine "Movie"-------
for thisComponent in MovieComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


# ------Prepare to start Routine "fixation"-------
t = 0
fixationClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(params['coolDownTime'])
# update component parameters for each repeat
# keep track of which components have finished
fixationComponents = [fixCross]
for thisComponent in fixationComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# === EEG === #
# # This re-aligns the clocks between the stim computer and the NetStation computer.
# # Best to put at the start of each trial for maximal timing accuracy.
ns.sync()
# Send Message to EEG
win.callOnFlip(ns.send_event, key='FIX', timestamp=None, label="Fixation", description="Fixation Cross", pad=False)
# === END EEG === #

# -------Start Routine "fixation"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = fixationClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *fixCross* updates
    if t >= 0.0 and fixCross.status == NOT_STARTED:
        # keep track of start time/frame for later
        fixCross.tStart = t
        fixCross.frameNStart = frameN  # exact frame index
        fixCross.setAutoDraw(True)
    frameRemains = 0.0 + params['coolDownTime'] - win.monitorFramePeriod * 0.75  # most of one frame period left
    if fixCross.status == STARTED and t >= frameRemains:
        fixCross.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in fixationComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "fixation"-------
for thisComponent in fixationComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)





# ------Prepare to start Routine "WaitForEnd"-------
t = 0
WaitForEndClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
EndKey = event.BuilderKeyResponse()
# keep track of which components have finished
WaitForEndComponents = [WaitForEndText, EndKey]
for thisComponent in WaitForEndComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# === EEG === #
# # This re-aligns the clocks between the stim computer and the NetStation computer.
# # Best to put at the start of each trial for maximal timing accuracy.
ns.sync()
# Send Message to EEG
win.callOnFlip(ns.send_event, key='END', timestamp=None, label="WaitForEnd", description="Waiting for End of Scan", pad=False)

# === END EEG === #

# -------Start Routine "WaitForEnd"-------
while continueRoutine:
    # get current time
    t = WaitForEndClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *WaitForEndText* updates
    if t >= 0.0 and WaitForEndText.status == NOT_STARTED:
        # keep track of start time/frame for later
        WaitForEndText.tStart = t
        WaitForEndText.frameNStart = frameN  # exact frame index
        WaitForEndText.setAutoDraw(True)
    
    # *EndKey* updates
    if t >= 0.0 and EndKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        EndKey.tStart = t
        EndKey.frameNStart = frameN  # exact frame index
        EndKey.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(EndKey.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if EndKey.status == STARTED:
        theseKeys = event.getKeys(keyList=['q', 'escape'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            EndKey.keys = theseKeys[-1]  # just the last key pressed
            EndKey.rt = EndKey.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in WaitForEndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "WaitForEnd"-------
for thisComponent in WaitForEndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if EndKey.keys in ['', [], None]:  # No response was made
    EndKey.keys=None
thisExp.addData('EndKey.keys',EndKey.keys)
if EndKey.keys != None:  # we had a response
    thisExp.addData('EndKey.rt', EndKey.rt)
thisExp.nextEntry()
# the Routine "WaitForEnd" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# === EEG === #
# # This re-aligns the clocks between the stim computer and the NetStation computer.
# # Best to put at the start of each trial for maximal timing accuracy.
ns.sync()
# Send Message to EEG
win.callOnFlip(ns.send_event, key='DONE', timestamp=None, label="ExperimentDone", description="End of Scan", pad=False)

# === End Session
# # This method is misleading, as it merely pauses the recording in NetStation. Equivalent to the pause button.
# # It is not actually stopping the recording session. That is done by the 'EndSession()' method.
ns.StopRecording()

# # I don't typically use this, as it is closes the current "Session" in NetStation.
# # I find it easier to just pause the recording using "StopRecording()" and then
# # get ending impedance measurements before manually closing NetStation.
ns.EndSession()

# # This line ends the connection via the ns object, and should then be destroying the object itself.
# # It is good practice to use so as not to waste memory or leave TCP/IP links open, which could lead to being
# # unable to reconnect without restarting the computer running the experiment.
if params['isEegConnected']:
    ns.disconnect()

# === END EEG === #

# ----------Finishing Experiment----------
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
