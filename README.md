# PsychopyExamples

This repository is designed to assist Hanyang University students in creating experimental sources (2023-2). 

# Dependency 

The sources of this repository depends on psychopy library.

## Installation guideline of psychopy

To run codes, You have to install psychopy library in your computer. I recommend to install psychopy library using conda environment. 

References 
- https://www.psychopy.org/download.html

## Checked Configuration

Windows 10 (builder version: 22H2)
- python: 3.8.18
- psychopy: 2022.2.5

Mac (version: 12.6.8)
- python: 
- psychopy: 

# File structures

## ExperimentSources

There are various kinds of experiment source implemented by psychopy library in ExperimentSources directory. In the sub-directory of the ExperimentSources, I divided experiment sources using type of stimuli, one is visual, the other is auditory. After that, task names follow type of stimuli. Finally, You will see the sources of each experiment.

- Audio
  - Attention
      - AuditorySartTask
  - Inference
      - BopItTask
  - Memory
      - LearnNonsenseWorks
  - Motor
      - AuditorySequenceTask
  - Psychometric
      - GetPerceptualThreshold
      - ThresholdToneDetection
      - ThresholdToneDetection_2AFC
  - QA
      - AudioInsterspersedQuestions
      - PlaySoundsWithQuestions
- Visual
  -  Attention
      - ColorVigilanceTask
      - FlankerTask
      - GoNoGoTask_d1
      - LocalGlobalAttention
      - NumericalSartTask
  -  Interference
      - LetterOrderTask_d1
      - LetterOrderTask_d2
      - LetterOrderTask_d3
  -  Memory
      - FourLetterTask
  -  Motor
      - SequenceLearningTask
        
## Datas

After running codes, the result of experiment is recorded in the directory. 

# Origin

These sources are adapted from David Jangraw's repository (https://github.com/djangraw/PsychoPyParadigms)


