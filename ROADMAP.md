# Project Roadmap 


## Need to Complete, Not Roadblocks atm  
- [ ] Add default global geometry rules to all IDFs

**Base Objects**
- [ ] Test names, especially the regexing..

**Zones**
- [ ] room zone key with RoomZonePair 
- [ ] domain create bounds.. 
Testing 
- [ ] Tests to do on rooms -> no duplicates..
- [ ] -> Domains should be hashed -> no dup domains,
- [ ] no duplicate room names..
- [ ] 


**Subsurface logic**
- [ ] creating domain from centroid
- [ ] creating domain from cardinal points
- [ ] buffer
- [ ] checking subsurface and surface areas are valid, throwing image on error
- [ ] clean up domains!
2.0
- [ ] > 1 subsurface on a surface


## Future Issues
**Geometry rules**
- Need to either conform to geometry rules from the idf, or assert that they are a particular way 
- Need to find the boundaries and act accordingly. 


## Maintenance
**Exception**
- Review code, figure out types of exceptions being thrown, and handle accordingly
  

**Inheritance for EZObjects**
- These should be regular classes not dataclasses, probably.. 


**Need to fix the geomeppy error!**
  - Mutable sequence bc of different version of python -> pull request?

**Set location of EnergyPlus Installation + IDD file**
- Either look for this or or make an input to EZCase.. 
- Making the path to the IDD is good enough, but can't make my local installation a default.. 
- Maybe have a separate version for testsing, or remember to remove 



## Future features 
**Logging (with Rich?)**
  - Detailed IDD already set error (+ need to better understand the scope of this IDD set.. )





## Learn more about 
- Doing errors correctly.. 

