# Bonsai + Allen : A report toward integrating Bonsai into our behavioral pipeline

<img src="Images/bonsai-lettering.svg?token=AATAHT4TLCQWUH54YLGGACDAT3QKU" height="100" />
<img src="Images/AllenInstitute_Logo_RGB.png?token=AATAHTYYP47RH4KTUQBIBEDAT3QBQ" height="100" />

## Introduction 

### Description of Bonsai

[Bonsai](https://bonsai-rx.org) is an open-source visual programming language for controlling systems neuroscience experiments. The logic of each experiment is specified by a Bonsai “workflow” file, which defines how diverse input and output signals are coordinated in time. The [BonVision](https://bonvision.github.io/) package includes workflow nodes for generating visual stimuli and presenting them with high temporal fidelity. Additional packages provide interfaces to NI hardware, Arduinos, and other DAQ hardware. This makes it possible to replicate the majority of Camstim functionality using existing Bonsai packages.

### Goal of this effort

This document details ongoing requirements and efforts related to the piloting and testing of Bonsai as part of the Allen Brain Observatory pipeline. We assess here whether and how Bonsai can replace Camstim for controlling both passive viewing and active behavior experiments. Bonsai would update visual (or other) stimuli in response to lick and running wheel input, and would need to operate in conjunction with existing software packages, such as WSE, Sync, and Videomon. 

### Design principles 
Behavioral task designs are specified as Bonsai workflow files  (.bonsai). These files will be provided by each internal or external scientific team. Hardware components of the pipeline will be integrated with existing Bonsai modules and (if necessary) with custom Bonsai packages written in C#. Commonly used stimulus types can be saved as reusable workflow elements that can be shared by multiple scientific teams. Each package will have a deployed and testing mode, allowing individual packages to emulate normal functions on the experimental rig when the hardware is not available. 

### Areas for evaluation

#### Stimulus and task definition
We ensure that Bonsai can cover our desired range of use cases with a simple/limited set of test cases: 
  - Passively viewing visual stimuli 
    - Static and drifting gratings 
    - Natural images and movies 
  - Active behavior 
    - Run a simple go/no go task with only one natural image associated with go and no go trials, with fixed trial probabilities. 
    - Run a simple detection of change behavior with fixed change probability.  
  - Concatenating scripts  
    - Run an experiment built from multiple scripts, e.g.: 
        - Run static gratings stimuli.
        - Run Sparse Noise stimuli.
        - Run a Go/No Go experiment.

#### Pipeline integration 
  - Bonsai should be compatible with our behavior hardware (lick spouts, running wheels, etc.) and our hardware control packages (such as `daqmx`)  
  - We should be able to make a portable hardware configuration using Bonsai. 
  - We should evaluate how hardware configuration parameters will be saved (port number and device address for instance).  
  - Scripts should be able to reference input/output components by an informative name (for instance, `lick_line_status` or `reward_signal`, rather than `NI device 1, input 0`).  
  - We need to start scripts from WSE/Mouse Director 
  - We need to be able to poll for status (15 or 20 things) 
  - We need Bonsai to publish stats along the way (to accumulator) 
 
#### Benchmarking
  - Performance levels (in terms of temporal precision) should be compatible with behavior experiments, including visual stimulus presentation 
  - We should check that BonVision’s stimulus warping functions properly as documented in BonVision’s documentation and warping does not impair display performance beyond our QC criteria. 
 
## Methods

### Description of Bonsai test rig

For this effort, we built a testing rig at the Institute allowing scientific teams to submit integration tests of their Bonsai workflow with a reasonable duplicate of the pipeline hardware:
- This rig had a replicated Stimulus computer, Sync computer, Camera monitor computer with teh same specifications as the pipeline rigs. 
- The stimulus computer running Bonsai had an Nvidia Quadro K4000 graphics card and 32Gb of RAM.  
- The 6321 DAQ is installed in the stimulus computer running Bonsai via PCIe connection. Digital output lines are configured using this daq to output signals from Bonsai workflows which are captured on a seperate machine via a PCIe-6612 DAQ to be analyzed. 
- Due to the DAQmx library not having a digital input function at the present time (see [Discussion](#Discussion)), digital inputs to the Bonsai stimulus are implemented via an arduino micro that is attached to the stimulus computer via USB. 
- Lick detection was implemented with a piezo contact microphone but could be bypassed with a signal generator which was used to provide a 0.1 Hz signal for testing
- Sync lines installed and used in this study are shown in the table below with labels
![image](https://user-images.githubusercontent.com/2491343/117510054-36f92f00-af40-11eb-80b3-26ce6f71b309.png)
- As on all physiological rigs, a photodiode was installed in the top-right corner of the stimulus monitor and connected by a photodiode circuit connected to a dedicated sync line. 
- A subset of sync lines were turn on and off by various experimental worklows (see below). 

### Description of workflows

Based on requirements to tests multiple test cases, we designed and created multiple complementaries workflows. Each workflow was led by a different scientist so as to gain feedbacks and experience from multiple personal expertise. 

1 - **Passively viewing worflow**.
This worflow presented windowed drifting gratings of various contrasts as well as a replicated version of the locally sparse noise stimulus. 
All stimuli were wrapped onto a spherical projection as is currently being implemented in CamStim. 
This workflow is available [here](https://github.com/AllenInstitute/bonsai_workflows/tree/master/PassiveViewing).

2 - **Go/No Go behavior workflow**.
This worflow presented 2 natural images, one associated to a GO stimulus and the other to a NO GO stimulus. The GO stimulus triggered an external reward line.
Image presentation was randomly selected from a uniform distribution at run-time. 
All stimuli were wrapped onto a spherical projection as is currently being implemented in CamStim. 
This workflow is available [here](https://github.com/AllenInstitute/bonsai_workflows/tree/master/Go-Nogo).

3 - **Detection of change workflow**.
This worflow presented 8 natural images, following the logic of the visual behavior workflow. Image change was triggered by pulling from a uniform distribution, deciding how many times each image was repeated. Pre-change lick would delay subsequent change by 2 presentations. 
All stimuli were wrapped onto a spherical projection as is currently being implemented in CamStim. 
This workflow is available [here](https://github.com/AllenInstitute/bonsai_workflows/tree/master/DetectionOfChange).

4 -  **Performance measurement workflow developed by Goncalo Lopes**. Our intent here was to compare performance metrics of our test rig with published values. This worfklow displayed an increasing large number of drifting gratings in an array pattern to assess performance of Bonsai and BonVision under stress. 
This workflow is available [here](https://github.com/AllenInstitute/bonsai_workflows/tree/master/GridGratingDrawing).

  - All workflows triggered the photo-diode sync line via BonVision, similarly to how CamStim creates an oscillating stimulus black and white square under the photodiode. 
  - All workflows alternated a dedicated sync line upon frame calculation. 
  - The "detection of change" workflow leveraged the largest number of sync lines to measure: 
    - The turn-around time to read a lick TTL into an external TTL on another sync line. 
    - The reward calculation time to convert a lick TTL into a trigger reward via a TTL pulse when an image changed happened concurrently to a lick. 

### Description of tests

Using the above described platform and workflows, we ran a series of tests and quantifications. Those tests were meant to evaluate the stability and performance. 
We ran each worflow separately. The associated datasets are available [here](https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis). 
Briefly: 

- Test on Bonsai performance script: Workflow that display increasingly large number of gratings, ran and analyzed. 
  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/GridGratingDrawing

- Test on passively viewing stimuli: Workflow that display driftings gratings and locally sparse noise, ran and analyzed
  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/PassiveViewing_run1
  
- Test on Go/No:
  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/long_stim_test_1
  Ran for an hour long with no interactions. 
  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/keyboard_test_1
  Ran for approximately 5 min with manual keyboard interactions

- Tests on Detection of change
  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/det_change_short_manual
  Ran for approximately 5 min with manual keyboard interactions. All hardware was connected and functional (lick sensor, water valves)

  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/det_change_long_no_licks
  Ran for an hour with no incoming licks. All hardware was connected and functional

  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/det_change_long_fake_lick_generator
  Ran for an hour with a 0.1 Hz TTL generator as lick input incoming licks. All hardware was connected and functional. Reward valve was triggered

  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/detection_of_change_with_camera
  Ran for approximately 5 min with a workflow that performs detection of change while also acquiring and saving a camera feed at 30Hz

  - https://github.com/AllenInstitute/bonsai_workflows/tree/master/Analysis/detection_of_change_without_camera
  Same as above but camera feed was disabled. 

## Results

[Insert qualitative assessment here here]


### Passive viewing experiments

#### Stimulus update intervals

![Quantification of photodiode stability during passively viewing of gratings and locallyl sparse noise](https://raw.githubusercontent.com/AllenInstitute/bonsai_workflows/master/Analysis/PassiveViewing_run1/2021-05-12-passively_viewing_run1.png?token=AATAHT6BHRUH5BZ4KQGZCILAUWEAU).

*Quantification of photodiode stability during passively viewing of gratings and locally sparse noise*

#### Stress test

To validate our measure of performance and push Bonsai over its limit, we reproduced a performance quantification published along the BonVision paper [(Lopes et al. 2020)](https://www.biorxiv.org/content/10.1101/2020.03.09.983775v3). To that end, we [modified a workflow](https://github.com/AllenInstitute/bonsai_workflows/blob/master/GridGratingDrawing/gabor.bonsai) displaying an increasingly large number of non-overlapping grating elements. A reference figure was published in the original BonVision publication and is shared here for ease of comparision:

![Goncalo_2020_figure](https://user-images.githubusercontent.com/2491343/118040614-9da69000-b326-11eb-8c9e-2cfac2789695.png)

*Quantification of frame update period (Bottom) to display an array of drifting gratings (Top). Reproduced from (Lopes et al., 2020)*

In this test, Bonvision is tasked to display a very large number of drifting gratings in an array pattern. We replicated the code, utilizing our photodiode circuit to measure the rising time of requested stimuli updates. The associated analysis is [available in this notebook](https://github.com/AllenInstitute/bonsai_workflows/blob/master/Analysis/GridGratingDrawing/2021-05-12-GridGratingDrawing.ipynb). 

Our  figure below is faithful to the original published publication, i.e., approximately 1000 grating elements are necessary before performance (measured in frames per second) start to deteriorate:

![Reproduction of performance](Images/2021-05-12-BonVision_grating_replication.png)

*Quantification of frame update period to display an array of drifting gratings using the same workflow from (Lopes 2020) but on an Allen Institute stimulus test rig.* 



### Go/No task

- Screen stimulation stability

- Sync lines output stability

### Detection of change task

- Screen stimulation stability

- Sync lines output stability

### Concurrent acquisition of video

A key promise of Bonsai is its ability to quickly integrate multiple data modalities in a single data workflow. For example, measuring key behavioral parameters from a continuous stream of frames from a behavior camera would allow closed-loop experiments. While we do not anticipate this immediate use-case for the OpenScope project, this is a key property of Bonsai as [DeepLabCut modules](https://github.com/bonsai-rx/deeplabcut) have been fully integrated into Bonsai. To evaluate this capability, we measured the impact of continuously acquiring and saving an additional webcam, while running the detection of change task. The workflow for this experiment is [available here](https://github.com/AllenInstitute/bonsai_workflows/blob/master/DetectionOfChange/DetectionOfChange_with_hardware_and_camera.bonsai).  

The results for this comparison are plotted below. The associated code is [available here](https://github.com/AllenInstitute/bonsai_workflows/blob/master/DetectionOfChange/DetectionOfChange_with_hardware_and_camera.bonsai). 

![Detection of change performance with camera on](https://raw.githubusercontent.com/AllenInstitute/bonsai_workflows/master/Analysis/detection_of_change_with_camera/det_change_with_camera_sync_lines.png?token=AATAHT6CRDIBJSHND4N44UDAUWB2K).

*Quantification of frame update period in detection of change while acquiring and saving a video from a webcam at 30Hz.* 

![Detection of change performance with camera off](https://raw.githubusercontent.com/AllenInstitute/bonsai_workflows/master/Analysis/detection_of_change_without_camera/det_change_without_camera_sync_lines.png?token=AATAHT7BQ25K6NYR6CFGKVTAUWB36).

*Quantification of frame update period in detection of change without acquiring and saving a video.* 

The recorded video can be visualized [here](https://github.com/AllenInstitute/bonsai_workflows/blob/master/Analysis/detection_of_change_with_camera/camera_data.avi).


### Concatenating stimuli / tasks

- Screen stimulation stability

- Sync lines output stability


### Capabilities available for integration tests

- Describe here the capabilties that are already available 
- MORE DETAILS HERE

### Capabilities missing for integration tests

- Describe here the capabilties that are needed for integration 
- MORE DETAILS HERE

## Discussion

### Hardware integration

Hardware integration is one area where Bonsai clearly shines. With existing support for NI devices, Arduinos, and a wide range of cameras, it should be able to cover all of our hardware interfacing needs. It's also helpful that events from standard input devices (e.g., keyboard and computer mouse) can serve as a stand-in for digital input lines.

One limitation we encountered was that there is currently no "digital input" node for NI devices. The workaround was to use an Arduino for digital input.

It is straightforward to update the monitor configuration for a given rig by copy-pasting the relevant BonVision nodes into the workflow. These contain information about the monitor size, warping, and gamma calibration.

### Using Bonsai for coding behavioral experiments

It is clear that there is a steep learning curve to becoming proficient in Bonsai. There are many concepts from procedural programming languages that cannot be translated directly into Bonsai, which is closer to a functional programming language (see [this page](Bonsai_for_Python_Programmers.md) for an overview of the differences between Bonsai and Python). The behavior of particular Combinators (which are an essential for using Bonsai well) can be difficult to understand, and lack thorough documentation. While Bonsai makes it simple to do certain things that would be complicated in Python (e.g., coordinating responses to multiple asynchronous data streams), there are many things that are more complicated in Bonsai. This is bound to lead to frustrations for scientists that don't want to learn a new programming language to set up their experiment.

After carrying out our pilot experiments, a few things are clear:

- **There is almost nothing that can't be done in Bonsai.** Bonsai is a fully featured programming language, so it can be set up to produce any desired behavior. However, this can require the inputs of Bonsai experts (e.g., Gonçalo), in particular given the current state of the documentation.

- **Some implementations are better than others.** As an example of this, the GO/NOGO task we implemented was taking longer to display frames whenever the image changed. After Gonçalo inspected it, he found that the use of the `TimedGate` combinator was causing these delays; replacing it with an equivalent set of operators improved performance dramatically. For a naive user, there would be no obvious difference between these implementations.

- **Working examples are extremely important.** It's a lot easier to modify an existing Bonsai workflow than to build one from scratch. The available "prototype" workflows are currently lacking, so it would be extremely beneficial to develop more annotated examples. Similarly, a standardized pre-built workflow with all our hardware components included would greatly facilitate the development of new tasks.  

- **Debugging is easier in some ways, and harder in others.** One amazing feature of Bonsai is its ability to do introspection on the state of any operator while the workflow is running. However, when opening visualizers for many nodes in parallel, it can be difficult to keep track of all of them (i.e., having a centralized debug console would be helpful).

There are three ways that task development in Bonsai can be improved:

1. **Establishing local expertise.** It is not sustainable to rely on Gonçalo for troubleshooting (even though he is always more than happy to help). We need at least one in-house Bonsai expert who can help develop workflows and train others.

2. **Improving documentation and tutorials.** If we decide to adopt Bonsai, the developer time that would have been spent implementing a novel behavioral control system should be spent documenting Bonsai. This will have tremendous benefits for both our own work, and for the wider community. The importance of this cannot be overemphasized -- the ROI on this effort would be huge.

3. **Creating re-usable workflow elements and an empty canvas workflow with all pre-requisites.** If developing tasks in Bonsai can be as simple as copying and pasting standard building blocks, then it becomes much more practical for anyone to get up and running. This is aided by the fact that Bonsai workflows are defined by XML strings, which can be copied from anywhere (see [this page](https://open-ephys.github.io/onix-docs/Software%20Guide/Bonsai.ONIX%20Reference/index.html) for an example). An empty canvas workflow would provide key elements like rig geometry, photodiode square stimuli, wrapping, screen calibration and basic sync lines already pre-configured. During our tests, we already converged to a shared basic structure between all workflows.

### Overall performance

By all measures, Bonsai performed extremely well for displaying visual stimuli. Stimulus rendering intervals were consistently within 2 ms of the median, and measured photodiode flips occurred within 50 microseconds of the expected interval. There was no evidence of dropped frames, except when the rendering loop was pushed to the limit, e.g. with >1000 simultaneous drifting gratings. Performance did not deteriorate when camera frames were acquired and saved in parallel (although no online video processing was attempted).

It's safe to say that Bonsai's performance is better than camstim, which often shows dropped frames and irregular stimulus intervals.

### Data format

If we adopt Bonsai, it is critical that its data outputs can interface with our existing analysis pipelines. At the same time, there are a lot of drawbacks to our current system (saving all behavior data + metadata in a pickle file), and switching to Bonsai presents an opportunity to rethink our approach.

In Bonsai, it is incredibly easy to do two things: 

1. Trigger a digital output on a software event and sending that event to a dedicated sync line.
2. Write timestamped data to a CSV file

This suggests a different way forward, in which any events relevant to the task or stimulus are associated with both a digital on/off transition recorded by the sync computer, as well as metadata stored in a CSV file. At the end of the experiment, it is simple to package all of this into a single file (pickle or otherwise), assuming a minimal amount of bookkeeping to keep track of which sync lines are associated with which type of events.

This approach is more "lightweight" and language-agnostic that what is used by camstim, although it will take some work to define consistent conventions that can be used across experiments.
This proposal is practical as our pipeline sync hardware and wiring boxes already have **XXX** unused and available sync line that we could essentially turn on in software via Bonsai. 

Storing behavioral critical information as sync lines comes with several benefits: 
  - The sync system is fundamentally our reference temporal system and has the highest temporal precision and reliability. 
  - sync files are efficient and lightweights: They only store state transitions in an hdf5 file thereby minimizing data storage required. 
  - We already are experienced handling and using those files throughout the whole data collection and analysis pipeline. 
  - NWB files stores stimulus information in a stimulus **trial** table which uses the same storage scheme: Individual events have a name, a start and end timestamps associated to it. The start and end timestamps are essentially the rising and falling edges of a sync line. 
See here for more details : https://pynwb.readthedocs.io/en/stable/tutorials/general/file.html#trials
  - This simple storage scheme provides a great deal of flexibility on how behavioral events are recorded. Each scientific team can leverage available sync lines within Bonsai in a way that fits their scientific requirements. 

### Components to develop and integrate

COLIN/QUINN : Describe the missing pieces.

### Proposed strategy 

COLIN/QUINN : Migrating Bonsai to be used in the Allen Brain Observatory pipelines will be a multi-component process that should be tackled in distinct phases. This will allow us to avoid accelerated integration timelines and an efficient development.

#### **Phase 0 :** Bonsai pilot + Report + Build plan
The purpose and content of this report. 

#### **Phase 1 :** Single rig integration
  - Work out the need of running Bonsai during one session. 
  - Integration with WSE and hardware.
  - Saving data.
  - MORE DETAILS HERE
  - Generate template workflows for a variety of stimuli. 
  - System to manage binary depencies of stimuli. 

#### **Phase 2 :** Cluster integration
  - Interaction with BehaviorMon.
  - mTrain integration.
  - WaterLog test and integration.
  - MORE DETAILS HERE
  - Hardware backward compatible 

#### **Phase 3 :** Testing integration
  - Testing at scale with mice trained through the pipeline with a previously validated and known behavior. 
  - Catch and fix integration issues
  - MORE DETAILS HERE

### Timeline

COLIN/QUINN : What is practical for each phase? Maybe propose different scenarii depending on resources and priority? 

#### **Phase 1 :** Single rig integration
  - Proposed timeline

#### **Phase 2 :** Cluster integration
  - Proposed timeline

#### **Phase 3 :** Testing integration
  - Proposed timeline
  
### Discussion on Bonsai conceptual layers.

TBD (Jerome)

### Discusson on template

TBD


### Community engagement and ecosystem support

Bonsai already has a broad userbase and a fair number of extensions written by the community. It is critical that we don't operate in a vacuum, and that we engage with existing users at every step of the way. Once our development plan is more concrete, we should share it with the community (e.g., through the [bonsai-users](https://groups.google.com/g/bonsai-users) forum), to make sure we are not doing anything that's redundant with others.

### Potential synergies with AIx2, IBL, SWC

In addition to the hundreds of labs that use Bonsai, there are several larger research groups that have already adopted it or are considering adoption. The International Brain Laboratory uses Bonsai to control its behavioral tasks, and they have been extremely helpful in pointing out the issues they've encountered. The Sainsbury Wellcome Centre at UCL is now working with NeuroGEARS (Gonçalo's company) to develop task infrastructure around Bonsai. And AIx2, launching in 2022, is planning to use Bonsai for behavior control. We should do our best to communicate with these other projects, and hopefully divide up the work required to document and extend Bonsai. Eventually, it may be worthwhile to orchestrate a collaborative grant (or some consortium-style funding agreement) to help sustain Bonsai over the long run.

## Conclusion

Text goes here.

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


