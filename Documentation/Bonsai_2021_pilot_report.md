# Bonsai: A report toward integrating into our behavioral pipeline

## Introduction: 

### Description of Bonsai

![Bonsai Logo](Images/bonsai-lettering.svg)![Allen Logo](Images/AllenInstitute_Logo_RGB.png =100x20)

<img src="Images/AllenInstitute_Logo_RGB.png" alt=" height="100" />

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
    - Ability to run a simple detection of change behavior with fixed change probability and only one natural image associated with go and no go trials.  
    - We will assess the feasibility of concatenating scripts  
        We should be able to run an experiment build from multiple scripts. 
        e.g. Experiment 1  
        - Run static gratings
        - Run Sparse Noise
        - Run a go/No go exp 

##### Pipeline integration capabilities 
  - Bonsai should be compatible with our behavior hardware (lick spouts, running wheels, etc.) and our hardware control packages (such as daqmx)  
  - We should be able to make a portable hardware configuration using Bonsai. 
  - We should evaluate how hardware configuration parameters will be saved (port number and device address for instance).  
  - Scripts should be able to reference input/output components by an informative name (for instance, lick_line_status or reward_siganl, not NI device 1, input 0.)  
  - We need to start scripts from wse/mouse director 
  - We need to be able to poll for status (15 or 20 things) 
  - We need Bonsai to publish stats along the way (to accumulator) 
 
##### Performance evaluation 
  - Performance levels (in terms of temporal precision) should be compatible with behavior experiments, including visual stimulus presentation 
  - We should check that BonVision’s stimulus warping functions properly as documented in BonVision’s documentation and warping does not impair display performance beyond our QC criteria. 
 
## Methods

### Description of test rig developed for Bonsai

For this effort,  we built a testing rig at the Institute allowing scientific teams to submit integration tests of their Bonsai workflow with a reasonable duplicate of the pipeline hardware.  

QUINN

### Description of tests ran with Bonsai

JEROME

<br/>

## Results 

### Qualitative decription of tests ran with Bonsai

### Performance of tests ran with Bonsai

#### Screen stimulation stability

#### Sync lines output stability


## Discussion

### Components to develop and integrate

### Proposal strategy 

### Standardizing behavioral data storage

### Timeline

### Bonsai state of documentation

### Available resources for Bonsai developments

### Community engagement and Ecosystem support

## Conclusion
