
## Doesn't Matter Any More

**Defaults associated with Minimal_AP.idf**
- Are they what I would like?


**DevEx**
- VSCode shortcut for `from rich import print as rprint` or global import?



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