Ce script télécharge l'ensemble des fichiers d'annotations xml au format Pangloss d'une langue


(La partie de ce script qui récupère les informations de métadonnées provient d'un développement fait par Aurélia Vasile)

Pour lancer le script : 
```
python download_all_annotations_for_one_language.py --language --path_metadata PanglossXMLMetadadaFile
```

Input :
- `languaneName` : l'intitulé de la langue tel qu'il a été enregistré dans Pangloss
- `PanglossXMLMetadadaFile` : le fichier de métadonnées de la collection Pangloss (récupérable par moissonnage oai -> script disponible dans [harvest_cocoon_repository]())


Output :
- Un répertoire `results` contenant tous les fichiers d'annotations 

********


This script is used to download all xml annotations files for one language from the Pangloss collection.
The output is in a repository named "results"

Input :
- `languaneName` : Language name as it's recorded in Pangloss collection
- `PanglossXMLMetadadaFile` : Pangloss metadata xml file (you can get it by harvesting Cocoon oai repository -> script is available in [harvest_cocoon_repository]())


Output :
- A `results` directory containing all annotation files

Command:

python download_all_annotations_for_one_language.py --language --path_metadata PanglossXMLMetadadaFile