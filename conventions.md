# Conventions 


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

**Unit Vectors**
![Normal Vector Drawing](conventions/normal_vector.png)
