Ce script convertit un fichier csv de métadonées en fichier xml de métadonnées pangloss 



Pour lancer le script : 
```
python csv_v2_to_xml.py emplacement/fichier_csv
```

Input :
- `fichier_metadata.csv` : le fichier csv contenant les métadonnées des ressources à déposer


Output :
- Un fichier nommé à l'identique du fichier d'entrée mais au format xml : fichier_metadata.xml

********


This script is used to convert csv metadata file in an xml pangloss metadata file (using dublin core and olac standards)
the output file name is the same as the input one

Input :
- `metadata_file.csv`: csv metadata file


Output :
- `metadata_file.xml`: metadata file in the format required for a deposit

Command:

```
python csv_v2_to_xml.py path/metadata_file.csv
```