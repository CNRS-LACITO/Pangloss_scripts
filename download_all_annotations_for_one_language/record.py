import xml.etree.ElementTree as ET

DOI_PANGLOSS = "10.24397/Pangloss"

class Record:
    """
    Classe qui génère des objets record pour une ressource du fichier de métadonnées de la collection Pangloss (enregistrement audio, vidéo, fichier d'annotations, EGG etc etc)
    moissonnées de l'entrepôt oai-pmh Cocoon (https://cocoon.huma-num.fr/)
    Contient la méthode __init__ qui est constructeur d'objet de la classe Record

    """

    def __init__(self, datestamp, doiIdentifiant, identifiantOAI, publisherInstitution, format, dateCreation, dateMiseEnLigne, duree, titre,
                 codeXmlLangTitre, titresSecondaire, codeXmlLangTitreSecondaire, droits, licence, contributeurs, droitAccess,
                 codeLangue, labelLangue, languesEntendues, sujets, labelType, typeRessourceGeneral, typeAnnotation, isRequiredBy,
                 requires, relation, identifiant_Ark_Handle, urlOriginale, urlDiffusion, version, originaleAnnotation, abstract, tableDeMatiere, description,
                 labelLieux, codeLieu, longitudeLatitude, pointCardinaux):
        """
        Constructeur d'objet de la classe Record

        Contient des attributs avec des valeurs par défaut (setSpec, publisher, hostingInstitution)
        Contient aussi des attributs avec des valeurs issues des éléments composant la balise record

        :param datestamp: date de modification des metadonnées <oai:datestamp>
        :type datestamp: str
        :param doiIdentifiant: identifiant DOI présent dans la balise <dc:identifier>
        :type doiIdentifiant : str
        :param identifiantOAI: identifiant OAI présent dans la balise <oai:identifier>
        :type identifiantOAI: str
        :param publisherInstitution: valeur par défaut
        :type publisherInstitution: str
        :param format: format de la ressource. Elémént présent dans la balise <dc:format>
        :type format: list
        :param dateCreation: année de création de la ressource. Elément présent dans la balise <dcterms:created>
        :type dateCreation: str
        :param dateMiseEnLigne: année de publication. Elément présent dans la balise <dcterms:available>
        :type dateMiseEnLigne: str
        :param duree: durée de la ressource. Elément présent dans la baise <dcterms:extent>
        :type duree: str
        :param titre: titre de la ressource. Elément présent dans la balise <dc:title>
        :type titre: str
        :param codeXmlLangTitre: code XML du titre. Attribut de la balise <dc:title>
        :type codeXmlLangTitre: str
        :param titresSecondaire: titre alternatif de la ressource. Elément présent dans la balise <dcterms:alternative>
        :type titresSecondaire: list
        :param codeXmlLangTitreSecondaire: code XML du titre secondaire. Attribut de la balise <dcterms:alternative>
        :type codeXmlLangTitreSecondaire: str
        :param droits: personne qui détient les droits sur la ressource. Elément présent dans la balise <dc:rights>
        :type droits: str
        :param licence: type de licence concernant les droits. Elément présent dans la balise <dcterms:licence>
        :type licence: str
        :param contributeursDoi: nom des contributeurs de la ressource. Eléments convertis à partir de la liste des contributeurs
        :type contributeursDoi: list
        :param droitAccess: description des droits d'acces à la ressource. Elément présent dans la balise <dcterms:accessRights>
        :type droitAccess: str
        :param languesEntendues: l'intitulé des langues ainsi que leur code langue des langues entendues dans l'enregistrement. Elément présent dans la balise <dc:language>
        :type languesEntendues: list
        :param labelLangue: l'intitulé de la langue principale de la ressource et son code langue. Elément présent dans la balise <dc:subject>
        :type labelLangue: list
        :param sujets: les mots clés et les attribut xml:lang. Elément présent dans la balise <dc:subject>
        :type sujets: list
        :param labelType: le type de la ressource. Elément présent dans l'attribut olac:code de la balise <dc:type> où xsi:type = olac:discourse-type
        :type labelType: str
        :param typeRessourceGeneral: type général de la ressource. Elément présent dans la balise où xsi:type = dcterms:DCMIType
        :type typeRessourceGeneral: str
        :param typeAnnotation: le type des annotations lexicon ou primary_text. Elément présent dans la balise <dc:type>
        :type typeAnnotation: str
        :param isRequiredBy: l'URI de la ressource qui appelle la ressource actuelle. Elément présent dans la balise <dcterms:isRequiredBy>
        :type isRequiredBy: list
        :param requires: l'URI de la ressource qui est appellé par la ressource actuelle. Elément présent dans la balise <dcterms:requires>
        :type requires: list
        :param relation: l'URI de la ressource qui a une relation avec cette ressource (autre que requires ou isRequiredBy). Elément présent dans la balise <dc:relation>
        :type relation: list
        :param identifiant_Ark_Handle: les identifiants ark et handle.Elément présent dans la balise <dc:identifier>
        :type identifiant_Ark_Handle: list
        :param urlOriginale: lien URL du fichier original
        :type urlOriginale: str
        :param urlDiffusion: lien URL du fichier de diffusion
        :type urlDiffusion: str
        :param  version: numéro de version de la ressource
        :type version: str
        :param originaleAnnotation: format original des annotations
        :type originaleAnnotation: str
        :param abstract: le résumé descriptif. Elémént présent dans la balise <dcterms:abstract>
        :type abstract: list
        :param tableDeMatiere:sommaire. Elément présent dans la balise <dcterms:tableOfContents>
        :type tableDeMatiere: list
        :param description: description de la ressource. Elément présent dans la balise <dc:description>
        :type description: list
        :param labelLieux: le nom du lieu. Elément présent dans la balise <dcterms:spatial>
        :type labelLieux: list
        :param codeLieu: le code à 2 lettres du lieu. Elément présent dans la balise <dcterms:spatial>
        :type codeLieu: str
        :param longitudeLatitude: les 2 valeurs de la longitude et latitude. Eléments présents dans la balise <dcterms:Point>
        :type longitudeLatitude: list
        :param pointCardinaux: les 4 valeurs des points cardinaux. Eléments présents dans la balise <dcterms:Box>
        :type pointCardinaux: list
        """
        self.datestamp = datestamp
        self.doiIdentifiant = doiIdentifiant
        self.identifiantOAI = identifiantOAI
        self.setSpec = "Linguistique"
        self.publisher = "Pangloss"
        self.publisherInstitution = publisherInstitution
        self.hostingInstitution = ["COllections de COrpus Oraux Numériques", "Huma-Num",
                                   "Langues et Civilisations à Tradition Orale",
                                   "Centre Informatique National de l'Enseignement Supérieur"]
        self.format = format
        self.dateCreation = dateCreation
        self.dateMiseEnLigne = dateMiseEnLigne
        self.relatedIdPangloss = DOI_PANGLOSS
        self.duree = duree
        self.titre = titre
        self.codeXmlLangTitre = codeXmlLangTitre
        self.titresSecondaire = titresSecondaire
        self.codeXmlLangTitreSecondaire = codeXmlLangTitreSecondaire
        self.droits = droits
        self.licence = licence
        self.contributeurs = contributeurs
        self.droitAccess = droitAccess
        self.codeLangue = codeLangue
        self.labelLangue = labelLangue
        self.languesEntendues = languesEntendues
        self.sujets = sujets
        self.labelType = labelType
        self.typeRessourceGeneral = typeRessourceGeneral
        self.typeAnnotation = typeAnnotation
        self.isRequiredBy = isRequiredBy
        self.requires = requires
        self.relation = relation
        self.identifiant_Ark_Handle = identifiant_Ark_Handle
        self.urlOriginale = urlOriginale
        self.urlDiffusion = urlDiffusion
        self.version = version
        self.originaleAnnotation = originaleAnnotation
        self.abstract = abstract
        self.tableDeMatiere = tableDeMatiere
        self.description = description
        self.labelLieux = labelLieux
        self.codeLieu = codeLieu
        self.longitudeLatitude = longitudeLatitude
        self.pointCardinaux = pointCardinaux

 
