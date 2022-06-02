from record import Record
import re
import logging
import csv
import os

from collections import defaultdict

NAMESPACES = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms" : "http://purl.org/dc/terms/",
            "olac" : "http://www.language-archives.org/OLAC/1.1/",
            "xsi" : "http://www.w3.org/2001/XMLSchema-instance",
            "oai" : "http://www.openarchives.org/OAI/2.0/",
            "doi" : "http://datacite.org/schema/kernel-4",
            "crdo" : "http://cocoon.huma-num.fr/schemas/",
            
        }

def parseRecord (record):
        """
        Fonction qui parse les éléments xml contenus dans la balise <record> du fichier metadata_pangloss.xml et récupère la valeur des attributs de l'objet
        :param record: les éléments contenus dans la balise <record>
        :type record: élément de la classe 'xml.etree.ElementTree.Element'
        :return Objet contenant comme paramètres les noms des variables qui stockent les valeurs des attributs et des éléments
        :rtype: object
        """
        
       
                

        # --------Parse header--------#

        # extrait l'identifiant OAI
        identifiantOAI = ""
        if record.find('*/oai:identifier', NAMESPACES) is not None:
            identifiantOAI = record.find('*/oai:identifier', NAMESPACES).text
            
        # datestamp
        datestamp = ""
        if record.find('*/oai:datestamp', NAMESPACES) is not None:
            datestamp = record.find('*/oai:datestamp', NAMESPACES).text

        
        # --------Parse metadata-OLAC--------#

        # atteint le noeud olac:olac qui contient tous les autres éléments descriptif
        olac = record.find('*/olac:olac', NAMESPACES)


        # extrait le nom DOI s'il existe. Sinon, doiIdentifiant est vide
        doiIdentifiant = ""
      
        for identifiant in olac.findall('dc:identifier', NAMESPACES):
            if "doi:" in identifiant.text:
                doiIdentifiant_temp = identifiant.text
                doiIdentifiant = doiIdentifiant_temp.replace('doi:','')
                # print ('identifiant doi : ', doiIdentifiant)
                

        # déclaration d'une liste vide publisherInstitution
        publisherInstitution = []
        # parcourt toutes les balises dc:publisher
        for institution in olac.findall('dc:publisher', NAMESPACES):
            # extrait le nom de l'institution et l'ajoute à la liste
            nomInstituion = institution.text
            publisherInstitution.append(nomInstituion)
        
        # le format
        # atteint la balise dc:format
        if olac.find('dc:format', NAMESPACES) is not None:
            # crée une liste qui stocke le contenu de la balise dc:format après avoir séparer la chaine de carractères
            format = olac.find('dc:format', NAMESPACES).text.split("/")

        else:
            format = []

        # la date de création
        # atteint la balise dcterms:created
        if olac.find("dcterms:created", NAMESPACES) is not None:
            # extrait la date
            dateCreation = olac.find("dcterms:created", NAMESPACES).text
        else:
            dateCreation = ""

            
        # la date de mise en ligne
        # atteint la balise dcterms:available
        if olac.find("dcterms:available", NAMESPACES) is not None:
            # extrait la date
            dateMiseEnLigne = olac.find("dcterms:available", NAMESPACES).text
        else:
            dateMiseEnLigne = ""

        # duree
        if olac.find("dcterms:extent", NAMESPACES) is not None:
            duree = olac.find("dcterms:extent", NAMESPACES).text
        else:
            duree = ""

        # titre
        # recupère le contenu de la balise dc:title et le code xml:lang
        if olac.find("dc:title", NAMESPACES) is not None:
            titreElement = olac.find("dc:title", NAMESPACES)
            titre= titreElement.text
            # récupére la valeur de l'attribut xml:lang du titre
            codeXmlLangTitre = titreElement.get('{http://www.w3.org/XML/1998/namespace}lang')
        else:
            titre = ""
            message = "La balise <dc:title> n'existe pas"
            logging.info(message)

        # titre secondaire
        # extrait le titre alternatif et le code xml:lang et les stocke dans une liste
        titresSecondaire = []
        codeXmlLangTitreSecondaire = []
        # pour chaque titre dans les balises dcterms:alternative
        for titreAlternatif in olac.findall('dcterms:alternative', NAMESPACES):
            # ajouter à la liste titresSecondaire le titre
            titreLabel = titreAlternatif.text
            #extrait la valeur de l'attribut xml:lang
            codeXmlLangTitreSecondaire = titreAlternatif.get("{http://www.w3.org/XML/1998/namespace}lang")
            #ajoute à la liste titreLangList le code xml:lang et le titre
            titreLangList = [codeXmlLangTitreSecondaire, titreLabel]
            # ajoute la liste titreLangList comme liste imbriquée à la liste titresSecondaire
            titresSecondaire.append(titreLangList)

        # detenteur des droits
        droits =""
        if olac.find("dc:rights", NAMESPACES) is not None:
            droitsComplet = olac.find("dc:rights", NAMESPACES).text
            if re.match("Copyright [^A-Z]*", droitsComplet):
                droits = re.sub("Copyright [^A-Z]*", '', droitsComplet)
            else:
                message = "Format invalide"
                logging.info(message)

        # licence
        if olac.find('dcterms:license', NAMESPACES) is not None:
            licence = olac.find('dcterms:license', NAMESPACES).text
        else:
            licence = ''

        # les contributeurs. On extrait d'abord les valeurs et les rôles des contributeurs Olac
        contributeursOlac = []
        contributeurs = defaultdict(list)
        # parcourt toutes les balises dc:contributor. Pour chaque balise
        for contributor in olac.findall('dc:contributor', NAMESPACES):
            langLabel = contributor.get('{http://www.w3.org/XML/1998/namespace}lang')
            if langLabel == None:
                    langLabel = ""
            # extrait le rôle du contributeur
            role = contributor.get('{http://www.language-archives.org/OLAC/1.1/}code')
            # extrait le nom du contributeur
            nomPrenom = contributor.text
            unContributeur = [langLabel, nomPrenom]
            contributeurs[role].append(unContributeur)
            
            
            # ajoute le nom et le rôle à contributorList
            contributorList = [nomPrenom, role]
            # ajoute contributorList comme liste imbriquée à liste globale contributeursOlac
            contributeursOlac.append(contributorList)

        # conversion des rôles des contributeurs du OLAC vers contributeur DOI
        contributeursDoi = []
        # parcourt chaque liste imbriquée composée du nom et du role du contributeur de la liste contributeursOlac
        for listeOlac in contributeursOlac:
            # remplace les rôlés ci-dessous par DataCurator
            if "transcriber" in listeOlac[1] or "annotator" in listeOlac[1] or "translator" in listeOlac[1] or "compiler" in listeOlac[1]:
                # crée listeCurator qui stocke le nom du contributeur et le role DataCurator
                listeCurator = [listeOlac[0], "DataCurator"]
                # vérifie que listeCurator n'existe pas dans la liste contributeursDoi pour
                # éviter de rajouter plusieurs fois la même liste avec le même nom et rôle
                if listeCurator not in contributeursDoi:
                    contributeursDoi.append(listeCurator)
            # remplace les rôle ci-dessous par DataCollector. Procédure similaire à celle pour DataCurator
            elif "interpreter" in listeOlac[1] or "recorder" in listeOlac[1] or "interviewer" in listeOlac[1]:
                listeCollector = [listeOlac[0], "DataCollector"]
                if listeCollector not in contributeursDoi:
                    contributeursDoi.append(listeCollector)
            # remplace les rôle ci-dessous par Other. Procédure similaire à celle pour DataCurator
            elif "performer" in listeOlac[1] or "responder" in listeOlac[1] or "singer" in listeOlac[1] or "speaker" in listeOlac[1]:
                listeOther = [listeOlac[0], "Other"]
                if listeOther not in contributeursDoi:
                    contributeursDoi.append(listeOther)
            # remplace le rôle depositor par ContactPerson
            elif "depositor" in listeOlac[1]:
                listeContactPerson = [listeOlac[0], "ContactPerson"]
                # il n'est pas nécessaire de vérifier que le liste existe car ici il n'y a qu'un seul rôle
                contributeursDoi.append(listeContactPerson)
            # remplace le rôle researcher par Researcher
            elif "researcher" in listeOlac[1]:
                listeResearcher = [listeOlac[0], "Researcher"]
                contributeursDoi.append(listeResearcher)
            # remplace le rôle editor par Editor
            elif "editor" in listeOlac[1]:
                listeEditor = [listeOlac[0], "Editor"]
                contributeursDoi.append(listeEditor)
            # remplace le rôle sponsor par Sponsor
            elif "sponsor" in listeOlac[1]:
                listeSponsor = [listeOlac[0], "Sponsor"]
                contributeursDoi.append(listeSponsor)

        # droit d'accès
        droitAccess = ""
        if olac.find("dcterms:accessRights", NAMESPACES) is not None:
            droitAccess = olac.find("dcterms:accessRights", NAMESPACES).text

         # langues entendues dans l'enregistrement
        languesEntendues = []
        for langue in olac.findall('dc:language', NAMESPACES):
            langueAttribut = langue.attrib
            # si la balise subject n'a pas d'attributs, la valeur de l'élement est ajoutée à la liste de mots-cles
            if not langueAttribut:
                continue
            # sinon, si la balise a des attributs
            else:
                # pour chaque clé et valeur du dictionnaire d'attributs
                for cle, valeur in langueAttribut.items():
                    # si la balise subject contient l'attribut type et la valeur olac:langue, recupérer le code et le label de la langue et le code xml:lang de la balise
                    if cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "olac:language":
                        # récupère le code de la langue et l'ajoute à la liste de code
                        codeLanguage = langueAttribut.get('{http://www.language-archives.org/OLAC/1.1/}code')
                        
                        
                        # récupérer dans une liste la valeur de l'attribut xml:lang et le label de la langue et l'ajoute à la liste de labelLangue
                        label = langue.text
                        listeAttribXmlLabel = [codeLanguage, label]
                        languesEntendues.append(listeAttribXmlLabel)

        # récupère le code de la langue principale de la ressource. Crée une liste parce que la balise subject est répétable
        codeLangue = []
        # récupère le label de la langue des corpus
        labelLangue = []
        # récupère des mots-clés sous forme de chaine de caractères et des listes imbriquées de mots-clés et xml:lang
        sujets = []
        
        
        for sujet in olac.findall('dc:subject', NAMESPACES):
            sujetAttribut = sujet.attrib
            # si la balise subject n'a pas d'attributs, la valeur de l'élement est ajoutée à la liste de mots-cles
            if not sujetAttribut:
                sujets.append(sujet.text)
            # sinon, si la balsie a des attributs
            else:
                # pour chaque clé et valeur du dictionnaire d'attributs
                for cle, valeur in sujetAttribut.items():
                    # si la balise subject contient l'attribut type et la valeur olac:langue, recupérer le code et le label de la langue et le code xml:lang de la balise
                    if cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "olac:language":
                        # récupère le code de la langue et l'ajoute à la liste de code
                        code = sujetAttribut.get('{http://www.language-archives.org/OLAC/1.1/}code')
                        codeLangue.append(code)
                        
                        # récupérer dans une liste la valeur de l'attribut xml:lang et le label de la langue et l'ajoute à la liste de labelLangue
                        label = sujet.text
                        codeXmlLangLabel = sujetAttribut.get('{http://www.w3.org/XML/1998/namespace}lang')
                        listeAttribXmlLabel = [code, label]
                        labelLangue.append(listeAttribXmlLabel)
                        
                    # si la balise subject contient l'attribut xml:lang,
                    # et qu'il n'y a pas d'attribut type
                    # récupérer dans une liste la valeur de l'attribut et le contenu de l'élément
                    if cle == "{http://www.w3.org/XML/1998/namespace}lang" and "{http://www.w3.org/2001/XMLSchema-instance}type" not in sujetAttribut:
                        codeXmlLangSujet = valeur
                        motCle = sujet.text
                        listeAttribMot = [codeXmlLangSujet, motCle]
                        # ajout de la liste attribut langue et mot clé à la liste de mots clés
                        sujets.append(listeAttribMot)

        # Le type de ressource: récupère les informations des balises dc:type
        # liste qui récupère le contenu de la balise type et la valeur de l'attribut olac:code et qui vont être affectés à l'élément type en sortie
        labelType = ""
        typeRessourceGeneral = ""
        typeAnnotation = ""
        # déclare un booléen à False
        bool = False
        # partourt toutes les balises dc:type
        for element in olac.findall("dc:type", NAMESPACES):
            # extrait les attributs
            typeAttribut = element.attrib
            # si la balise ne contient pas d'attributs, ajoute le contenu de la balise à la liste de mots-clés (subject)
            if not typeAttribut:
                sujets.append(element.text)
            # sinon, si la balise contient des attributs
            else:
                for cle, valeur in typeAttribut.items():

                    # si la balise contient l'attribut xml:lang
                    if cle == '{http://www.w3.org/XML/1998/namespace}lang':
                        # extrait la valeure de la balise et de l'attribus xml:lang et les ajouter comme liste imbriquée à la liste sujets
                        codeXmlLangSujet = valeur
                        motCle = element.text
                        listeAttribMot = [codeXmlLangSujet, motCle]
                        sujets.append(listeAttribMot)
                   
                    # si la balise contient l'attribut type et la valeur dcterms:DCMIType
                    elif cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:DCMIType":
                        # remplace le contenu MovingImage par Audiovisual
                        if element.text == "MovingImage":
                            typeRessourceGeneral = "Audiovisual"
                        # pour le reste des éléments, typeRessourceGeneral est équivalent du contenu de la ressource
                        else:
                            typeRessourceGeneral = element.text
                            
                    # récupère le contenu de l'atttribut olac:code de la balise dc:type où l'attribut type a comme valeur olac:linguistic-type
                    elif cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "olac:linguistic-type":
                        typeAnnotation = typeAttribut.get('{http://www.language-archives.org/OLAC/1.1/}code')

                    # récupère le contenu de l'atttribut olac:code de la balise dc:type où l'attribut type a comme valeur olac:discourse-type
                    elif cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "olac:discourse-type":
                        labelType = typeAttribut.get('{http://www.language-archives.org/OLAC/1.1/}code')
                        bool = True
                        # la condition est satisfaite et le booléen prend la valeur True

        # sinon afficher "(:unkn)"
        if not bool:
            labelType = "(:unkn)"
            bool = True

        isRequiredBy = []
        for ressource in olac.findall('dcterms:isRequiredBy', NAMESPACES):
            isRequiredBy.append(ressource.text)

        requires = []
        for ressource in olac.findall('dcterms:requires', NAMESPACES):
            requires.append(ressource.text)

        relation = []
        for ressource in olac.findall('dc:relation', NAMESPACES):
            relation.append(ressource.text)

        # lien ark, handle
        identifiant_Ark_Handle = []
        for identifiantAlternatif in olac.findall('dc:identifier', NAMESPACES):
            identifiantAttribut = identifiantAlternatif.attrib
            for cle, valeur in identifiantAttribut.items():
                if cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:URI":
                    if "ark" in identifiantAlternatif.text:
                        identifiantType = "ARK"
                        lienArk = identifiantAlternatif.text
                        listeIdLienArk = [identifiantType, lienArk]
                        identifiant_Ark_Handle.append(listeIdLienArk)
                    if "handle" in identifiantAlternatif.text:
                        identifiantType = "Handle"
                        lienHandle = identifiantAlternatif.text
                        listeIdLienHandle = [identifiantType, lienHandle]
                        identifiant_Ark_Handle.append(listeIdLienHandle)

        #identifiant contenant le lien url d'une ressource en fonction de si c'est le format original ou le format de diffusion
        urlOriginale = ""
        urlDiffusion = ""
        version = ""

        
        
        for urlResource2 in olac.findall('dcterms:isFormatOf', NAMESPACES):

            if urlResource2.text.endswith(".mp4"):
                urlOriginale = urlResource2.text
                break

            if urlResource2.text.endswith(".wav"):
                urlOriginale = urlResource2.text
                break
           
            if urlResource2.text.endswith(".eaf"):
                urlOriginale = urlResource2.text
                break

            if urlResource2.text.endswith(".TextGrid"):
                urlOriginale = urlResource2.text
                break
        

           


           
        for urlResource1 in olac.findall('dc:identifier', NAMESPACES):
           
            if urlResource1.text.endswith(".xml"):
                urlDiffusion = urlResource1.text
                break
        
            if urlResource1.text.endswith(".TextGrid"):
                urlDiffusion = urlResource1.text
                break
        
            if urlResource1.text.endswith(".mp3"):
                urlDiffusion = urlResource1.text
                break

            if urlResource1.text.endswith(".mp4"):
                urlDiffusion = urlResource1.text
                break

            if urlResource1.text.endswith(".pdf"):
                urlDiffusion = urlResource1.text
                break

            if urlResource1.text.endswith(".jpg"):
                urlDiffusion = urlResource1.text
                break

            if urlResource1.text.endswith(".egg"):
                urlOriginale = urlResource1.text
                break

           
        for isformatof_version in olac.findall('dcterms:isFormatOf', NAMESPACES):
            #print(urlResource2.text)
            
            if ".version" in isformatof_version.text:
                version = isformatof_version.text.split(".")[-1]
                version = version.replace("version", "")
                #print (version)
                break


                    
        for identifiant_version in olac.findall('dc:identifier', NAMESPACES):
            #print(identifiant_version.text)
            
            if ".version" in identifiant_version.text:
                version = identifiant_version.text.split(".")[-1]
                version = version.replace("version", "")
                #print (version)
                break

                
        
        
        #format du fichier de l'annotation
        originaleAnnotation = ""
        for identifiantFormatAnnotation in olac.findall('dcterms:isFormatOf', NAMESPACES):
            #extraire le lien du fichier 
            if ".eaf" in identifiantFormatAnnotation.text:
                originaleAnnotation += identifiantFormatAnnotation.text
                break
            if ".trs" in identifiantFormatAnnotation.text:
                originaleAnnotation += identifiantFormatAnnotation.text
                break
            if ".textGrid" in identifiantFormatAnnotation.text:
                originaleAnnotation += identifiantFormatAnnotation.text
                break
            if ".xml" in identifiantFormatAnnotation.text:
                originaleAnnotation += identifiantFormatAnnotation.text
                break
        
        # récupère la description de la balise abstract sous la forme d'une liste avec le contenu de la balise
        # et/ou avec une liste contenant l'attribut langue et le contenu de la balise
        abstract = []
        for contenu in olac.findall("dcterms:abstract", NAMESPACES):
            # récupère les attributs et valeurs d'attributs sous la forme d'un dictionnaire
            abstractAttrib = contenu.attrib

            # si la balise ne contient pas d'attributs, alors ajouter le contenu de l'élément à la liste
            if not abstractAttrib:
                langueAbstract = ""
            # si la balise contient d'attributs (attributs xml:lang d'office), créer une liste avec le code de la langue et le contenu de la balise
            else:
                langueAbstract = abstractAttrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            texteAbstract = contenu.text
                
            listeLangueContenu = [langueAbstract, texteAbstract]
            abstract.append(listeLangueContenu)
        # récupérer le contenu de la balise tableOfContent
        tableDeMatiere = []
        for contenu in olac.findall("dcterms:tableOfContents", NAMESPACES):
            # récupère les attributs et valeurs de la balise sous la forme d'un dictionnaire
            tableAttrib = contenu.attrib
            # si la balise ne contient pas d'attributs, alors ajouter le contenu à la liste
            if not tableAttrib:
                langueTable = ""
            # si la balise contient d'attributs (attributs xml:lang d'office), créer une liste avec le code de la langue et le contenu de la balise
            else:
                langueTable = tableAttrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            texteTable = contenu.text

            listeLangueContenu = [langueTable, texteTable]
            tableDeMatiere.append(listeLangueContenu)   

        # extrait le texte de la description et l'attribut xml:lang si elle existe
        description = []
        for texte in olac.findall("dc:description", NAMESPACES):
            descriptionAttrib = texte.attrib
            if not descriptionAttrib:
                langueDescription = ""
               
            else:
                langueDescription = descriptionAttrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            texteDescription = texte.text

            listeLangueContenu = [langueDescription, texteDescription]
            description.append(listeLangueContenu)

        # liste qui récupère les labels du lieu
        labelLieux = []
        codeLieu = ""
        longitudeLatitude = []
        pointCardiaux = []
        listeLieu = []
        # pour chaque balise dcterms:spatial, on récupère les attributs
        for lieu in olac.findall('dcterms:spatial', NAMESPACES):
            lieuAttrib = lieu.attrib
            # si la balise n'a pas d'attribut, on ajoute à la liste labelLieux le contenu de la balise (le nom nu lieu)
            if not lieuAttrib:
                listeLieu = ["", lieu.text]
                labelLieux.append(listeLieu)
               
            # si la balise contient un attribut xml:lang, on ajoute liste labelLieux le contenu de la balise (le nom nu lieu)
            # cela exclue le contenu des balises dcterms:spatial qui ont des attributs, mais pas xml:lang
            for cle, valeur in lieuAttrib.items():
                if cle == '{http://www.w3.org/XML/1998/namespace}lang':
                    listeLieu = [valeur, lieu.text]
                    labelLieux.append(listeLieu)
                if cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:ISO3166":
                    codeLieu = lieu.text
                # on boucle sur le dictionnaire contenant les attributs
                # récupère les 2 points de la longitude et latitude en une seule chaine de caractères pour le cas où l'attribut est Point
                if cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:Point":
                    pointLieux = lieu.text
                    # transforme la chaine en une liste avec deux éléments :north:valeur latitude et east:valeur longitude
                    long_lat = pointLieux.split(";")

                    # élimine l'espace en trop du contenu texte des deux éléments de la liste (north et east)
                    point1sansEspaces = long_lat[0].strip()
                    point2sansEspaces = long_lat[1].strip()

                    # condition pour régler le problème d'ordre des éléments nord et sud. Récupération des valeurs chiffrées de la longitude et de la latitude
                    if "east" in point1sansEspaces:
                        longitude = point1sansEspaces[5:]
                        latitude = point2sansEspaces[6:]
                    else:
                        longitude = point2sansEspaces[5:]
                        latitude = point1sansEspaces[6:]

                    longitudeLatitude.append(longitude)
                    longitudeLatitude.append(latitude)


                # récupère les 4 points de la longitude et latitude en une seule chaine de caractères pour le cas où l'attribut est Box
                elif cle == "{http://www.w3.org/2001/XMLSchema-instance}type" and valeur == "dcterms:Box":
                    boxLieux = lieu.text
                    # transforme la chaîne en une liste avec quatre éléments : southlimit, northlimit, eastlimit, westlimit
                    sudNordEstWest = boxLieux.split(';')

                    # supression des espaces pour les quatres points
                    sudSansEspace = sudNordEstWest[0].strip()
                    nordSansEspace = sudNordEstWest[1].strip()
                    estSansEspace = sudNordEstWest[2].strip()
                    westSansEspace = sudNordEstWest[3].strip()

                    # récupère uniquement la valeur chiffrée des quatres points
                    sud = sudSansEspace[11:]
                    nord = nordSansEspace[11:]
                    est = estSansEspace[10:]
                    west = westSansEspace[10:]
                    pointCardiaux.append(west)
                    pointCardiaux.append(est)
                    pointCardiaux.append(sud)
                    pointCardiaux.append(nord)

      

        record_object = Record(datestamp, doiIdentifiant, identifiantOAI, publisherInstitution, format, dateCreation, dateMiseEnLigne, duree, titre,
                               codeXmlLangTitre, titresSecondaire, codeXmlLangTitreSecondaire ,droits, licence, contributeurs, droitAccess, codeLangue,
                               labelLangue, languesEntendues, sujets, labelType, typeRessourceGeneral, typeAnnotation, isRequiredBy, requires, relation,
                               identifiant_Ark_Handle, urlOriginale, urlDiffusion, version, originaleAnnotation, abstract, tableDeMatiere,
                               description, labelLieux, codeLieu, longitudeLatitude, pointCardiaux)
        return record_object
