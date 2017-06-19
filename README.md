# AquaCrop-Irrigation-Designer
a simulation tool base on python code executing aquacrop-plugin exeutable

# Environment

## Windows
- Windows Platform for .exe executing 
  - We highly recommend [anaconda](https://www.continuum.io/downloads) as python platfrom toolkit
- Python3.6
## Linux / Mac

We had trid using wine to execute AquaCrop_plugin, But it stuck with prompt windows.
Therefore, We suggest install Virtual Machine ( Oracle Virtual Box ... etc ) with Windows environment to execute our codes

If you need a lightweight developing environment for windows virtual mahcine, checkout this
- [Lightweight_python_dev_env.md](https://github.com/AgriHarmony/AquaCrop-Irrig.Designer/blob/master/Lightweight_python_dev_env.md)
# Usage

1. Open bin/aquacrop_v5_0/AquaCrop.exe and set up the simulation
  - Climate data, Crop, Management
  - Select the Irrigation to specific Irrigation Scheduling
  
2. Run python main.py to conduct the Irrigation Method Design by AquaCrop Simulation 

# Limitaion

## AquaCrop

- One direction water flow ( Only vertical )
- Daily timestep simulation
- No interactive API but execuatable

## Irrig.Designer
Due to the AquaCrop and AquaCrop-Plugin is close source program. User can not directly control the simulation process.
The main.py program have to repeatly check __[.pro name]PROday.out__ file. If the condition of __[.pro name]PROday.out__ file triggers irrigation event on specific date, the AquaCrop must to re-execute the whole simulation. 

The reason is that AquaCrop simulator does not generate middle status then it can not simulate from middle between first day and last day.
