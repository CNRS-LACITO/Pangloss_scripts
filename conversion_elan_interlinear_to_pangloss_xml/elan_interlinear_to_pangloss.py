#C:\Python\Python36-32


import sys
import re
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter.filedialog import *
from functools import partial
import os.path
import tkinter.font as tkFont

# from messagefactory import Message



def elan_to_pangloss(repertoire):
    num=1
    ref=""
    content=""
    start=""
    end=""
    transcription_phono=""
    transcription_phone=""    
    who = ""
    translation_en=""
    translation_fr=""
    translation_autre=""
    words=""
    gloses=""
    liste_audio = []
    liste_morphs = []
    liste_gloses = []
    liste_mots = []
    liste_mots_morphs = []
    id_phrase = 0
    mot_morphs = []
    mot_gloses = []
  

    
    for element in os.listdir(repertoire):
        if element.endswith('.txt'):        
            
            # on extrait le nom du fichier sans son extension
            expression = re.compile(r"(.*)\.(.*)")
            result_regex=expression.search(element)
            file_name=result_regex.group(1)
            extension=result_regex.group(2)
            nom_fichier=element[:-4]
            print ('fichier : ',nom_fichier)
            
            if not os.path.exists('out'):
                os.makedirs('out')
            
            # on ouvre le fichier et on écrit au moin l'en tête xml pour un texte 
            with open('out/'+nom_fichier+".xml", "w" ,encoding='utf8') as file_out:
                
                        
                    num = 1
                    file_out.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
                    file_out.write("<!DOCTYPE TEXT SYSTEM \"https://cocoon.huma-num.fr/schemas/Archive.dtd\">\n")
                    file_out.write("<TEXT id=\'"+nom_fichier+"\' xml:lang='***'>\n")

                    file_out.write("<HEADER></HEADER>\n")
                    
                    # indiquer encodage du fichier a traiter
                    with open(repertoire+'/'+element, "r" ,encoding='utf8') as f:
                        for line in f:
    
                            result_regex=re.search(r"(.*?)\t(.*)", line)
                            print("**", repr(line))
                    
                            if len(liste_audio)>1:
                                id_phrase+=1
                                print (liste_audio)
                                    
                                # si on a deux personnes qui parlent on les distingue avec le contenu de l'attribut who
                                if (transcription_phono != ""):
                                        
                                    if who !="":
                                        file_out.write("<S id=\'S"+str(num)+"\' who=\'"+who+"\'>\n")
                                    else:
                                        file_out.write("<S id=\'S"+str(num)+"\'>\n")
                                        
                                    if liste_audio !="": 
                                        file_out.write("<AUDIO start=\'"+liste_audio[0]+"\' end=\'"+liste_audio[1]+"\'/>\n")
                                     
                                    if transcription_phono!="":
                                        file_out.write("<FORM kindOf='phono'>"+transcription_phono+"</FORM>\n")
                                        
                                    if transcription_phone!="":
                                        file_out.write("<FORM kindOf='phone'>"+transcription_phone+"</FORM>\n")    
                                        
                                    if translation_fr!="": 
                                        file_out.write("<TRANSL xml:lang='fr'>"+translation_fr+"</TRANSL>\n")
                                        
                                    if translation_en!="": 
                                        file_out.write("<TRANSL xml:lang='en'>"+translation_en+"</TRANSL>\n")
                                      
                                    if translation_autre!="":
                                        file_out.write("<TRANSL xml:lang='tr'>"+translation_autre+"</TRANSL>\n")
                                      
                                    num += 1
                                        
                                        # if liste_morphs!="" and liste_gloses=="": 
                                            # for mot in liste_morphs:
                                                # file_out.write("<W>"+str(mot)+"</W>\n")
                                              
                                               
                                    # mot et gloses du speaker
                                    if liste_morphs != "" and len(liste_gloses) == 0:
                                           
                                        for j in range(0,len(liste_mots_morphs)):
                                                  
                                                    
                                            file_out.write("<W>\n")
                                            mot_morphs = liste_mots_morphs[j].split('-')
                                            
                                            
                                            mot = ""
                                            if liste_mots !="":
                                                mot = liste_mots[j]
                                                file_out.write("<FORM>"+mot+"</FORM>\n")
                                                
                                                    
                                            for i in range(0,len(mot_morphs)):
                                                morphem=re.sub('<','&lt;',mot_morphs[i])
                                                file_out.write("<M>\n")
                                                file_out.write("<FORM>"+morphem+"</FORM>\n")
                                                file_out.write("</M>\n")
                                            file_out.write("</W>\n")
                                                        
                                    elif len(liste_morphs) > 0 and len(liste_gloses) > 0: 
                                               
                                        emp=0
                                        for j in range(0,len(liste_mots_morphs)):
                                            # print ("Mot_morphs :", liste_mots_morphs)
                                            # print ("All_gloses :", liste_gloses)
                                            file_out.write("<W>\n")
                                            
                                            mot_morphs = liste_mots_morphs[j].split('-')
                                            
                                            
                                            mot = ""
                                            print ("liste mots : ", mot_morphs)
                                            
                                            if liste_mots !="":
                                                
                                                mot = liste_mots[j]
                                                file_out.write("<FORM>"+mot+"</FORM>\n")
                                            
                                            
                                                  
                                            if mot_morphs != "" and liste_gloses != "":
                                                for i in range(0,len(mot_morphs)):
                                                    print ('emp : ', emp)
                                                    morphem=re.sub('<','&lt;',mot_morphs[i])
                                                    glose = re.sub('<','&lt;',liste_gloses[emp])
                                                    
                                                    
                                                    file_out.write("<M>\n")
                                                    file_out.write("<FORM>"+morphem+"</FORM>\n")
                                                    file_out.write("<TRANSL>"+glose+"</TRANSL>\n")
                                                    file_out.write("</M>\n")
                                                    emp+=1
                                                    
                                            file_out.write("</W>\n")
                                       
                                    elif len(liste_mots) > 0 and liste_mots_morphs == "" and len(liste_mots_gloses)  == "":
                                        print ("Ici :", liste_mots)
                                        
                                        emp=0
                                        if liste_mots != "" and liste_gloses != "":
                                            for i in range(0,len(liste_mots)):
                                                
                                                mot=re.sub('<','&lt;',liste_mots[i])
                                                glose = re.sub('<','&lt;',liste_gloses[emp])
                                                    
                                                
                                                file_out.write("<W>\n")
                                                file_out.write("<FORM>"+mot+"</FORM>\n")
                                                file_out.write("<TRANSL>"+glose+"</TRANSL>\n")
                                                file_out.write("</W>\n")   
                                                emp+=1
                                                 
                                       
                                file_out.write("</S>\n")    

                                champ=""
                                content=""
                                start=""
                                end=""
                                transcription_phono=""
                                transcription_phone=""
                                who = ""
                                translation_en=""
                                translation_fr="" 
                                translation_autre=""                                 
                                liste_mots = []                                    
                                liste_morphs = []
                                gloses_supp = []
                                liste_gloses = []
                                liste_mots2 = []                                    
                                liste_morphs2 = []
                                liste_gloses2 = []
                                liste_audio = []
                                liste_mots_morphs = []
                                    
                            elif result_regex is not None:
                                
                                champ=result_regex.group(1)
                                content=result_regex.group(2)
                                content=re.sub('<','&lt;',content)
                                content=re.sub('>','&gt;',content)
                                
                                # Détection des phrases
                                # if "REF" in champ:
                                    # print ('phrase', num)
                                    # ref = num
                                    # id_phrase = content
                                    
                                    
                                # Récupération de la transcription de la phrase
                                if champ == "tx":
                                    transcription_phono=content  
                                    transcription_phono=re.sub('\t+',' ',transcription_phono)
                                    transcription_phono=re.sub('\s+',' ',transcription_phono)
                                    
                                # Récupération de la transcription de la phrase
                                if champ == "tx_phntc":
                                    transcription_phone=content  
                                    transcription_phone=re.sub('\t+',' ',transcription_phone)
                                    transcription_phone=re.sub('\s+',' ',transcription_phone)
                                    
                                 
                                if champ == "ft_en" or champ == "ft_eng":
                                    # print ('traduction en')
                                    translation_en=content
                                    translation_en=re.sub('\t+',' ',translation_en)
                                    translation_en=re.sub('\s+',' ',translation_en)
                                    translation_en=re.sub('<','&lt;',translation_en)
                                    translation_en=re.sub('>','&gt;',translation_en)
                                  
                                if champ == "ft":
                                    # print ('traduction fr')
                                    translation_fr=content
                                    translation_fr=re.sub('\t+',' ',translation_fr)
                                    translation_fr=re.sub('\s+',' ',translation_fr)
                                    translation_fr=re.sub('<','&lt;',translation_fr)
                                    translation_fr=re.sub('>','&gt;',translation_fr)
                                    
                                if champ == "Phrase Free Translation":
                                    # print ('traduction autre')
                                    translation_autre=content
                                    translation_autre=re.sub('\t+',' ',translation_autre)
                                    translation_autre=re.sub('\s+',' ',translation_autre)
                                    translation_autre=re.sub('<','&lt;',translation_autre)
                                    translation_autre=re.sub('>','&gt;',translation_autre)

                                    
                                
                                
                                    
                                # Récupération des mots au niveau des morphèmes (avec - indiqué pour pouvoir recréer le mot)
                                if champ == "mb":  
                                    morphems=content
                                    
                                    liste_morphs = morphems.split('\t')
                                    
                                    morphems=re.sub('\t-','-',morphems)
                                    morphems=re.sub('-\t','-',morphems)
                                    morphems=re.sub('--','-',morphems)
                                   
                                   
                                  
                                    # morphems=re.sub('-','',morphems)
                                    morphems=re.sub(',','',morphems)
                                    
                                    liste_mots_morphs = morphems.split('\t')
                                                                  
                                    
                                # Récupération des gloses au niveau des morphèmes
                                if champ == "ge":
                                    gloses=content
                                    morphems=content
                                   
                                    
                                    # gloses=re.sub('-','',gloses)
                                    gloses=re.sub(',','',gloses)
                                       
                                    liste_gloses = gloses.split('\t')

                               
                                # Récupération des mots (avec indication de morphème par un -) s au niveau des mots
                                if champ == "mot": 
                                     
                                
                                    morphems=content
                                    morphems=re.sub('--','-',morphems)
                                    morphems=re.sub(',','',morphems)
                                    
                                    liste_mots = morphems.split('\t')
                                
                                         
                                # Récupération des gloses au niveau des morphèmes
                                if champ == "ge-fr@SP":
                                    gloses_supp=content
                                    gloses_supp=re.sub('=','=-',gloses_supp)
                                    # gloses_supp=re.sub('-','\t',gloses_supp)
                                     
                                    gloses_supp=re.sub('-','',gloses_supp)
                                    gloses_supp=re.sub(',','',gloses_supp)
                                      
                                    liste_gloses_supp = gloses_supp.split('\t')
                                        
                                    
                
                                        
                                    
                                # Récupération des timecode
                                # TC	0.601 - 4.218
                                if champ == "TC" and (transcription_phono != ""):
                                    
                                    content=re.sub('\t+',' ',content)
                                    content=re.sub('\s+','',content)
                                    liste_audio = content.split('-')
                                    start= liste_audio[0]
                                    end= liste_audio[1]
                                    start = start.replace(',', '.')
                                    end = end.replace(',', '.')
                                    # print (start, ' ', end)  



                    file_out.write("</TEXT>")
                    
                    file_out.close()



       
 
 
repertoire=sys.argv[1]

# appel de la fonction avec les arguments nécessaires 
elan_to_pangloss(repertoire)

