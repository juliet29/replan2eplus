# Project Roadmap 

## Conventions 

**I/O**
- Will call file paths `PATH_TO_FILENAME`
- Will call directory paths `DIRECTORYNAME_DIR`
- As variables, use the lowercase `path_to_filename` and `directoryname_dir`

**Defaults and Constants**
- Will keep all defaults in a `defaults` folder or file? 


**Folder organization inside the design modules**
- data: reading json, will also have the json typed dict that is expected, and should throw error, maybe use pydantic
- interfaces: has types that are used in logic and expected in presentation? 
- logic: actual work 
- presentation: functions that `ezcase/main.py` will call... 

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