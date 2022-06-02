Ce script ajoute automatiquement un DOI au niveau de la phrase pour tous les fichiers d'annotations d'une langue donnée (issu de la collection Pangloss) et ce, à partir du DOI de la ressource.
Phrase 1 -> DOI_de_la_ressource#S1
Phrase 2 -> DOI_de_la_ressource#S2
...

(La partie de ce script qui récupère les informations de métadonnées associées à un DOI provient d'un développement fait par Aurélia Vasile)

Pour lancer le script : 
```
python add_doi_in_annotation_sentences.py --language languaneName --path_annotations annotationRepository --path_metadata PanglossXMLMetadadaFile
```

Input :
- `languaneName` : l'intitulé de la langue tel qu'il a été enregistré dans Pangloss
- `annotationRepository` : le répertoire contenant l'ensemble des fichiers d'annotations d'une même langue pour lesquels les DOIs doivent être intégrés au niveau de la phrase (scripts disponibles dans [download_all_annotations_for_one_language]()) 
- `PanglossXMLMetadadaFile` : le fichier de métadonnées de la collection Pangloss (récupérable par moissonnage oai -> scripts disponibles dans [harvest_cocoon_repository]())


Output :
- Un répertoire `results` contenant tous les fichiers d'annotations avec les DOIs insérés
- Un fichier `erreur.txt` qui indique les erreurs rencontrées (pas de découpage en phrase du fichier d'annotations donc impossibilité d'ajouter les DOIs, fichiers d'annotations indiqué dans les métadonnées mais non présente dans le répertoire)

********


This script automatically adds a DOI at sentence level for all annotation files of a given language (from the Pangloss collection) based on the DOI of the resource.
Sentence 1 -> Resource_DOI#S1
Sentence 2 -> Resource_DOI#S2
...

Command:

python add_doi_in_annotation_sentences.py --language languaneName --path_annotations annotationRepository --path_metadata PanglossXMLMetadadaFile

Input :
- `languaneName` : Language name as it's recorded in Pangloss collection
- `annotationRepository` : Directory containing all annotation files for one language for which DOIs have to be integrated at sentence level (script is available in [download_all_annotations_for_one_language]()) 
- `PanglossXMLMetadadaFile` : Pangloss metadata xml file (you can get it by harvesting Cocoon oai repository -> script is available in [harvest_cocoon_repository]())

Output :
- A `results` directory containing all annotation files with Dois inserted at sentence level