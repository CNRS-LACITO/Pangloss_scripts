import os, shutil
import sys
import re
import xml.etree.ElementTree as ETree
import urllib.parse, urllib.request, urllib.error
from collections import defaultdict
from parse import parseRecord
# import lxml.etree
import sqlvalidator
import pymysql
import pymysql.cursors
import argparse
import datetime
from pathlib import Path

DOI_PANGLOSS = "10.24397/Pangloss"

NAMESPACES = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms" : "http://purl.org/dc/terms/",
            "olac" : "http://www.language-archives.org/OLAC/1.1/",
            "xsi" : "http://www.w3.org/2001/XMLSchema-instance",
            "oai" : "http://www.openarchives.org/OAI/2.0/",
            "doi" : "http://datacite.org/schema/kernel-4",
            "crdo" : "http://cocoon.huma-num.fr/schemas/",
            
        }

caractsASupprimer = ['À','Á','Â','Ã','Ä','Å','Ç','È','É','Ê','Ë','Ì','Í','Î','Ï','Ò','Ó','Ô','Õ','Ö','Ù','Ú','Û','Ü','Ý','à','á','â','ã','ä','å','ç','è','é','ê','ë','ì','í','î','ï','ð','ò','ó','ô','õ','ö','ù','ú','û','ü','ý','ÿ']
caractPourRemplacer=['A','A','A','A','A','A','C','E','E','E','E','I','I','I','I','O','O','O','O','O','U','U','U','U','Y','a','a','a','a','a','a','c','e','e','e','e','i','i','i','i','o','o','o','o','o','o','u','u','u','u','y', 'y']

dico_pangloss = defaultdict(lambda: defaultdict(int))
dicoNomLangues = {}
listeNomLanguesExactes = set()

today = str(datetime.date.today())




# création d'un dictionnaire contenant en clé l'identifiant oai de la ressource et en valeur l'objet contenant toutes les métadonnées de la ressource
def dico_all_resources(metadata):
    
    print ('Parsing metadata....')
    tree = ETree.parse(metadata)
    root = tree.getroot()
    listAllResourcesMetadata =  {}
    
   # parsing du fichier xml pangloss de métadonnées
    for index, record in enumerate(root.findall(".//oai:record", NAMESPACES)):
 
        # appel de la fonction parseRecord pour parser chaque record et créer un objet record
        objetRecord = parseRecord(record)
        listAllResourcesMetadata [objetRecord.identifiantOAI] = objetRecord

    
    return listAllResourcesMetadata




# récupération de toutes les information contenue dans chaque record dans les métadonnées et remplissage du dictionnaire dico_pangloss qui sera le bilan du contenu de la collection    
def insert_doi_in_annotations(args):

    language_name = args.language
    metadata_file = args.path_metadata
    annotations_dir = args.path_annotations

    
    nb_annotations = 0
    dico_metadata = dico_all_resources(metadata_file)
    
    nb_ressources = 0

    error_file = open("error.txt", "w", encoding="utf-8")


    nb_audio_tot = 0
    nb_video_tot = 0
    nb_annotations_tot = 0
    
    id1 = 0
    id2 = 0

    # parsing du fichier xml pangloss
    for id_oai, record in dico_metadata.items():
        
        objetRecord = record
        
        datestamp = objetRecord.datestamp
        datestamp = datetime.datetime.strptime(datestamp, '%Y-%m-%d')
        

        oai = id_oai.replace("oai:crdo.vjf.cnrs.fr:", "")

        subject = ""
        # liste des langues (en général une pour une ressource)
        subj = objetRecord.labelLangue
        
        if len(subj) >0:
            for one_subject in subj:
            
                intitule_subject = ""
                if one_subject[0] is None:
                    one_subject[0] = ""
                if one_subject[1] is None:
                    one_subject[1] = ""
                    
                code_subject = one_subject[0]
                subject = one_subject[1]
               
        
        # code langues de la langue étudiée (en général un pour une ressource)
        code_subject = objetRecord.codeLangue
        
        # récupération du format de la ressource dans un tableau à 2 éléments : par exemple "audio" et "x-wav"
        listFormatRessource = objetRecord.format

        # identifiant DOI
        doi = objetRecord.doiIdentifiant
        doi = doi.lower()
        # identifiant ARK et handle (dans un tableau)
        ids = objetRecord.identifiant_Ark_Handle
            
  
         # url originale ressource
        url_originale = objetRecord.urlOriginale
        url_diffusion = objetRecord.urlDiffusion

        
        if url_originale == "" and url_diffusion != "":
            url_originale = url_diffusion
            
        if url_diffusion == "" and url_originale != "":
            url_diffusion = url_originale
        
        url_temp = url_diffusion.split('/')
        nom_fichier = url_temp[-1]
       
       
         # type ressource général
        type_ressource = objetRecord.typeRessourceGeneral
        
        type_annotation = ""
        type_annot = objetRecord.typeAnnotation
        if type_ressource == "Text":
            if type_annot == "primary_text":
                type_annotation = "text"
            elif type_annot == "lexicon":
                type_annotation = "wordlist"
            else:
                type_annotation = "text"
            type_ressource = type_annotation
       
        # numéro de version de la ressource
        version = objetRecord.version
        if version == '':
            version = '0'
      
        
         # annotation originale
        originale_annotation = objetRecord.originaleAnnotation


        droit_acces = objetRecord.droitAccess
        if droit_acces == "Freely accessible":
            access_right = "0"
        elif droit_acces == "Access restricted (password protected)":
            access_right = "1"
            
        
        if subject == language_name and type_annotation == 'text':
            nb_annotations += 1 
           
            if Path(annotations_dir+'/'+nom_fichier).is_file():
                print (nom_fichier)
                tree = ETree.parse(annotations_dir+'/'+nom_fichier)
                root = tree.getroot()
            
                num_phrase = 0
                os.makedirs("results", exist_ok=True)
                with open("results/"+nom_fichier, 'wb') as f:
                    f.write('<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'.encode('UTF-8'))
                    f.write('<!DOCTYPE TEXT SYSTEM "https://cocoon.huma-num.fr/schemas/Archive.dtd">\n'.encode('UTF-8'))

                    if root.find(".//S"):
                        
                        # parsing du fichier d'annotation xml pangloss
                        for element in root.findall(".//S"):
                            num_phrase += 1
                           
                            new = ETree.Element("DOI")
                            new.text = 'https://doi.org/'+doi+'#S'+str(num_phrase)
                            element.append(new)
                        tree.write(f, 'UTF-8')
                    else:
                        error_file.write("fichier "+nom_fichier+" : pas de découpage en phrase"+" \n\n")
                    
                     
            else:
                error_file.write("fichier "+nom_fichier+" : fichier introuvable"+" \n\n")
                     
    print (nb_annotations)      
    
    error_file.close()
    
    
    
  


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

  
    parser.add_argument('--language', type=str, required=True,
                         help="language (corpus) for which the dois will be added in the annotation files")
    parser.add_argument('--path_metadata', type=str, required=True,
                         help="Path of the xml metadata file")
    parser.add_argument('--path_annotations', type=str, required=True,
                         help="Path of the annotations files")
    
    args = parser.parse_args()
    insert_doi_in_annotations(args)


