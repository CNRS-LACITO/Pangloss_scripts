#C:\Python\Python36-32

# Lancement du script :  python  emplacement_fichier.txt


import sys
import re
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
from functools import partial
import os.path
import datetime
# from messagefactory import Message


                    
# Fonction principale (unique pour l'instant)   
def excel_to_xml_metadata(file):

    # Mettre REP_CHERCHEUR à **nom_chercheur** : nom de famille uniquement
    REP_CHERCHEUR = '****' 
     

    # Mettre CODE_PAYS à ** ou 2 lettres du code ISO
    CODE_PAYS = '**' 
     
      
      
      
      
      
    # on extrait le nom du fichier sans son extension
    expression = re.compile(r"(.*)\.(.*)")
    result_regex=expression.search(file)
    file_name_metadata=result_regex.group(1)
    extension=result_regex.group(2)
    nom_fichier=file[:-4]
    
    file_name_metadata = re.sub(' ','_',file_name_metadata)
    
    # Le fichier de sortie des métadonnées portera le même nom que le fichier txt pris en entrée. Extension en .xml au lieu de .txt
    file_out = file_name_metadata +'.xml'
    
    # Affichage dans la console du nom du fichier de métadonnées xml
    print ('file out : ',file_out)
     
   
    # Ouverture du fichier de métadonnées xml en écriture
    with open(file_out, "w" ,encoding='utf8') as file_out:
        
        num = 1
        
        # Définition de la balise principale du catalogue
        file_out.write("<crdo:catalog xmlns:olac=\"http://www.language-archives.org/OLAC/1.1/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:crdo=\"http://crdo.risc.cnrs.fr/schemas/\" xmlns:dcterms=\"http://purl.org/dc/terms/\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xsi:schemaLocation=\"http://cocoon.huma-num.fr/schemas/ http://cocoon.huma-num.fr/schemas/metadata.xsd\">\n")
        
        
       # Ouverture en lecture du fichier texte issu de l'exportation du fichier excel contenant la description des données
        with open(file, "r" ,encoding='utf8') as f:
            
            # Affichage dans la console du nom du fichier texte duquel toutes les informations de métadonnées seront issues
            # print ('file in : ', file)
            
            # Parcours de chaque ligne du fichier texte
            for line in f:
                
                # Remplacement de caractères interdits
                line = re.sub('&','&amp;',line)
                
                champs = ''
                
                # Initialisation des variables balises
                balise_title = ''
                balise_alternative = ''
                balise_subject = ''
                balises_languages = ''
                balise_spatial_free = ''
                balise_spatial_lat_long = ''
                balise_created = ''
                balises_contributors = ''
                balises_contributors_xml = ''
                balise_extent = ''
                balise_description = ''
                balise_publisher = ''
                balise_access_rights = ''
                balise_licence = ''
                balise_copyright = ''
                balise_moissonnage = ''
                balise_collection = ''
                balise_required_by = ''
                balise_requires = ''
                balise_linguistic_type = ''
                balise_discourse_type = ''
                balise_source = ''
               
                # Initialisation de variables autres
                required_by_temp = ''
                liste_required_by = ''
                publisher = ''

                 # Formatage de la date du jour
                date = datetime.datetime.now()
                date_today = '{:%Y-%m-%d}'.format(date)  
                 
                # Chaque champ du fichier excel est récupéré et mis dans un tableau nommé champs
                champs = line.split("\t")

                
                # print (len(champs))
                # Vérification qu'il existe bien les 26 champs requis (vides ou non) (le premier champ est 0 et le dernier 25 donc on a 26 champs)
                if len(champs) >= 25:
                    
                    # Récupération du contenu du tableau dans des variables afin d'effectuer des traitements individuels
                    file_name_temp = champs[2]
                    title_temp = champs[3]
                    alternative_temp = champs[4]
                    subject_temp = champs[5]
                    languages_temp = champs[6]
                    spatial_free_temp = champs[7]
                    lat_temp = champs[8]
                    long_temp = champs[9]
                    created_temp = champs[10]
                    depositor_temp = champs[11]
                    researchers_temp = champs[12]
                    speakers_temp = champs[13]
                    sponsors_temp = champs[14]
                    others_contributors_temp = champs[15]
                    extent_temp = champs[16]
                    description_temp = champs[17]
                    publisher_temp = champs[18]
                    access_rights_temp = champs[19]
                    licence_temp = champs[20]
                    copyright_temp = champs[21]
                    collection_temp = champs[22]
                    required_by_temp = champs[23]
                    linguistic_type_temp = champs[24]
                    discours_type_temp = champs[25]
                    # source_temp = champs[26]
                    source_temp = ''

                    
                    # Traitement du nom de fichier ; séparation entre le nom et l'extension
                    if file_name_temp != '':
                        file_name_temp_split = file_name_temp.split(".")
                        file_name = file_name_temp_split[0]
                        
                        # file_name contient le nom du fichier concerné et file_extension son extension (qui doit etre audio ou vidéo)
                        file_name = re.sub(' ','_',file_name)
                        file_extension = file_name_temp_split[1]
                         
                        # Traitement du titre de la ressource
                        expression = re.compile(r"(.*)\((..)\)")
                        result_regex = expression.search(title_temp)
                        title = title_temp
                        
                        # Si le titre est écrit dans une langue particulière on indique la langue sinon non
                        if result_regex != None:
                            title = result_regex.group(1)
                            title_langue = result_regex.group(2)
                            balise_title = "<dc:title xml:lang=\""+title_langue.strip()+"\">"+title.strip()+"</dc:title>\n"
                        else:
                            balise_title = "<dc:title>"+title+"</dc:title>\n"
                        
                        
                        # Traitement du titre alternatif
                        expression = re.compile(r"(.*)\((..)\)")
                        result_regex = expression.search(alternative_temp)
                        alternative = alternative_temp
                        
                        if result_regex != None:
                            alternative = result_regex.group(1)
                            alternative_langue = result_regex.group(2)
                            balise_alternative = "<dcterms:alternative xml:lang=\""+alternative_langue.strip()+"\">"+alternative.strip()+"</dcterms:alternative>\n"
                        else:
                            balise_alternative = "<dcterms:alternative>"+alternative+"</dcterms:alternative>\n"
                        
                        subject_temp_split = ''
                        # Traitement de la langue d'étude
                        if ";" in subject_temp:
                            subject_temp_split = subject_temp.split(";")
                        elif "," in subject_temp:
                            subject_temp_split = subject_temp.split(",")
                        else:
                            subject_temp_split = subject_temp.split(";")
                            
                            
                        for subj in subject_temp_split:
                            expression = re.compile(r"(.*)\((.*?)\)")
                            result_regex = expression.search(subj)
                            print (subj)
                            # subject contient le nom de la langue et subject_code le code langue à 3 lettres
                            subject = result_regex.group(1)
                            subject_code = result_regex.group(2)
                        
                            balise_subject += "<dc:subject olac:code=\""+subject_code.strip()+"\" xsi:type=\"olac:language\">"+subject.strip()+"</dc:subject>\n"
                            
                        
                        
                        languages_temp_split = ''
                        # Traitement des différentes langues entendues dans l'enregistrement
                        languages_temp = re.sub('\"','', languages_temp)
                        # languages_temp = re.sub(' ','', languages_temp)
                        
                        if ";" in languages_temp:
                            languages_temp_split = languages_temp.split(";")
                        elif "," in subject_temp:
                            languages_temp_split = languages_temp.split(",")
                        else:
                            languages_temp_split = languages_temp.split(";")
                            
                       # Si l'on a plusieurs langues entendues dans l'enregistrement alors on les sépare en une langue par balise
                          
                        for item in languages_temp_split:
                            expression = re.compile(r"(.*)\((.*)\)")
                            result_regex = expression.search(item)
                            language = result_regex.group(1)
                            language_code = result_regex.group(2)
                            balises_languages += "<dc:language olac:code=\""+language_code.strip()+"\" xsi:type=\"olac:language\">"+language.strip()+"</dc:language>\n"
                            
                        
                        # Traitement du champ libre "spatial"
                        if spatial_free_temp != '':
                            expression = re.compile(r"(.*)\((.*)\)")
                            spatial_free_temp = re.sub('\"','', spatial_free_temp)
                            result_regex=expression.search(spatial_free_temp)
                            spatial_free = ''
                            spatial_free_langue = ''
                            
                            # Si la langue dans laquelle est écrit le lieu n'est pas spécifiée alors on n'indique pas de xml:lang et on considère par défaut qu'il s'agit d'anglais
                            if result_regex != None:
                                spatial_free = result_regex.group(1)
                                spatial_free_langue = result_regex.group(2)
                                balise_spatial_free = "<dcterms:spatial xml:lang=\""+spatial_free_langue.strip()+"\">"+spatial_free.strip()+"</dcterms:spatial>\n"
                            else:
                                spatial_free = spatial_free_temp
                                balise_spatial_free = "<dcterms:spatial>"+spatial_free.strip()+"</dcterms:spatial>\n"                    

                        # Traitement de la latitude et de la longitude pour le champ spatial
                        if lat_temp != '' and long_temp != '':
                            latitude = lat_temp
                            latitude = re.sub(',','.', latitude)
                            longitude = long_temp
                            longitude = re.sub(',','.', longitude)
                            balise_spatial_lat_long = "<dcterms:spatial xsi:type=\"dcterms:Point\">east="+longitude.strip()+"; north="+latitude.strip()+";</dcterms:spatial>\n" 
                        
                        # Traitement de la date de création de la ressource
                        if created_temp != '':
                            balise_created = "<dcterms:created xsi:type=\"dcterms:W3CDTF\">"+created_temp.strip()+"</dcterms:created>\n"
                        
                        # Traitement du deposant
                        if depositor_temp != '':
                            depositor = depositor_temp
                            balises_contributors += "<dc:contributor olac:code=\"depositor\" xsi:type=\"olac:role\">"+depositor.strip()+"</dc:contributor>\n"
                            balises_contributors_xml += "<dc:contributor olac:code=\"depositor\" xsi:type=\"olac:role\">"+depositor.strip()+"</dc:contributor>\n"
                        # Traitement de la liste des chercheurs
                        if researchers_temp != '':
                            researchers_temp = re.sub('\"','', researchers_temp)
                            researchers_split = researchers_temp.split(";")
                            for name in researchers_split:
                                balises_contributors += "<dc:contributor olac:code=\"researcher\" xsi:type=\"olac:role\">"+name.strip()+"</dc:contributor>\n"
                                balises_contributors_xml += "<dc:contributor olac:code=\"researcher\" xsi:type=\"olac:role\">"+name.strip()+"</dc:contributor>\n"
                        # Traitement de la liste des locuteurs
                        if speakers_temp != '':
                            speakers_temp = re.sub('\"','', speakers_temp)
                            speakers_split = speakers_temp.split(";")
                            for name in speakers_split:
                                balises_contributors += "<dc:contributor olac:code=\"speaker\" xsi:type=\"olac:role\">"+name+"</dc:contributor>\n"
                                
                         # Traitement de la liste des sponsors
                        if sponsors_temp != '':
                            sponsors_temp = re.sub('\"','', sponsors_temp)
                            sponsors_split = sponsors_temp.split(";")
                            for name in sponsors_split:
                                balises_contributors += "<dc:contributor olac:code=\"sponsor\" xsi:type=\"olac:role\">"+name.strip()+"</dc:contributor>\n"
                                
                        # Traitement de la liste des autres contributeurs
                        if others_contributors_temp != '' and others_contributors_temp != ';':
                            others_contributors_temp = re.sub('\"','', others_contributors_temp)
                            others_contributors_split = others_contributors_temp.split(";")
                            
                            for item in others_contributors_split:
                                expression = re.compile(r"(.*)\((.*)\)")
                                item = re.sub('\"','',item)
                                result_regex = expression.search(item)
                                
                                contributor_xml = ''
                                contributor = ''
                                contributor_role_xml = ''
                                contributor_role = ''
                                
                                # Détection des contributeurs ainsi que leur rôle et séparation entre contributeur à la ressource audio et contributeur à l'annotation
                                
                                # S'il y a plusieurs contributeurs
                                if result_regex != None:
                                    if (result_regex.group(2) == "annotator" or result_regex.group(2) == "translator" or result_regex.group(2) == "transcriber" or result_regex.group(2) == "data_inputter"):
                                        contributor_xml = result_regex.group(1)
                                        contributor_role_xml = result_regex.group(2)
                                        balises_contributors_xml += "<dc:contributor olac:code=\""+contributor_role_xml.strip()+"\" xsi:type=\"olac:role\">"+contributor_xml.strip()+"</dc:contributor>\n"
                                    else:
                                        contributor = result_regex.group(1)
                                        contributor_role = result_regex.group(2)
                                        balises_contributors += "<dc:contributor olac:code=\""+contributor_role.strip()+"\" xsi:type=\"olac:role\">"+contributor.strip()+"</dc:contributor>\n"
                                        
                                # S'il n'y a qu'un contributeur (donc pas de liste)
                                else:
                                    if (result_regex.group(2) == "annotator" or result_regex.group(2) == "translator" or result_regex.group(2) == "transcriber" or result_regex.group(2) == "data_inputter"):
                                        contributor_xml = others_contributors_temp
                                        balises_contributors_xml += "<dc:contributor olac:code=\""+contributor_role_xml.strip()+"\" xsi:type=\"olac:role\">"+contributor_xml.strip()+"</dc:contributor>\n"
                                    else:
                                        contributor = others_contributors_temp
                                        balises_contributors += "<dc:contributor olac:code=\""+contributor_role.strip()+"\" xsi:type=\"olac:role\">"+contributor.strip()+"</dc:contributor>\n"
                                
                                
                                
                                
                            
                        
                        # Traitement de la durée du fichier multimedia
                        if extent_temp != '':
                            extent_split = extent_temp.split(":")
                            
                            # Mise en forme PT00H00M00S (heures, minutes, secondes)
                            if len(extent_split) == 1:
                               balise_extent += "<dcterms:extent>PT0H0M"+str(extent_split[0])+"S</dcterms:extent>\n"
                            if len(extent_split) == 2:
                                balise_extent += "<dcterms:extent>PT0H"+str(extent_split[0])+"M"+str(extent_split[1])+"S</dcterms:extent>\n"
                            if len(extent_split) == 3:
                                balise_extent += "<dcterms:extent>PT"+str(extent_split[0])+"H"+str(extent_split[1])+"M"+str(extent_split[2])+"S</dcterms:extent>\n"
                       

                        # Traitement de la description
                        if description_temp != '':
                            expression = re.compile(r"(.*)\((..)\)")
                            result_regex=expression.search(description_temp)
                            description = ''
                            description_langue = ''
                            
                            # Si la langue dans laquelle est écrit le lieu n'est pas spécifiée alors on n'indique pas de xml:lang et on considère par défaut qu'il s'agit d'anglais
                            if result_regex != None:
                                description = result_regex.group(1)
                                description_langue = result_regex.group(2)
                                description = re.sub('\"','',description)
                                description_langue = re.sub(' ','',description_langue)
                                balise_description = "<dc:description xml:lang=\""+description_langue.strip()+"\">"+description.strip()+"</dc:description>\n"
                            else:
                                description = description_temp
                                description = re.sub('\"','',description)
                                balise_description = "<dc:description>"+description.strip()+"</dc:description>\n"                    

                        
                        # Traitement du champ publisher
                        if publisher_temp != '':
                            publisher = publisher_temp
                            balise_publisher = "<dc:publisher>"+publisher.strip()+"</dc:publisher>\n"
                        
                        # Traitement du champ access right
                        if access_rights_temp != '':
                            access_rights = access_rights_temp
                            balise_access_rights = "<dcterms:accessRights>"+access_rights.strip()+"</dcterms:accessRights>\n"
                        
                        
                        # Traitement du champ copyright
                        if copyright_temp != '':
                            copyright = copyright_temp
                            balise_copyright = "<dc:rights>Copyright (c) "+copyright.strip()+"</dc:rights>\n"
                        
                        
                        # Traitement du champ collection  
                        if collection_temp != '':
                            collection = collection_temp
                           
                        balise_pangloss = "<dcterms:isPartOf xsi:type=\"dcterms:URI\">oai:crdo.vjf.cnrs.fr:cocoon-af3bd0fd-2b33-3b0b-a6f1-49a7fc551eb1</dcterms:isPartOf>\n"
                     
                        # Traitement du champ licence  
                        if licence_temp != '':
                            licence = licence_temp
                            balise_licence = "<dcterms:license xsi:type=\"dcterms:URI\">"+licence.strip()+"</dcterms:license>\n"
                        else:
                            balise_licence = "<dcterms:license xsi:type=\"dcterms:URI\">http://creativecommons.org/licenses/by-nc-nd/3.0/</dcterms:license>\n"
                            
                        
                        # Traitement du type linguistique
                        if linguistic_type_temp != '':
                            if linguistic_type_temp == 'text': 
                                balise_linguistic_type = "<dc:type xsi:type=\"olac:linguistic-type\" olac:code=\"primary_text\"/>\n"
                            if linguistic_type_temp == 'lexicon': 
                                balise_linguistic_type = "<dc:type xsi:type=\"olac:linguistic-type\" olac:code=\"lexicon\"/>\n"
                        
                        
                        # Traitement du type du discours
                        if discours_type_temp != '':
                            discours_type = discours_type_temp
                            balise_discourse_type ="<dc:type xsi:type=\"olac:discourse-type\" olac:code=\""+discours_type.strip()+"\"/>\n"
                        
                        
                        # Traitement de la source
                        if source_temp != '':
                            source = source_temp
                            balise_source ="<dcterms:medium>"+source.strip()+"</dcterms:medium>\n"
                        
                        
                        
                        # Traitement du champ fichier lié  
                        if required_by_temp != '':
                            required_by = required_by_temp
                            required_by = re.sub('\"','',required_by)
                            required_by = re.sub(' ','',required_by)
                            required_by = re.sub(',',';',required_by)
                            required_by_split = required_by.split(";")
                            liste_required_by = required_by_split
                            
                            # Pour chaque fichier lié on sépare le nom de fichier de son extension
                            for item in required_by_split:
                                file = item
                                one_required_by = item.split ('.')
                                required_by_file = one_required_by[0]
                                required_by_extension = one_required_by[1]
                                
                                # Si l'extension du fichier est du wav mais sans le terme EGG dans le nom de fichier alors on ajoute que le fichier actuel est requis par un fichier sonore et donc on ajoute _SOUND (pour l'identifiant OAI requis par cette ressource)
                                if (required_by_extension == "wav") and not("_EGG" in required_by_file):
                                    required_by_file = required_by_file+"_SOUND"
                                
                                
                                requires_file = file_name
                                requires_extension = file_extension
                                
                                # Si le fichier actuel est bien un fichier wav alors on ajoute que le fichier lié a besoin de ce son et donc on ajoute _SOUND (pour l'identifiant OAI qui requiert cette ressource)
                                if requires_extension == "wav":
                                    requires_file = requires_file+"_SOUND"
                                
                                # S'il n'y a pas le terme _EGG dans le nom du fichier requis alors nous avons surement à faire à un fichier d'annotations (et on n'ajoute pas le _SOUND à l'OAI qui requiert le fichier actuel)
                                if not("_EGG" in required_by_file):
                                    balise_required_by += "<dcterms:isRequiredBy xsi:type=\"dcterms:URI\">oai:crdo.vjf.cnrs.fr:"+required_by_file.strip()+"</dcterms:isRequiredBy>\n"
                                
                                balise_requires = "<dcterms:requires xsi:type=\"dcterms:URI\">oai:crdo.vjf.cnrs.fr:"+requires_file.strip()+"</dcterms:requires>\n"
                        
                        # Si le fichier actuel est du wav alors ajout du format audio et type son
                        if (file_extension == 'wav') or (file_extension == 'Wav') or (file_extension == 'WAV'):
                            balise_format_sound = "<dc:format xsi:type=\"dcterms:IMT\">audio/x-wav</dc:format>\n"
                            balise_type_sound = "<dc:type xsi:type=\"dcterms:DCMIType\">Sound</dc:type>\n"
                            # Emplacement et nom du fichier wav d'origine
                            balise_master = "<dcterms:isFormatOf xsi:type=\"dcterms:URI\">http://cocoon.huma-num.fr/data/"+REP_CHERCHEUR+"/masters/"+file_name+".wav</dcterms:isFormatOf>\n"
                            # Emplacement et nom du fichier dégradé en wav
                            balise_deg_mp3 = "<dc:identifier xsi:type=\"dcterms:URI\">http://cocoon.huma-num.fr/data/"+REP_CHERCHEUR+"/"+file_name+".mp3</dc:identifier>\n"
                        
                           
                            
                        # Sinon si le fichier actuel est de la vidéo mp4 ou mts ajout du format et type video et image animée
                        elif (file_extension == 'mp4') or (file_extension == 'mts'):
                            balise_format_sound = "<dc:format xsi:type=\"dcterms:IMT\">video/mp4</dc:format>\n"
                            balise_type_sound = "<dc:type xsi:type=\"dcterms:DCMIType\">MovingImage</dc:type>\n"
                            # Emplacement et nom du fichier wav d'origine
                            balise_master = "<dcterms:isFormatOf xsi:type=\"dcterms:URI\">http://cocoon.huma-num.fr/data/"+REP_CHERCHEUR+"/masters/"+file_name+".mp4</dcterms:isFormatOf>\n"
                            # Emplacement et nom du fichier dégradé en wav
                            balise_deg_mp3 = "<dc:identifier xsi:type=\"dcterms:URI\">http://cocoon.huma-num.fr/data/"+REP_CHERCHEUR+"/"+file_name+".mp4</dc:identifier>\n"
                        
                            
                        # Code pays à 2 lettres
                        balise_spatial_2_letters = "<dcterms:spatial xsi:type=\"dcterms:ISO3166\">"+CODE_PAYS+"</dcterms:spatial>\n"
                        
                        
                        
                        # Domaine de recherche
                        balise_domain = "<crdo:domain>Linguistique</crdo:domain>\n"
                        
                        # Date de mise en ligne de la ressource
                        balise_available = "<dcterms:available xsi:type=\"dcterms:W3CDTF\">"+date_today+"</dcterms:available>\n"
                        
                            
                        # Ecriture de toutes les balises décrivant cette ressource dans le fichier xml de métadonnées   
                        file_out.write("<crdo:item crdo:datestamp=\""+date_today+"\" crdo:id=\""+file_name+"_SOUND\">\n")    
                        file_out.write(balise_title)    
                        file_out.write(balise_subject)
                        file_out.write(balises_languages)
                        file_out.write(balise_spatial_free)
                        file_out.write(balise_spatial_lat_long)
                        file_out.write(balise_spatial_2_letters)
                        file_out.write(balise_created)     
                        file_out.write(balises_contributors)
                        file_out.write(balise_format_sound)
                        file_out.write(balise_type_sound)
                        file_out.write(balise_extent)
                        file_out.write(balise_deg_mp3)
                        file_out.write(balise_master)
                        file_out.write(balise_publisher)
                        file_out.write(balise_description)
                        file_out.write(balise_access_rights)
                        file_out.write(balise_copyright)
                        file_out.write(balise_licence)
                        file_out.write(balise_moissonnage)
                        file_out.write(balise_pangloss)
                        file_out.write(balise_required_by)
                        file_out.write(balise_linguistic_type)
                        file_out.write(balise_discourse_type)
                        file_out.write(balise_domain)
                        file_out.write(balise_available)
                        file_out.write("</crdo:item>\n\n")
                        
                        
                        
                       
                        # Détection des fichiers liés au son (ou à la vidéo) et création des métadonnées correspondantes
                        if liste_required_by != '':
                            for item in required_by_split:
                                file = item
                                one_required_by = item.split ('.')
                                # Fichier requis et extension du fichier requis
                                required_by_file = one_required_by[0]
                                required_by_extension = one_required_by[1]
                                
                                # Ajout de l'extension _SOUND au nom du fichier lié s'il s'agit de son mais pas d'EGG
                                if (required_by_extension == "wav") and not("_EGG" in required_by_file):
                                    required_by_file = required_by_file+"_SOUND"

                                
                                requires_file = file_name
                                requires_extension = file_extension
                                
                                # Ajout de l'extension _SOUND au nom du fichier actuel en tant que fichier requis par le fichier lié s'il s'agit bien d'un fichier son
                                if requires_extension == "wav":
                                    requires_file = requires_file+"_SOUND"
                               
                             
                                if len(one_required_by) == 2:
                                    linked_filename = required_by_file
                                    extension = required_by_extension
                                    
                                    # Si le fichier lié au fichier actuel est au format xml création des métadonnées décrivant les annotations
                                    if extension == 'xml':
                                        balise_format_xml = "<dc:format xsi:type=\"dcterms:IMT\">text/xml</dc:format>\n"
                                        balise_type_text = "<dc:type xsi:type=\"dcterms:DCMIType\">Text</dc:type>\n"
                                        balise_identifier = "<dc:identifier xsi:type=\"dcterms:URI\">http://cocoon.huma-num.fr/data/"+REP_CHERCHEUR+"/masters/"+file+"</dc:identifier>\n"
                                        
                                        balise_dtd = "<dcterms:conformsTo xsi:type=\"dcterms:URI\">oai:crdo.vjf.cnrs.fr:cocoon-49aefa90-8c1f-3ba8-a099-0ebefc6a2aa7</dcterms:conformsTo>\n"
                                        
                                        
                                        # Ecriture dans le fichier de métadonnées du fichier lié au fichier actuel
                                        file_out.write("<crdo:item crdo:datestamp=\""+date_today+"\" crdo:id=\""+linked_filename+"\">\n")
                                        file_out.write(balise_title)    
                                        file_out.write(balise_subject)
                                        file_out.write(balises_languages)
                                        file_out.write(balise_created)     
                                        file_out.write(balises_contributors_xml)
                                        file_out.write(balise_format_xml)
                                        file_out.write(balise_type_text)
                                        file_out.write(balise_identifier)
                                        file_out.write(balise_dtd)
                                        file_out.write(balise_publisher)
                                        file_out.write(balise_description)
                                        file_out.write(balise_linguistic_type)
                                        file_out.write(balise_discourse_type)
                                        file_out.write(balise_access_rights)
                                        file_out.write(balise_copyright)
                                        file_out.write(balise_licence)
                                        file_out.write(balise_moissonnage)
                                        file_out.write(balise_pangloss)
                                        file_out.write(balise_requires)
                                        file_out.write(balise_domain)
                                        file_out.write(balise_available)
                                        file_out.write("</crdo:item>\n\n")
                                
                                
        # Fermeture de la balise catalogue du fichier xml décrivant toutes les ressources audio et vidéo ainsi que leurs d'annotations liées   
        file_out.write("</crdo:catalog>")  

# Lecture du nom de fichier texte export du excel qui sera utilisé pour créer le fichier xml de métadonnées        
file=sys.argv[1]

# Appel de la fonction  text_to_pangloss avec les arguments nécessaires (le nom du répertoire contenant les fichiers textes Toolbox)
excel_to_xml_metadata(file)

