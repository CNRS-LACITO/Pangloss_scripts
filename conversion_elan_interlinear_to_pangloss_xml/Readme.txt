Ce script convertit un fichier interlineaire elan (txt) en fichier xml au format pangloss 
Il doit être adapté en fonction des tiers utilisés dans elan (modifications à faire à la tout fin de la fonction `elan_to_pangloss`)  


Pour lancer le script : 
```
python elan_interlinear_to_pangloss.py rep_input/ rep_output/
```

Input :
- `rep_input` : le répertoire contenant le ou les fichiers elan interligne (format txt) à convertir.
Ce fichier contient les différentes tiers (exportés en block) ainsi que la tier de timecode (si elle existe doit être exportée au format ss.msec) 


Output :
- `rep_output` : Le répertoire contenant le ou les fichiers créés.
Ces fichiers xml créés sont enregistrés chacun avec le même nom du fichier d'entrée elan 

********


This script converts an elan interlinear file (txt) into an xml file in pangloss format. 
It must be adapted according to the tiers names used in elan (modifications to be made at the very end of the `elan_to_pangloss` function)
the output file name is the same as the input one

Input :
- `rep_input`: the directory containing the elan interline file(s) (txt format) to be converted.
This file contains the various tiers (exported as a block) and the timecode tier (if it exists, it must be exported in ss.msec format). 


Output :
- `rep_output`: The directory containing the file or files created.
The xml files created are each saved with the name of the input elan file

Command:

```
python elan_interlinear_to_pangloss.py rep_input/ rep_output/
```