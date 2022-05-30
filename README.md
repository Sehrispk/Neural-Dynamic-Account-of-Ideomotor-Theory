# Neural Dynamic Account Of Ideomotor Theory
This repository contains the Webots and Cedar implementation of a Neural Dynamic Model. This Project is part of the Master-Thesis "A Neural Dynamic Account of Ideomotor Theory: Contingency Learning and Goal Oriented Behavior" from Stephan Sehring at Ruhr-Universität Bochum.

### Overview
The thesis describing the implemented model in detail is provided in Neural_Dynamic_Account_of_Ideomotor_Theory.pdf.

Files implementing the Webots simulation are located in /worlds, /controllers/ and /protos. These include the world file, the protos for custom robots and the robot controllers. 

Files implementing the Cedar simulation are located in /DFT-Architecture. This includes the implemented architecture and the experiment. 

Some plot tools are provided in /plotUtils.

### Dependencies
The Simulation was implemented in Ubuntu.

The simulation is run in Webots (https://cyberbotics.com/). 

The Architecture is simulated in Cedar (https://cedar.ini.rub.de/).

### Install
The Webot robot controllers were written for Ubuntu. Installation guide for Webots can be found at https://cyberbotics.com/doc/guide/installing-webots.

The Cedar Architecture requires TCP read/write and Reward Hebb trace plugins. Installation guide can be found at https://cedar.ini.rub.de/tutorials/writing_custom_code_for_cedar/.

### Run Program
To run the simulation, both the Webots and Cedar simulations have to interface. To connect, customize ip-Address in /controllers/E-puckController/default_config and TCP-writers in Cedar. Data is saved automatically. Run /DFT-Architecture/Experiment.jsom in Cedar to start experiment.

### Sample Data
An exemplary sample raw data set is provided at:
https://www.dropbox.com/sh/airer437hs9hbew/AACuDyf-uq6zBmDTw51AQZSFa?dl=0

### Plotting
/plotUtils provide some scripts for ploting recorded data. Just add relevant paths to config.yml.

### Authors
* Stephan Sehring
