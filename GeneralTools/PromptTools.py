#!/usr/bin/env python2
"""Load Questions, Run Prompts, and Run Probe Trials."""
# PromptTools.py
# Created 1/30/15 by DJ based on VidLecTask.py
# Updated 3/16/15 by DJ - added ReadingTask_dict.py
# Updated 9/8/15 by DJ - added Likert option and RunQuestions_Move.
# Updated 10/29/15 by DJ - updated distraction/reading task prompts to ask subjects to read top to bottom.
# Updated 11/9/15 by DJ - added ParsePromptFile function.
# Updated 1/11/16 by DJ - added fwdKeys input to RunPrompts function
# Updated 1/14/16 by DJ - added returnTimes input to ParseQuestionsAll (extracts pages and times of questions), added 'First' conditions to GetPrompts
# Updated 1/20/16 by DJ - fixed RunPrompts fwdKeys default
# Updated 1/24/17 by DJ - removed import of visual, fixed question timeout
# Updated 3/17/17 by DJ - added SingingTask

from psychopy import core, event, logging#, visual # visual and gui conflict, so don't import it here
import time
import string


# --- PARSE QUESTION FILE INTO QUESTIONS AND OPTIONS --- #
def ParseQuestionFile(filename,optionsType=None,returnTimes=False): # optionsType 'Likert' returns the Likert scale for every question's options.
    # initialize
    questions_all = []
    answers_all = []
    options_all = []
    pages_all = []
    times_all = []
    if optionsType is None:
        options_this = []
    elif optionsType == 'Likert':
        options_likert = ['Strongly agree','Agree','Neutral','Disagree','Strongly disagree']
        options_this = options_likert
        
    # parse questions & answers
    with open(filename) as f:
        for line in f:
            # remove the newline character at the end of the line
            line = line.replace('\n','')
            # replace any newline strings with newline characters
            line = line.replace('\\n','\n')
            # pass to proper output
            if line.startswith("-"): # incorrect answer
                options_this.append(line[1:]) # omit leading -
            elif line.startswith("+"): # correct answer
                options_this.append(line[1:]) # omit leading +
                answers_all.append(len(options_this))
            elif line.startswith("?"): # question
                questions_all.append(line[1:]) # omit leading ?
                # if it's not the first question, add the options to the list.
                if options_this:
                    options_all.append(options_this)
                    if optionsType is None:
                        options_this = [] #reset
                    elif optionsType == 'Likert':
                        options_this = options_likert
            elif line.startswith("#"): # question header
                pieces = line.split(',')
                for piece in pieces:
                    nameval = piece.split() # split at space
                    if nameval[0] == 'PAGE':
                        pages_all.append(nameval[1])
                    elif nameval[0] == 'TIME':
                        minsec = nameval[1].split(':')
                        times_this = int(minsec[0])*60+int(minsec[1])
                        times_all.append(times_this)
                    # info[nameval[0]] = nameval[1]
                        
    # make sure last set of options is included
    options_all.append(options_this) 
    # return results
    if returnTimes:
        return (questions_all,options_all,answers_all,pages_all,times_all)
    else:
        return (questions_all,options_all,answers_all)

# --- PARSE PROMPT FILE INTO TOP AND BOTTOM PROMPTS --- #
# Each top prompt should be preceded by a +. Each bottom prompt should be preceded by a -. Everything else will be ignored.
def ParsePromptFile(filename): 
    # initialize
    topPrompts = []
    bottomPrompts = []
        
    # parse questions & answers
    with open(filename) as f:
        for line in f:
            # remove the newline character at the end of the line
            line = line.replace('\n','')
            # replace any newline strings with newline characters
            line = line.replace('\\n','\n')
            # pass to proper output
            if line.startswith("-"): # bottom prompt
                bottomPrompts.append(line[1:]) # omit leading -
            elif line.startswith("+"): # top prompt
                topPrompts.append(line[1:]) # omit leading +
                # if it's not the first question, add the options to the list.
                        
    # return results
    return (topPrompts,bottomPrompts)

# Display prompts and let the subject page through them one by one.
def RunPrompts(topPrompts,bottomPrompts,win,message1,message2,fwdKeys=None,backKeys=['backspace'],backPrompt=0):
    iPrompt = 0
    
    # declare default for fwdKeys
    if fwdKeys is None:
        fwdKeys = [chr(i) for i in range(127)]
        
    while iPrompt < len(topPrompts):
        message1.setText(topPrompts[iPrompt])
        message2.setText(bottomPrompts[iPrompt])
        #display instructions and wait
        message1.draw()
        message2.draw()
        win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(iPrompt+1))
        win.flip()
        #check for a keypress
       	thisKey = event.waitKeys(keyList = fwdKeys + backKeys + ['q', 'escape'])
        if thisKey[0] in ['q','escape']:
            core.quit()
        elif thisKey[0] in fwdKeys:
            iPrompt += 1
        elif thisKey[0] in backKeys:
            iPrompt = backPrompt
        


# Display questions and let user select each one's answer with a single keypress.
def RunQuestions(question_list,options_list,win,message1,message2, name='Question', questionDur=float('inf'), isEndedByKeypress=True,respKeys=['1','2','3','4']):
    # set up
    nQuestions = len(question_list)
    allKeys = ['']*nQuestions
    trialClock = core.Clock()
    iQ = 0
    while iQ < nQuestions:
        print('iQ = %d/%d'%(iQ+1,nQuestions))
        # get response lists
        respText = "" # to be displayed to subject
#        respKeys = [] # allowable responses
        for iResp in range(0,len(options_list[iQ])):
            respText += '%d) %s\n'%((iResp+1),options_list[iQ][iResp])
#            respKeys += str(iResp+1)
        # set text
        message1.setText(question_list[iQ])
        message2.setText(respText)
        
        # draw question & answers
        message1.draw()
        message2.draw()
        
        #Flush the key buffer and mouse movements
        event.clearEvents()
        #Put the image on the screen
        win.logOnFlip(level=logging.EXP, msg='Display %s%d'%(name,iQ));
        win.flip()
        #Reset our clock to zero  - I think this call should take less time than window.flip, so resetting after the flip should be slightly more accurate.
        trialClock.reset()
        # Wait for keypress
        endQuestion = False;
        while (trialClock.getTime()<questionDur and not endQuestion):
            newKeys = event.getKeys(keyList=(respKeys + ['q','escape','backspace','period']),timeStamped=trialClock)
            for newKey in newKeys:
                # check for quit keys
                if newKey[0] in ['q', 'escape']:
                    endQuestion = True; # end the loop
                elif newKey[0] == 'backspace':
                    print('backspace')
                    iQ = max(0,iQ-1) # go back one
                    endQuestion = True;
                elif newKey[0] == 'period': 
                    iQ +=1 # skip fwd without recording response
                    endQuestion = True;
                else: # ok response keys 
                    iA = respKeys.index(newKey[0]) # convert from key to index in respKeys list
                    allKeys[iQ] = (iA+1, newKey[1]) # make new tuple with answer index and response time
                    # allKeys[iQ] = newKey
                    if isEndedByKeypress:
                        iQ +=1
                        endQuestion = True;
        
        if len(newKeys)>0 and newKey[0] in ['q', 'escape']: 
            break # end the loop
        elif (trialClock.getTime()>=questionDur):
            iQ += 1 # advance question
    # return result
    return allKeys


# Display questions and let the subject navigate selection up and down before selecting.
def RunQuestions_Move(question_list,options_list, win, name='Question', questionDur=float('inf'), isEndedByKeypress=True, upKey='up', downKey='down', selectKey='enter'):
    # set up
    nQuestions = len(question_list)
    allKeys = ['']*nQuestions
    trialClock = core.Clock()
    iQ = 0
    iA = 0
    respKeys=[upKey,downKey,selectKey]
    # make visuals
    from psychopy import visual
    questionText = visual.TextStim(win, pos=[0,+.5], wrapWidth=1.5, color='#000000', alignHoriz='center', name='questionText', text="aaa",units='norm')
    optionsText = []
    for iResp in range(0,len(options_list[0])):
        optionsText.append(visual.TextStim(win, pos=[0,-.1*iResp], wrapWidth=1.5, color='#000000', alignHoriz='center', name='option%d'%(iResp+1), text="aaa",units='norm',autoLog=False))
    
    while iQ < nQuestions:
        print('iQ = %d/%d'%(iQ+1,nQuestions))
        # default response is middle response (and round down)
        iA = int((len(options_list[iQ])-1)*0.5)
        # set and draw text
        questionText.setText(question_list[iQ])
        questionText.draw()
        optionsText[iA].bold = True # make currently selected answer bold
        for iResp in range(0,len(options_list[iQ])):
            optionsText[iResp].setText('%d) %s'%((iResp+1),options_list[iQ][iResp]))
            optionsText[iResp].draw()
                
        # Flush the key buffer and mouse movements
        event.clearEvents()
        # Put the image on the screen
        win.logOnFlip(level=logging.EXP, msg='Display %s%d'%(name,iQ));
        win.flip()
        # Reset our clock to zero  - I think this call should take less time than window.flip, so resetting after the flip should be slightly more accurate.
        trialClock.reset()
        # Wait for keypress
        endQuestion = False;
        while (trialClock.getTime()<questionDur and not endQuestion):
            newKeys = event.getKeys(keyList=(respKeys + ['q','escape','backspace','period']),timeStamped=trialClock)
            for newKey in newKeys:
                # check for quit keys
                if newKey[0] in ['q', 'escape']:
                    endQuestion = True; # end the loop
                elif newKey[0] == 'backspace':
                    print('backspace')
                    iQ = max(0,iQ-1) # go back one
                    endQuestion = True;
                elif newKey[0] == 'period': 
                    iQ +=1 # skip fwd without recording response
                    endQuestion = True;
                elif newKey[0] == upKey: # move response up
                    # remove old bold
                    optionsText[iA].bold = False
                    # update answer
                    iA -= 1
                    if iA<0:
                        iA=0
                    # make newly selected answer bold
                    optionsText[iA].bold = True
                    # redraw everything
                    questionText.draw()
                    for iResp in range(0,len(options_list[iQ])):
                        optionsText[iResp].draw()
                    win.flip()
                elif newKey[0] == downKey: # move response down
                    # remove old bold
                    optionsText[iA].bold = False
                    # update answer
                    iA += 1
                    if iA>=len(options_list[iQ]):
                        iA = len(options_list[iQ])-1
                    # make newly selected answer bold
                    optionsText[iA].bold = True
                    # redraw everything
                    questionText.draw()
                    for iResp in range(0,len(options_list[iQ])):
                        optionsText[iResp].draw()
                    win.flip()
                elif newKey[0] == selectKey:
                    # log response
                    allKeys[iQ] = (iA+1, newKey[1]) # make new tuple with answer index and response time
                    logging.log(level=logging.EXP, msg= 'Responded %d'%(iA+1))
                    # remove old bold
                    optionsText[iA].bold = False
                    # advance question index
                    iQ +=1
                    if isEndedByKeypress:
                        endQuestion = True;
                else:
                    print('pressed %s'%newKey[0])
        
        if len(newKeys)>0 and newKey[0] in ['q', 'escape']: 
            break # end the loop
    # return result
    return allKeys



# ===== DECLARE PROMPTS ===== %
def GetPrompts(experiment,promptType,params):
    
    if experiment == 'VidLecTask_dict.py':
        if promptType == 'Test':
            # declare default list of prompts
            topPrompts = ["You are about to watch a video of an academic lecture. Keep your eyes open and try to absorb as much of the material as you can.",
                "When the lecture is over, you'll be asked a few questions about it. Answer the questions using the number keys.", 
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the lecture, a question about your attention may appear. When this happens, answer the question within a few seconds using the number keys.",
                "Just before and after the lecture, a cross will appear. Look directly at the cross while it's on the screen."]
    
        elif promptType == 'Reverse':
            # prompts for BACKWARDS MOVIE:    
            topPrompts = ["You are about to watch a video of an academic lecture played backwards. Try to ignore it and think about something else.",
                "This is the LOW ATTENTION RUN: it's extremely important that you do NOT focus on the lecture during this run.",
                "Stay awake and keep your eyes open, but let your mind wander freely: try not to do any repetitive task like counting or replaying a song.", 
                "If at any time you notice that your mind hasn't been wandering as instructed, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
                "Sometimes during the lecture, a question about your attention may appear. When this happens, answer the question within a few seconds using the number keys.",
                "Just before and after the lecture, a cross will appear. Look directly at the cross while it's on the screen."]
                
        elif promptType == 'Wander':
            # prompts for LOW ATTENTION:    
            topPrompts = ["You are about to watch a video of an academic lecture. Try to ignore it and think about something else.",
                "This is the LOW ATTENTION RUN: it's extremely important that you do NOT focus on the lecture during this run.",
                "Stay awake and keep your eyes open, but let your mind wander freely: try not to do any repetitive task like counting or replaying a song.", 
                "When the lecture is over, you'll be asked a few questions about it. Answer the questions using the number keys.", 
                "If at any time you notice that your mind hasn't been wandering as instructed, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the lecture, a question about your attention may appear. When this happens, answer the question within a few seconds using the number keys.",
                "Just before and after the lecture, a cross will appear. Look directly at the cross while it's on the screen."]
        
        elif promptType == 'Attend':
            # prompts for HIGH ATTENTION
            topPrompts = ["You are about to watch a video of an academic lecture. Try to absorb as much of the material as you can.",
                "This is the HIGH ATTENTION RUN: it's extremely important that you pay close attention to the lecture during this run.",
                "When the lecture is over, you'll be asked a few questions about it. Answer the questions using the number keys.", 
                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the lecture, a question about your attention may appear. When this happens, answer the question within a few seconds using the number keys.",
                "Just before and after the lecture, a cross will appear. Look directly at the cross while it's on the screen."]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)
            
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."
            
    elif experiment == 'VidLecTask_vigilance.py':
        if promptType == 'Default':
            # declare default list of prompts
            topPrompts = ["You are about to watch a video of an academic lecture. Keep your eyes open and try to absorb as much of the material as you can.",
                "When the lecture is over, you'll be asked a few questions about it. Answer the questions using the number keys.", 
                "During the lecture, a %s dot will display in the middle of the screen. Look at the dot for the duration of the lecture. When the dot turns %s, press the %c key with your right index finger."%(params['dotColor'],params['targetColor'],params['respKey'].upper()),
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the lecture, a question about your attention may appear. When this happens, answer the question within a few seconds using the number keys.",
                "Just before and after the lecture, a cross will appear. Look directly at the cross while it's on the screen."]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)
            
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."
        
        
    elif experiment.startswith('ReadingTask') or experiment.startswith('ReadingImageTask_eyelink') or experiment.startswith('DistractionTask'):
        if promptType == 'Test':
            # declare default list of prompts
            topPrompts = ["You are about to read the transcript of an academic lecture. Try to absorb as much of the material as you can.",
                "Press the '%s' key to advance to the next page. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']), 
                "When the reading is over, you'll be asked a few questions about it. Answer the questions using the number keys.", 
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the reading, a question about your attention may appear. When this happens, answer the question within a few seconds using the number keys.",
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen."]
        elif promptType == 'Read':
            topPrompts = ["You are about to read the transcript of an academic lecture. Try to absorb as much of the material as you can.",
                "When the session is over, you'll be asked a few questions about the material.", 
#                "You will have %.1f seconds to read each page. When the text starts to fade, that time is almost up."%(params['maxPageTime']), 
                "Press the '%s' key to advance to the next page. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']), 
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the reading, a question about your attention may appear. When this happens, answer the question within a few seconds using the number keys.",
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen."]
        elif promptType == 'AttendReading':
            topPrompts = ["You are about to read the transcript of an academic lecture. At the same time, you will hear audio from a different lecture.",
                "When the session is over, you'll be asked a few questions about the reading. Questions about the audio will happen at the end of all the sessions.",
#                "You will have %.1f seconds to read each page. When the text starts to fade, that time is almost up."%(params['maxPageTime']), 
                "Try to read top to bottom without skipping forward or back. Read as quickly as you can while still absorbing the material.",
                "When you're done reading a page, press the '%s' key to advance to the next one. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']), 
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the reading, a question about your attention may appear. When this happens, answer the question using the number keys.",
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen.",
                "In this session, pay attention to ONLY the reading and IGNORE the audio."]
        elif promptType == 'AttendReadingFirst':
            topPrompts = ["You are about to read the transcript of an academic lecture. At the same time, you will hear audio from a different lecture.",
                "When the session is over, you'll be asked a few questions about the reading and audio.",
                "Try to read top to bottom without skipping forward or back. Read as quickly as you can while still absorbing the material.",
                "When you're done reading a page, press the '%s' key to advance to the next one. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']), 
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen.",
                "For the first part of this session, pay attention to ONLY the reading and IGNORE the audio."]
        elif promptType == 'AttendReading_short':
            topPrompts = ["In this session, pay attention to ONLY the reading and IGNORE the audio."]
        elif promptType == 'AttendReadingFirst_short':
            topPrompts = ["For the first part of this session, pay attention to ONLY the reading and IGNORE the audio."]
        elif promptType == 'AttendReading_switch':
            topPrompts = ["For the rest of the session, pay attention to ONLY the reading and IGNORE the audio."]        
        elif promptType == 'AttendBoth':
            topPrompts = ["You are about to read the transcript of an academic lecture. At the same time, you will hear audio from a different lecture.",
                "When the session is over, you'll be asked a few questions about the reading. Questions about the audio will happen at the end of all the sessions.", 
#                "You will have %.1f seconds to read each page. When the text starts to fade, that time is almost up."%(params['maxPageTime']), 
                "Try to read top to bottom without skipping forward or back. Read as quickly as you can while still absorbing the material.",
                "When you're done reading a page, press the '%s' key to advance to the next one. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']),  
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the reading, a question about your attention may appear. When this happens, answer the question using the number keys.",
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen.",
                "In this session, pay attention to BOTH the reading AND the audio."]
        elif promptType == 'AttendBothFirst':
            topPrompts = ["You are about to read the transcript of an academic lecture. At the same time, you will hear audio from a different lecture.",
                "When the session is over, you'll be asked a few questions about the reading and audio.", 
                "Try to read top to bottom without skipping forward or back. Read as quickly as you can while still absorbing the material.",
                "When you're done reading a page, press the '%s' key to advance to the next one. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']),  
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen.",
                "For the first part of this session, pay attention to BOTH the reading AND the audio."]
        elif promptType == 'AttendBoth_short':
            topPrompts = ["In this session, pay attention to BOTH the reading AND the audio."]
        elif promptType == 'AttendBothFirst_short':
            topPrompts = ["For the first part of this session, pay attention to BOTH the reading AND the audio."]
        elif promptType == 'AttendBoth_switch':
            topPrompts = ["For the rest of the session, pay attention to BOTH the reading AND the audio."]
        elif promptType == 'AttendLeft':
            topPrompts = ["You are about to read the transcript of an academic lecture. At the same time, you will sometimes hear audio from a different lecture.",
                "On some trials, a lecture will play in only your left ear. On other trials, a DIFFERENT lecture will play in only your right ear.",
                "Only the reading and the LEFT ear lecture are important. When the audio is in your LEFT ear, try to absorb as much of BOTH the reading AND audio material as you can.", 
                "When the audio is in your RIGHT ear, IGNORE the audio and just absorb the reading.",
                "When the session is over, you'll be asked a few questions about the reading. Questions about the audio will happen at the end of all the sessions.", 
#                "You will have %.1f seconds to read each page. When the text starts to fade, that time is almost up."%(params['maxPageTime']), 
                "Press the '%s' key to advance to the next page. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']), 
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the reading, a question about your attention may appear. When this happens, answer the question using the number keys.",
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen."]
        elif promptType == 'AttendRight':
            topPrompts = ["You are about to read the transcript of an academic lecture. At the same time, you will sometimes hear audio from a different lecture.",
                "On some trials, a lecture will play in only your right ear. On other trials, a DIFFERENT lecture will play in only your left ear.",
                "Only the reading and the RIGHT ear lecture are important. When the audio is in your RIGHT ear, try to absorb as much of BOTH the reading AND audio material as you can.",
                "When the audio is in your LEFT ear, IGNORE the audio and just absorb the reading.",
                "When the session is over, you'll be asked a few questions about the reading. Questions about the audio will happen at the end of all the sessions.", 
#                "You will have %.1f seconds to read each page. When the text starts to fade, that time is almost up."%(params['maxPageTime']), 
                "Press the '%s' key to advance to the next page. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']), 
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the reading, a question about your attention may appear. When this happens, answer the question using the number keys.",
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen."]
        elif promptType == 'AttendForward':
            topPrompts = ["You are about to read the transcript of an academic lecture. At the same time, you will sometimes hear audio from a different lecture.",
                "On some trials, a lecture will play forward. On other trials, the lecture will play backward.",
                "Only the reading and the forward lecture are important. When the audio playing FORWARD, try to absorb as much of BOTH the reading AND audio material as you can.",
                "When the audio is playing BACKWARD, IGNORE the audio and just absorb the reading.",
                "When the session is over, you'll be asked a few questions about the reading. Questions about the audio will happen at the end of all the sessions.", 
#                "You will have %.1f seconds to read each page. When the text starts to fade, that time is almost up."%(params['maxPageTime']), 
                "Press the '%s' key to advance to the next page. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']), 
#                "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%params['wanderKey'].upper(),
#                "Sometimes during the reading, a question about your attention may appear. When this happens, answer the question using the number keys.",
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen."]
        elif promptType == 'TestReading':
            topPrompts = ["You will now be asked a few questions about the text you just read. Answer using the number keys.",
                "There's no time limit on each question, but try to answer in a reasonable amount of time.",
                "If you don't know the answer, take your best guess."]
        elif promptType == 'TestReading_box':
            topPrompts = ["You will now be asked a few questions about the text you just read. Answer using the button box.",
                "There's no time limit on each question, but try to answer in a reasonable amount of time.",
                "If you don't know the answer, take your best guess."]
        elif promptType == 'TestBoth':
            topPrompts = ["You will now be asked a few questions about the lectures you just read and heard. Answer using the number keys.",
                "Some questions may be on material you were asked to ignore. Please try to answer anyway. If you don't know the answer, take your best guess.",
                "There's no time limit on each question, but try to answer in a reasonable amount of time."]
        elif promptType == 'Practice':
            topPrompts = ["You are about to read the transcript of an academic lecture. Try to absorb as much of the material as you can.",
#                "Press the '%s' key to advance to the next page. If you don't advance within %.1f seconds, it will advance automatically. If the text starts to fade, that time is almost up."%(params['pageKey'].upper(),params['maxPageTime']), 
                "Try to read top to bottom without skipping forward or back. Read as quickly as you can while still absorbing the material.", 
                "This session is just practice. When you're done reading a page, press the '%s' key to advance to the next one."%(params['pageKey'].upper()), 
                "Between pages, a cross will appear. Look directly at the cross while it's on the screen."]
        elif promptType == 'None':
            topPrompts = []
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)
                
        # declare bottom prompts
        if promptType == 'None':
            bottomPrompts = []
        else:
            bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
            bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."
        
    elif experiment.startswith('ReadingTask_questions'):
        if promptType == 'Test':
            # declare default list of prompts
            topPrompts = ["You will now be asked a few questions about the text you just read. Answer using the number keys.",
                "There's no time limit on each question, but try to answer in a reasonable amount of time.",
                "If you don't know the answer, take your best guess."]
        elif promptType == 'TestBoth':
            # declare prompts for questions on both reading and audio.
            topPrompts = ["You will now be asked a few questions about the lectures you just read and heard. Answer using the number keys.",
                "Some questions may be on material you were asked to ignore. Please try to answer anyway. If you don't know the answer, take your best guess.",
                "There's no time limit on each question, but try to answer in a reasonable amount of time."]
        elif promptType == 'TestSound':
            # declare prompts for questions on audio.
            topPrompts = ["You will now be asked a few questions about the lecture you just heard. Answer using the number keys.",
                "Some questions may be on material you didn't hear or were asked to ignore. Please try to answer anyway. If you don't know the answer, take your best guess.",
                "There's no time limit on each question, but try to answer in a reasonable amount of time."]
        elif promptType == 'TestSound_box':
            # declare prompts for questions on audio.
            topPrompts = ["You will now be asked a few questions about the lecture you just heard. Answer using the button box.",
                "Some questions may be on material you didn't hear or were asked to ignore. Please try to answer anyway. If you don't know the answer, take your best guess.",
                "There's no time limit on each question, but try to answer in a reasonable amount of time."]            
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)
                
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."
        
    elif experiment.startswith('ColorVigilanceTask'):
        if promptType == 'Default':
            # declare default list of prompts
            topPrompts = ["During this task, a %s dot will display in the middle of the screen. Look at the dot for the duration of the task. When the dot turns %s, press the %c key with your right index finger."%(params['dotColor'],params['targetColor'],params['respKey'].upper()),
                "Just before and after each block of trials, a cross will appear. Look directly at the cross while it's on the screen."]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)
                
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."
        
    elif experiment.startswith('SingingTask'):
        if promptType == 'Default':
            # declare default list of prompts
            topPrompts = ["During this task, you will be asked to perform scales, speak, or sing while keeping your head still.",
                "Just before each exercise, a cross will appear. Look directly at the cross while it's on the screen.",
                "Before each of these trials, you will see a brief countdown. Please start the scale/speech/song when it reaches 0.",
                "Once you've started, use the change in numbers as your beat. Stop when the count is over and the cross reappears."]
        elif promptType == 'CountImagineSing':
            # declare default list of prompts
            topPrompts = ["During this task, you will be asked to COUNT along with the beat, IMAGINE singing, or SING while keeping your head still.",
                "Just before each exercise, a cross will appear. Look directly at the cross while it's on the screen.",
                "Before each of these exercise, you will see a brief countdown. Please start the exercise when it reaches 0.",
                "Once you've started, use the change in numbers as your beat. Stop when the count is over and the cross reappears."]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)
                
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."
        
    elif experiment.startswith('AuditorySequenceTask'):
        if promptType == 'Default':
            # declare default list of prompts
            topPrompts = ["During this task, you will see a fixation cross that changes colors.Look directly at the cross while it's on the screen.",
                "On each trial, you will feel two sequences of taps on your fingers. After the second sequence, the cross will turn yellow.",
                "When the cross turns yellow, press %s if the two sequences were the same and %s if they were different."%(params['respKeys'][0],params['respKeys'][1]) ]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)
                
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."    
    
    elif experiment.startswith('MultiTaskAvWithCheckerboard'):
        if promptType == 'Default':
            # declare default list of prompts
            topPrompts = ["During this task, you will see a fixation cross, words, and checkerboard patterns. Look directly at the center of the screen during the whole run.",
                "You will also hear sounds. A cue before each block will tell you whether you should respond to the sounds or the written words, and how you should respond.",
                "Respond AS QUICKLY AS POSSIBLE to the words or sounds according to what the cue asks you to do."]
        elif promptType == 'Long':
            # declare default list of prompts
            topPrompts = ["During this task, you will see a fixation cross, words, and checkerboard patterns. Keep your eyes open and look directly at the center of the screen during the whole run.",
                "You will also hear sounds. A cue before each block will tell you whether you should respond to the sounds or the written words, and how you should respond.",
                "'Visual: Button' indicates that you should press a button as soon as you see the fixation cross change into something else. Ignore the checkerboards and sounds.",
                "'Visual: Add' indicates that you should mentally add all the numbers you see. Keep track in your head until the end of the block, when you will be asked for your count. Ignore the checkerboards and sounds and avoid moving.",
                "'Audio: Button' indicates that you should press a button as soon as you hear speech. Ignore the checkerboards and text visuals.",
                "'Audio: Add' indicates that you should mentally add all the numbers you hear. Keep track in your head until the end of the block, when you will be asked for your count. Ignore the checkerboards and text visuals and avoid moving.",
                "'Rest' indicates that you should ignore all visual and auditory stimuli and think about other things during the block.",
                "Respond AS QUICKLY AS POSSIBLE to the words or sounds according to what the cue asks you to do."]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)
                
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."    
        
    elif experiment.startswith('MovieTask'):
        if promptType == 'Test':
            # declare default list of prompts
            topPrompts = ["You are about to watch a movie. Keep your eyes open and try to absorb as much of the movie as you can.",
                "When the movie is over, you'll be asked a few questions about it. Answer the questions using the number keys.", 
                "Just before and after the movie, a cross will appear. Look directly at the cross while it's on the screen."]
        elif promptType == 'Watch':
            topPrompts = ["You are about to watch a movie. Keep your eyes open and try to absorb as much of the movie as you can.",
                "Just before and after the movie, a cross will appear. Look directly at the cross while it's on the screen."]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)        
        
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."            
    
    elif experiment.startswith('AuditorySpeedReadingTask'):
        if promptType == 'Default':
            # declare default list of prompts
            topPrompts = ["In this run, you will hear a voice reading text. Try to absorb as much of the reading as you can.",
                "When the reading is over, you'll be asked a few questions about it. Answer the questions using the button box.", 
                "Throughout the whole run, a cross will appear. Look directly at the cross while it's on the screen."]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)        
        
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."            
    elif experiment.startswith('VisualSpeedReadingTask'):
        if promptType == 'Default':
            # declare default list of prompts
            topPrompts = ["In this run, you will see text flashed in front of you. Try to absorb as much of the reading as you can.",
                "When the reading is over, you'll be asked a few questions about it. Answer the questions using the button box.", 
                "Between blocks of text, a cross will appear. Look directly at the cross while it's on the screen."]
        else:
            raise Exception('Prompt Type %s not recognized!'%promptType)        
        
        # declare bottom prompts
        bottomPrompts = ["Press any key to continue."]*len(topPrompts) # initialize
        bottomPrompts[-1] = "WHEN YOU'RE READY TO BEGIN, press any key."            
    else:
        raise Exception('Experiment %s not recognized!'%experiment)    
    
    # return the prompts
    return (topPrompts,bottomPrompts)
