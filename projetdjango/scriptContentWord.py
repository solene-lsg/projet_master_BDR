#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetbdr.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import os
import re
import string
import copy

import django
django.setup()
from appli.models import Content, Word, Conversation
from django.db import DataError
from date import daterep, date1  # Fonctions définies dans date.py

stopwords = {'ourselves', 'us','hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having',
             'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off',
             'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his',
             'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up',
             'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why',
             'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i',
             'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than',
             'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 'u', 'v', 'w', 'x', 'y', 'z'}

def scriptContentWord(directory):
    """
    Remplir les tables Content et Word en parcourant les mails de la base
    """
    #regex
    date_mail=re.compile(r"(?<=Date:\s).*?(?= \(...)")
    sent_mail=re.compile(r"(?<=Sent:\s)(\s*)(.*? (AM|PM))")

    file_name=re.compile(r"(?<=X-FileName: ).*")
    file_name_rep=re.compile(r"(?<= << File:).*")

    WORD=[]
    c=0 # compteur de conversations
    a=1 # compteur de mails : id de Content
    n=1 # compteur de mots
    for root, dirs, files in os.walk(directory):
        for file in files:
            c+=1
            print(file)
            if file.endswith(''):
                print('---- Mail/Conversation',c,'----')
                fichier=os.path.join(root, file)

            with open(fichier,"r",encoding="utf-8") as file:
                liste = []                                              # Lignes de tout le fichier
                liste_dict=[]                                           # Liste de dictionnaires
                global_dict={}                                          # Dictionnaire de mots avec leurs occurences pour la conversation

                for line in file:
                    liste.append(line) 

                textes = " ".join(str(l) for l in liste) 
                mails=re.split('-----Original Message-----',textes)    
        
                k=0
                for m in mails: 
                    k+=1
                    liste_content=[]
                    i=0
                    mail=m.lstrip()
                
                    if k==1:  # Premier mail
                        
                        filename1=file_name.search(mail) 
                        date=date_mail.search(mail)

                        if filename1:  
                            filename=True
                        else:
                            filename=False
                        
                        if date:    
                            datemail=date.group()
                            datemail=date1(datemail)
                    
                    else:  # Mails réponses
                        filenamerep1=file_name_rep.search(mail)
                        sent=sent_mail.search(mail)
                        
                        if filenamerep1:
                            filename=True
                        else:
                            filename=False
                        
                        if sent: #date
                            if sent.group() != '' and sent.group() != '\s':
                                date_sent=sent.group(2)
                                datemail=daterep(date_sent)
                            else :
                                datemail=datemail   
                    
                    
                    mail1=mail.split('\n')
                    
                    # Recherche la première ligne non blanche du corps du mail
                    while mail1[i] != ' ' and i!=len(mail1)-1:
                        i+=1
                    L = mail1[i+1:]
                    content = "".join(str(j) for j in L)

                    #NOMBRE DE MOTS
                    ponct = string.punctuation                      # Ensemble des ponctuations
                    content_word=copy.copy(content)                 # Copie du content pour le garder pour la table Content
                    
                    for p in ponct:                                 # Parcourt toutes les ponctuations pour les supprimer
                        content_word = content_word.replace(p, " ")
                        content_word=content_word.lower()
                    
                    contentword = re.sub(r'[0-9]+', '', content_word)   # Supprime les nombres
                    
                    numberwords=contentword.split()                     # Liste contenant les mots d'un mail
                    number_words=len(numberwords)                       # Nombre de mots du mail
                    
                    # Mots clés
                    keyword = [word for word in numberwords if word not in stopwords] # Suppression des stopwords
                    
                    # Occurences
                    dict = {}
                    for w in keyword:
                        if w in dict:
                            dict[w] = dict[w] + 1
                        else:
                            dict[w] = 1
                    
                    # Ajoute le dictionnaire à la liste_dict de la conversation
                    liste_dict.append(dict)
                    
                    for d in liste_dict:
                        global_dict.update(d)   # Mise à jour du dictionnaire

                    liste_content.append((a,c,content,number_words,filename,datemail))
                    
                    # Insertion dans Content
                    key=Conversation.objects.get(conversation_id=c) # Récupérer la clé étrangère de conversation
                    try:
                        current_content = Content(conversation_id=key,content=content,number_words=number_words,filename=filename,date_mail=datemail)
                        current_content.save()
                    except DataError:
                        content=content[:1000]
                        current_content = Content(conversation_id=key,content=content,number_words=number_words,filename=filename,date_mail=datemail)
                        current_content.save()
                    a+=1
                    
                    # Liste de tuples contenant les mots et leurs occurences
                    liste_dico = global_dict.items()
                    liste_dico = list(liste_dico)
                
                    for i in liste_dico:
                        WORD.append((n,c,i[0],i[1]))
                        n+=1

                # Insertion dans la table Word
                for j in WORD:
                    key=Conversation.objects.get(conversation_id=j[1])
                    current_word=Word(conversation_id=key,keyword=j[2],occurence=j[3])
                    current_word.save()