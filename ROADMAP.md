# Project Roadmap 

## Future Issues
**Geometry rules**
- Need to either conform to geometry rules from the idf, or assert that they are a particular way 
- Need to find the boundaries and act accordingly. 


## Maintenance
**Inheritance for EZObjects**
- These should be regular classes not dataclasses, probably.. 


**Need to fix the geomeppy error!**
  - Mutable sequence etc.. 

**Set location of EnergyPlus Installation + IDD file**
- Either look for this or or make an input to EZCase.. 
- Making the path to the IDD is good enough, but can't make my local installation a default.. 
- Maybe have a separate version for testsing, or remember to remove 



## Future features 
**Logging (with Rich?)**
  - Detailed IDD already set error (+ need to better understand the scope of this IDD set.. )



## DevEx
- VSCode shortcut for `from rich import print as rprint` or global import?


## Learn more about 
- Doing errors correctly.. 


## Doesn't Matter Any More

**Defaults associated with Minimal_AP.idf**
- Are they what I would like?



## Completed 

**Eppy/Geomeppy Inheritance**
- Decide if using Epbunch from Eppy or Geomeppy? 
- Similarly decide if using IDF from Eppy or Geomeppy 
- Think Geomeppy generally has more features.., but Eppy is the base
- Decision: Using Geomeppy bc need add blocks.. 

**Make constants with keys that are used**
- ie Zone, BuildingSuface, etc => should all live in one locations.. folder => keys, then subdetails like "wall.." 


**Corralling Ep-related functions**
- Have an EZIDF class that has all the functions that need to happen at the idf level, this is what gets passed around.. 
- Also have EzBunch that makes the object stuff more legible... 
  - For now implemented as functions, could change this in the future.. 