# PsychopyExamples

This repository is designed to assist Hanyang University students (2023-2). 

# Dependency 

This repository sources depend on psychopy library.

## Psychopy installation guideline

### Windows

To run codes, You have to install psychopy library in your computer. I recommend to install psychopy library using conda environment. If you are not familiar with anaconda, please read this article (https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).

After download this repository, Please open the anaconda command line prompt(or terminal) and go to the this repository path. 

Enter this command in the anaconda command line prompt(or terminal).
```bash
conda env create -n psychopy -f psychopy-env.yml
```
The previous command would take much time. Please be patient (In my case, It took 15 minutes). After completed the command, enter following command in your prompt. If there is no error, the configuration is fully installed.

```bash
conda activate psychopy
```

References 
- https://www.psychopy.org/download.html

### Mac (intel)

Please open terminal and run the following lines.

```bash
brew install portaudio

conda create -n psychopy python=3.8
pip install psychopy==2021.2.3
pip install pygame==2.1.2
pip install pyo==1.0.4
pip install websocket-client==1.2.1
pip install screeninfo==0.7
```

### Mac (Apple Silicon) ex: M1

Please refer to this document.

https://github.com/waltervanheuven/psychopy-on-M1/blob/main/v2023.2.3.md

## Running an experiment code

Open the terminal and activate conda environment for psychopy.

```bash
conda activate psychopy
```

Go to the source which you want to run and execute experiment code like following line.

```bash
(psychopy) C:\Users\USER\Desktop\PsychopyExamples\ExperimentSources\Visual\Memory> python ./FourLetterTask.py
```

# File structures

## ExperimentSources

There are various kinds of experiment source implemented by psychopy library in ExperimentSources directory. In the sub-directory of the ExperimentSources, I divided experiment sources using type of stimuli, one is visual, the other is auditory. After that, task names follow type of stimuli. Finally, You will see the sources of each experiment.

- Audio
  - Attention
      - AuditorySartTask: Implement an audio version of the SART (sustained attention response task) described in Seli 2011 (doi:10.1037/a0025111)
  - Inference
      - BopItTask: Audio-behavior association task based on the game BopIt.
  - Memory
      - LearnNonsenseWorks: Play pairs of nonsense words, then display one and the subject must recall the other (multiple-choice questions)
  - Motor
      - AuditorySequenceTask: Experiment with inputting sequences corresponding to audio
  - Psychometric
      - GetPerceptualThreshold/ThresholdToneDetection(_2AFC): use staircasing to find a subject’s audio volume threshold, then periodically play tones near that threshold. _2AFC indicates a 2-alternative forced choice version of this task
  - QA
      - AudioInsterspersedQuestions: Question (Sound) – Answer – Question (Sound) are repeated experiment
      - PlaySoundsWithQuestions: After playing a certain audio file, ask a question
- Visual
  -  Attention
      - ColorVigilanceTask: Simple visual vigilance task where a central fixation dot changes color at random intervals.
      - FlankerTask: Implement the Erikson Flanker Task described in Eichele 2008 (doi: 10.1073/pnas.0708965105)
      - GoNoGoTask_d1
      - LocalGlobalAttention: Implements the local-global attention task as described in Weissman, Nature Neurosci. 2006 (doi: 10.1038/nn1727)
      - NumericalSartTask: Implement the modified SART (sustained attention response task) described in Morrison 2014 (doi: 10.3389/fnhum.2013.00897)
  -  Interference
      - LetterOrderTask_d1/_(d2)/_(d3): Perform two tasks alternately (Remember, Alphabetize).
  -  Memory
      - FourLetterTask: Implement a visuospatial working memory task described in Mason et al., Science 2007 (doi: 10.1126/science.1131295)
  -  Motor
      - SequenceLearningTask: Implement a sequence learning task described in Mason et al., Science 2007 (doi: 10.1126/science.1131295)
        
## Datas

After running codes, the results of experiment will be recorded in the directory. 

## GeneralTools

This directory includes multiple utility sources to run experiments.

# Checked Configuration

Windows 10 (builder version: 22H2)
- python: 3.8.18
- psychopy: 2022.2.5

Mac (version: 12.6.8)
- python: 3.8.11
- psychopy: 2021.2.3

# License

These sources are adapted from David Jangraw's repository (https://github.com/djangraw/PsychoPyParadigms)


