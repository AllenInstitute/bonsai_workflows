## Hardware interfacing through 6321 and 6001 NIDAQ's
The hardware interactions have been added to this test workflow in the **Sync Square and Hardware** Group Workflow.
Digital outputs are handled via the **Bonsai.DAQmx package**, along with Analog inputs (and outputs, in theory), while digital inputs are handled through the **Bonsai.Arduino** package. 
Device ID's and ports/lines for the BTVTest rig are shown below.

### Current Configuration
The example here shows the sync square output to the screen, as well as a digital output signal that displays the state of the sync square. There is also a stim_vsync line that is currently running at 30hz, and a digital output that is watching the digital input from the arduino and mapping it out to the 6321 DAQ.

**Currently enabled:**
*Digital In*
COM3 Pin 2: Digitized piezo lick signal via Arduino Micro

*Digital Out*
Dev1/port1/line4: 30 Hz stim frame signal
Dev1/port1/line5: Digital Input of piezo lick signal, output back to the 6321 DAQ
Dev1/port1/line7: Photodiode digital status signal

*Analog In*
Dev0/ai2: Analog encoder Vsig

## Analog Input
Dev0/AI2 is the vsig for the analog encoder
Dev0/AI3 is the vref (5V) signal for the analog encoder

### Sync Lines for interaction
| 6321 Dev1         | Sync Line     | sync line label      |
| ----------------- |:-------------:| --------------------:|
| Dev1/port1/line4  | line 2        | vsync_stim           |
| Dev1/port1/line5  | line 3        | None                 |
| Dev1/port1/line7  | line 5        | stim_running         |
| Dev1/port0/line1  | line 6        | None                 |
| Dev1/port0/line0  | line 7        | None                 |
| Dev1/port2/line1  | line 15       | None                 |
| Dev1/port2/line2  | line 17       | stim_running_opto    |
| Dev1/port2/line3  | line 18       | stim_trial_opto      |
