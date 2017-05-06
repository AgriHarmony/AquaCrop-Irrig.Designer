
      5.0       : AquaCrop Version (October 2015)
  36241         : First day of simulation period - 22 March 2000    
  36350         : Last day of simulation period - 9 July 2000      
  36241         : First day of cropping period - 22 March 2000    
  36350         : Last day of cropping period - 9 July 2000      
      4         : Evaporation decline factor for stage II
      1.10      : Ke(x) Soil evaporation coefficient for fully wet and non-shaded soil surface
      5         : Threshold for green CC below which HI can no longer increase (% cover)
     70         : Starting depth of root zone expansion curve (% of Zmin)
      5.00      : Maximum allowable root zone expansion (fixed at 5 cm/day)
     -6         : Shape factor for effect water stress on root zone expansion
     20         : Required soil water content in top soil for germination (% TAW)
      1.0       : Adjustment factor for FAO-adjustment soil water depletion (p) by ETo
      3         : Number of days after which deficient aeration is fully effective
      1.00      : Exponent of senescence factor adjusting drop in photosynthetic activity of dying crop
     12         : Decrease of p(sen) once early canopy senescence is triggered (% of p(sen))
      1         : Thresholds for water stress for stomatal closure are affected by soil salinity stress
     30         : Depth [cm] of soil profile affected by water extraction by soil evaporation
      0.30      : Considered depth (m) of soil profile for calculation of mean soil water content for CN adjustment
      1         : CN is adjusted to Antecedent Moisture Class
     20         : salt diffusion factor (capacity for salt diffusion in micro pores) [%]
    100         : salt solubility [g/liter]
     16         : shape factor for effect of soil water content gradient on capillary rise
     12.0       : Default minimum temperature (�C) if no temperature file is specified
     28.0       : Default maximum temperature (�C) if no temperature file is specified
      3         : Default method for the calculation of growing degree days
-- 1. Climate (CLI) file
   Foggia.CLI
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\DATA\
   1.1 Temperature (Tnx or TMP) file
   Foggia.TMP
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\DATA\
   1.2 Reference ET (ETo) file
   Foggia.ETO
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\DATA\
   1.3 Rain (PLU) file
   Foggia.PLU
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\DATA\
   1.4 Atmospheric CO2 concentration (CO2) file
   MaunaLoa.CO2
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\SIMUL\
-- 2. Crop (CRO) file
   Tomato.CRO
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\DATA\
-- 3. Irrigation management (IRR) file
   Example.Irr
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\DATA\
-- 4. Field management (MAN) file
   ModerateSF.MAN
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\DATA\
-- 5. Soil profile (SOL) file
   DEFAULT.SOL
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\SIMUL\
-- 6. Groundwater table (GWT) file
   (None)
   (None)
-- 7. Initial conditions (SW0) file
   WetDry.SW0
   D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_v5_0\DATA\
-- 8. Off-season conditions (OFF) file
   (None)
   (None)
