# Bonsai + Allen : A report toward integrating Bonsai into our behavioral pipeline

<img src="https://raw.githubusercontent.com/AllenInstitute/bonsai_workflows/master/Documentation/Images/bonsai-lettering.svg?token=AATAHT4TLCQWUH54YLGGACDAT3QKU" height="100" /><img src="https://raw.githubusercontent.com/AllenInstitute/bonsai_workflows/master/Documentation/Images/AllenInstitute_Logo_RGB.png?token=AATAHTYYP47RH4KTUQBIBEDAT3QBQ" height="100" />

## Introduction: 

### Description of Bonsai

Bonsai (https://bonsai-rx.org) is an open-source visual programming language for controlling systems neuroscience experiments. The logic of each experiment is specified by a Bonsai “workflow” file, which defines how diverse input and output signals are coordinated in time. The BonVision package includes workflow nodes for generating visual stimuli and presenting them with high temporal fidelity. Additional packages provide interfaces to NI hardware, Arduinos, and other DAQ hardware. This makes it possible to replicate the majority of Camstim functionality using existing Bonsai packages.

### Goal of this effort

This document details ongoing requirements and efforts to support the piloting and testing of Bonsai as part of the Allen Brain Observatory pipeline. We assess here whether and how Bonsai can replace Camstim for controlling both passive and active behavior experiments. Bonsai would update visual (or other) stimuli in response to lick and running wheel input, and would need to operate in conjunction with existing software packages, such as WSE, Sync, and Videomon. 

#### Design principles 
Behavioral task designs will be specified as Bonsai workflow files  (.bonsai). These files will be provided by each internal or external scientific team. Hardware components of the pipeline will be integrated with existing Bonsai modules and (if necessary) with custom Bonsai packages written in C#. Commonly used stimulus types can be saved as reusable workflow elements that can be shared by multiple scientific teams. Each package will have a deployed and testing mode, allowing individual packages to emulate normal functions on the experimental rig when the hardware is not available. 

####  Sub-parts of the evaluation 
##### Behavior capabilities  
We will check that Bonsai is sufficient to cover our desired range of behavior use cases with a simple/limited set of test cases: 
  - Passively viewing visual stimuli 
    - Ability to display static and drifting gratings 
    - Ability to display natural images and movies 
  - Active behavior 
    - Ability to run a simple go/no go task with only one natural image associated with go and no go trials and fixed trial probabilities. 
    - Ability to run a simple detection of change behavior with fixed change probability.  
    - We will assess the feasibility of concatenating scripts  
        We should be able to run an experiment build from multiple scripts. 
        e.g. Experiment 1  
        - Run static gratings stimuli.
        - Run Sparse Noise stimuli.
        - Run a Go/No Go experiment.

##### Pipeline integration capabilities 
  - Bonsai should be compatible with our behavior hardware (lick spouts, running wheels, etc.) and our hardware control packages (such as daqmx)  
  - We should be able to make a portable hardware configuration using Bonsai. 
  - We should evaluate how hardware configuration parameters will be saved (port number and device address for instance).  
  - Scripts should be able to reference input/output components by an informative name (for instance, lick_line_status or reward_signal, not NI device 1, input 0.)  
  - We need to start scripts from wse/mouse director 
  - We need to be able to poll for status (15 or 20 things) 
  - We need Bonsai to publish stats along the way (to accumulator) 
 
##### Performance evaluation 
  - Performance levels (in terms of temporal precision) should be compatible with behavior experiments, including visual stimulus presentation 
  - We should check that BonVision’s stimulus warping functions properly as documented in BonVision’s documentation and warping does not impair display performance beyond our QC criteria. 
 
## Methods:

### Description of test rig developed for Bonsai

For this effort,  we built a testing rig at the Institute allowing scientific teams to submit integration tests of their Bonsai workflow with a reasonable duplicate of the pipeline hardware.  


QUINN
- Sync lines installed and used in this study
![image](https://user-images.githubusercontent.com/2491343/117510054-36f92f00-af40-11eb-80b3-26ce6f71b309.png)

### Description of tests ran with Bonsai

JEROME

<br/>

## Results:

### Qualitative description of tests ran with Bonsai

### Performance of tests ran with Bonsai

#### Passively viewing experiments

- Screen stimulation stability

- Sync lines output stability

- To validate our measure of performance and push Bonsai over its limit, we reproduced a performance quantification published along the BonVision paper (Lopes 2020). For that end, we [modified a workflow](https://github.com/AllenInstitute/bonsai_workflows/blob/master/GridGratingDrawing/gabor.bonsai) displaying an increasingly large number of elements. A reference figure was published in the original BonVision publication and is shared below for ease of comparision

![Goncalo_2020_figure](https://user-images.githubusercontent.com/2491343/118040614-9da69000-b326-11eb-8c9e-2cfac2789695.png)

*Quantification of frame update period (Bottom) to display an array of drifting gratings (Top). Reproduced from (Lopes 2020)*

In this test, Bonvision is tasked to display a very large number of drifting gratings in an array pattern. We replicated the code, utilizing our photodiode circuit to measure the rising time of requested stimuli updates. The associated analysis is [available on this notebook](https://github.com/AllenInstitute/bonsai_workflows/blob/master/Analysis/GridGratingDrawing/2021-05-12-GridGratingDrawing.ipynb). 
Our replicated figure below is faithful to the original published publication, ie. approximately 1000 grating elements are necessary to start impacting performances of Bonsai. 

![Reproduction of performance](https://github.com/AllenInstitute/bonsai_workflows/raw/5c2ca01a6aa2fc1ed2cd8f2b163699910efb6328/Analysis/GridGratingDrawing/2021-05-12-BonVision_grating_replication.png).

*Quantification of frame update period to display an array of drifting gratings using the same workflow from (Lopes 2020) but on an Allen Institute stimulus test rig.* 


#### Go/No task

- Screen stimulation stability

- Sync lines output stability

#### Detection of change task

- Screen stimulation stability

- Sync lines output stability

#### Close-loop experiment: Ability to concurrently load and save camera data while running detection of change on the same computer.

A key promise of Bonsai is its ability to quickly integrate multiple data modalities in a single data workflow. For example, measuring key behavioral parameters from a continuous stream of frames from a behavior camera would allow closed-loop experiments. While we do not anticipate this immediate use-case for the OpenScope project, this is a key property of Bonsai as [DeepLabCut modules](https://github.com/bonsai-rx/deeplabcut) have been fully integrated into Bonsai. To evaluate this capability, we measured the impact of continuously acquiring and saving an additional webcam, while running the detection of change task. The workflow for this experiemnt is [available here](https://github.com/AllenInstitute/bonsai_workflows/blob/master/DetectionOfChange/DetectionOfChange_with_hardware_and_camera.bonsai).  

- Screen stimulation stability

- Sync lines output stability


#### Tasks concatenation

- Screen stimulation stability

- Sync lines output stability


#### Bonsai available capabilities to be used for integration

- Describe here the capabilties that are already available 
- MORE DETAILS HERE

#### Bonsai missing capabilities to be used for integration

- Describe here the capabilties that are needed for integration 
- MORE DETAILS HERE

## Discussion:

### General discussion on hardware integration

Describe the good and bads.

### Lessons learned on using Bonsai for coding behavioral experiments

- Feedbacks on coding behavioral experiments in Bonsai
- Migrating from Python to Bonsai...
- Need for documentation
- MORE DETAILS HERE

### General discussion on performance

Describe the good and bads of performance. 

### Components to develop and integrate

### Proposed strategy 
Migrating Bonsai to be used in the Allen Brain Observatory pipelines will be a multi-component process that will be better tackled in distinct phases. This will allow to avoid accelerated integration timelines and an efficient development.

#### Phase 0 : Bonsai pilot + Report + Build plan
The purpose and content of this report. 

#### Phase 1 : Single rig integration
  - Work out the need of running Bonsai during one session. 
  - Integration with WSE and hardware.
  - Saving data.
  - MORE DETAILS HERE

#### Phase 2 : Cluster integration
  - Interaction with BehaviorMon.
  - mTrain integration.
  - WaterLog test and integration.
  - MORE DETAILS HERE

#### Phase 3 : Testing integration
  - Testing at scale with mice trained through the pipeline with a previously validated and known behavior. 
  - Catch and fix integration issues
  - MORE DETAILS HERE

### Standardizing behavioral data storage

Describe the use of sync lines and h5 sync file as standardized event recordings. Describe the advantage comparing to NWB event storage scheme.

### Timeline

### Community engagement and Ecosystem support

### Potential synergies with AIX-2, IBL

## Conclusion:

## References:

1.	Lopes, G. et al. Bonsai: an event-based framework for processing and controlling data streams. Front. Neuroinform. 9, 7 (2015). 
2.	Lopes, G. et al. BonVision – an open-source software to create and control visual environments. doi:10.1101/2020.03.09.983775. 

## Useful resources:
- Cajal courses: 
https://neurogears.org/vrp-2021/
- BonVision live coding Session: 
https://www.youtube.com/watch?v=3qyHzXBx0dE
- Bonsai workflow descriptions on confluence : 
http://confluence.corp.alleninstitute.org/display/CP/Bonsai+Demos
- Collection of Bonsai repositories (37 repos on January 25th 2021).  
https://github.com/bonsai-rx 
- Primary documentation site
https://bonsai-rx.org/docs
- BonVision documentation
https://bonvision.github.io/
- International Brain Laboratory (IBL) hardware lines interface with Bonsai repository 
https://github.com/harp-tech/IBL_behavior_control 
- Benchmark repository used in Bonvision preprint 
https://github.com/bonvision/benchmarks 
- Bonsai workshop with lots of introductory material for visual tasks 
https://neurogears.org/vrp-2021/ 
- Bonsai google forum
https://groups.google.com/d/forum/bonsai-users


