# AquaCrop-Irrigation-Design
a simulation tool base on python code executing aquacrop-plugin exeutable

# Environment

- Windows Platform for .exe executing ( Linux and Mac you can use wine but I do not test it before")
- Python3.6

# Usage

1. Open bin/aquacrop_v5_0/AquaCrop.exe and set up the simulation
  - Climate data, Crop, Management
  - Select the Irrigation to specific Irrigation Scheduling
  
2. Run python main.py to conduct the Irrigation Method Design by AquaCrop Simulation 

# Limitaion
Due to the AquaCrop and AquaCrop-Plugin is close source program. User can not directly control the simulation process.
The main.py program have to repeatly check [.pro name]PROday.out file. If the condition of [.pro name]PROday.out file triggers irrigation event on specific date, the AquaCrop must to re-execute the whole simulation. 

The reason is that AquaCrop simulator does not generate middle status then it can not simulate from middle between first day and last day.
