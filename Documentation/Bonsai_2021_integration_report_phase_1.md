# Bonsai + Allen : Bonsai Integration plan and report into our behavioral rigs (Phase 1)

<img src="Images/bonsai-lettering.svg?token=AATAHT4TLCQWUH54YLGGACDAT3QKU" height="100" />
<img src="Images/AllenInstitute_Logo_RGB.png?token=AATAHTYYP47RH4KTUQBIBEDAT3QBQ" height="100" />

---

## Highlights

* TBA
---

## Introduction 

### What is Bonsai?

[Bonsai](https://bonsai-rx.org) is an open-source visual programming language for controlling systems neuroscience experiments. The logic of each experiment is specified by a Bonsai “workflow” file, which defines how diverse input and output signals are coordinated in time. The [BonVision](https://bonvision.github.io/) package includes workflow nodes for generating visual stimuli and presenting them with high temporal fidelity. Additional packages provide interfaces to NI hardware, Arduinos, and other data acquisition devices. This makes it feasible to replicate the functionality of Camstim, the MindScope Program's PsychoPy-based behavioral control software, using existing Bonsai packages.

### Why switch to Bonsai?

There are several reasons why Bonsai may be an attractive alternative to Camstim:

* Bonsai is an open-source project with a relatively large user base. If external scientists want to replicate our stimuli or behavioral paradigms, it's easier to share a .bonsai file that specifies the task logic than to release and support a complex Python package. If our rigs are Bonsai-compatible, it also makes it easier for others to submit new tasks to be run on them (e.g., for OpenScope).

* Many experiments run with Camstim suffer from dropped frames, inconsistent frame intervals, or other stimulus-related irregularities. At least according to the published benchmarks, Bonsai could help us avoid these problems.

* The lack of standardized software for defining rodent behavioral tasks is a huge impediment to progress in neuroscience. Bonsai is the software that is best-positioned to become this standard, and this seems like something worth supporting.

### Overall strategy 

Migrating Bonsai to be used in the Allen Brain Observatory pipelines will be a multi-component process that should be tackled in distinct phases. This will allow us to avoid accelerated integration timelines and an efficient development. Importantly, our system should be backward compatible: Hardware and software should be functional with both camstim and bonsai-based system. Based our our pilot, we outline below the required developments and organized them into rationalized deployment phases. 

#### **Phase 0 :** Bonsai pilot + Report + Build plan
The purpose and content of this report.

#### **Phase 1 :** Single rig integration
The goal of this phase is to develop all component required to running Bonsai during one session. 
  - Saving data. We will determine output file formats in agreement with key stakeholders. 
  - Add the ability to start a Bonsai stimulus session from the WSE
  - Add messaging from Bonsai so it can return status to the WSE
    - Ready, displaying stimulus, stimulus completed (with completion codes)
  - Add capability to Bonsai so it can push stimulus status messages to the BehaviorMon service
    - Session started, encoder count, rewards issued, passes, fails etc.  
  - Generate template workflows for a variety of stimuli.
  - System to manage binary dependencies of stimuli.
  - Interaction with BehaviorMon.
  - Additional Hardware Interfaces:
    - Implement DAQ digital input
    - Enhanced encoder
  - Finalize faithful replicate of the detection of change task with a bonsai workflow (trial logic, abort logic,...): This will be our key test bench workflow. 

#### **Phase 2 :** Cluster integration
The goal of this phase is to develop all external dependencies and implement full pipeline integration (data processing anda analysis). In particular, this step is meant to handle our legacy dependency on pkl files. 
  - mTrain integration.
    - WSE interacts with mTrain to determine which stimulus should be delivered to each mouse.  Bonsai ‘integration’ with mTrain is required only if automatic determination of script advancement is needed.  In this instance mTrain (or a replacement) must be updated to read and interpret the experiment record produced by Bonsai (Bonsai would not directly interact with mTrain).
  - Note on WaterLog test and integration.
    - In principle, there is no integration required for WaterLog.  Water delivery should be implemented through a Bonsai plugin that interacts with the hardware (this will happen in phase 1)
  - Conversion of sync+csv to NWB files. 

#### **Phase 3 :** Testing integration
  - Testing at scale with mice trained through the pipeline with the detection of change worklow finalized in phase 1. 
  - Catch and fix integration issues
  
### Goal of this specific effort

This document details *phase 1* of the integration of Bonsai into our behavioral pipeline. 

### Details of each required effort for Phase 1

#### Saving data from Bonsai

We will determine output file formats in agreement with key stakeholders. 

##### Data format

If we adopt Bonsai, it is critical that its data outputs can interface with our existing analysis pipelines. At the same time, there are a lot of drawbacks to our current system (saving all behavior data + metadata in a pickle file), and switching to Bonsai presents an opportunity to rethink our approach.

In Bonsai, it is incredibly easy to do two things: 

1. Trigger a digital output on a software event and sending that event to a dedicated sync line.

2. Write timestamped data to a CSV file

This suggests a different way forward, in which any events relevant to the task or stimulus are associated with both a digital on/off transition recorded by the sync computer, as well as metadata stored in a CSV file. At the end of the experiment, it is simple to package all of this into a single file (pickle or otherwise), assuming a minimal amount of bookkeeping to keep track of which sync lines are associated with which type of events.

This approach is more "lightweight" and language-agnostic than what is used by Camstim, although it will take some work to define consistent conventions that can be used across experiments.
This proposal is practical as our pipeline sync hardware and wiring boxes have 6 available sync lines with another 10 (for a total of 16) that could be made available with changes to the sync box.  This concept was tested during the piloting efforts (utilized several of the available sync lines to turn on in software via Bonsai).

Storing behavioral critical information as sync lines comes with several benefits: 
  - The sync system is fundamentally our reference temporal system and has the highest temporal precision and reliability. 
  - Sync files are efficient and lightweight: They only store state transitions in an hdf5 file, thereby minimizing data storage required. 
  - We already are experienced handling and using those files throughout the whole data collection and analysis pipeline. 
  - NWB files stores stimulus information in a stimulus **trial** table which uses the same storage scheme: Individual events have a name, a start and end timestamps associated to it. The start and end timestamps are essentially the rising and falling edges of a sync line. 
See here for more details : https://pynwb.readthedocs.io/en/stable/tutorials/general/file.html#trials
  - This simple storage scheme provides a great deal of flexibility on how behavioral events are recorded. Each scientific team can leverage available sync lines within Bonsai in a way that fits their scientific requirements. 

##### Current dependencies associated with output data format

Our proposal to switch from pkl files to a more general format including sync .h5 files + csv files comes with inherent development efforts. We should maintain our legacy system as we develop our new capabilities leveraging Bonsai. 

Currently, there are several dependencies on this data storage scheme: 
- **Data transfer from the experimental rigs to internal file storage registered by LIMS**. Those systems are maintained by MPE and can already handle various data formats produced by the instruments. 
- **Data conversion from pkl files to LIMS database and the associated interaction with mTRAIN**. mTrain essentially monitors behavior performance by extracting key metrics from pkl files. This interaction will have to be updated. 
- **Mouse-seeks access to pkl files information**. Mouse-seeks provide immediate analysis to behavioral data from pkl files to monitor basic metrics. The existing codebase can easily be transitioned to depend on a new file format by adding new loading and metrics calculation functions. This system was designed to work with a large collection of data storage files. 
- **Data conversion from pkl files to NWB files**. We discussed above in #Data format how simplifying our storage using event-based sync files will simplify this conversion. These NWB files will act as the primary gateway to data for the OpenScope project. Our goal is to avoid any dependencies on internal files/databases for external teams.   
- **Existing codebases accessing pkl files for behavioral and physiology analyses**. Perhaps this is where we have the largest legacy dependency. When appropriate, this suggests that ongoing projects should continue using our legacy Camstim and pkl system unless there is a desire to transition these codebases to work solely from NWB files.  

#### Add the ability to start a Bonsai stimulus session from the WSE
To be filled.

#### Add messaging from Bonsai so it can return status to the WSE
Ready, displaying stimulus, stimulus completed (with completion codes)
    
#### Add capability to Bonsai so it can push stimulus status messages to the BehaviorMon service
Session started, encoder count, rewards issued, passes, fails etc.  

#### Generate template workflows for a variety of stimuli.
To be filled.

#### System to manage binary dependencies of stimuli.
To be filled.

#### Interaction with BehaviorMon.
To be filled. 

#### Additional Hardware Interfaces:
- Implement DAQ digital input
- Enhanced encoder
    
#### Finalize faithful replicate of the detection of change task with a bonsai workflow (trial logic, abort logic,...): 
This will be our key test bench workflow. 
This will allow to further develop our workflow template:

##### Workflow templates

To faciliate the development of new behavioral workflow, we propose to first develop an **empty workflow template** which will contain the connected nodes associated with :

1. Declaring the visual stimulation hardware
2. Creating the geometry associated with our rigs. 
3. Drawing and controlling the photodiode square pulse in the right position
4. Reading a lick line and sending it directly to the water reward line
5. Controlling one sync line for the start and end of the sessions and one sync line for following the stimulus rendering. 
6. Starting and aborting a workflow remotely
7. Saving the wheel speed.

Based on our experience with Bonsai, we assembled a first draft of this workflow, as shown in the figure below. This example highlights how easy and accessible are all of the components of the template.

![Slide1](https://user-images.githubusercontent.com/2491343/119024600-1aa1bd00-b958-11eb-9cc7-5eff63b69e56.png)
*A proposed workflow template to develop new workflows. The modularity of Bonsai allowing to easily add new components is very apparent here. Each connected directed graph is associated with a description of its role*

Once this template is finalized, we recommend building exemplar sub-workflows that display drifting gratings, natural images and movies, and running the detection of change task. The modularity of Bonsai will allow us to copy/paste those worflows into the template while developing a new task. 

To be filled 

### Description of integration tests for phase 1
We should describe here which tests we intent to run to validate the system.

#### Test 1
xxx

#### Test 2
XXX

## Results

We should document here the results of our tests.

## Discussion

This discussion is meant to be filled once we have finished the integration of Phase 1. 

### Timeline

The goal of the OpenScope project is to have Bonsai integration available for the second proposal cycle (ie. experiments starting Q1 2023). Other teams and projects dependencies could be considered based on the following proposal timeline. 

#### **Phase 1 :** Single rig integration
Phase 1 is primarily a developmental effort by MPE with key involvements of stakeholders (technology, scientifc teams, ...) for finalizing the data storage output of Bonsai. We aim to have a beta release of all of these components by the end of 2021. This effort could entail hiring an additonal staff member for the MPE team using resources provided by the NIH U24 grant. 

#### **Phase 2 :** Cluster integration
We expect this development to occur during Q1 and Q2 of 2022. This timeline could be refined based on progress in Phase 1.

#### **Phase 3 :** Testing integration
We expect this integration test to occur in Q3 and Q4 of 2022. This timeline could be refined based on progress in Phase 2. 

## Conclusion

see [Highlights](#Highlights) at the top of the document.

## References

1.	Lopes, G. et al. (2015) Bonsai: an event-based framework for processing and controlling data streams. *Front Neuroinform* **9**: 7. 
2.	Lopes, G. et al. (2020) BonVision – an open-source software to create and control visual environments. *bioRxiv.* doi:10.1101/2020.03.09.983775. 

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
