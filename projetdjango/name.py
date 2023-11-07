#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetbdr.settings')
import django
django.setup()

# Fonctions pour récupérer les noms (premier mail et réponses)

def name(names): 
    """
    Traitement d'une ligne de noms (names) pour récupérer les noms des personnes sous forme de liste
    """
    # Regex
    balise=re.compile(r"\</(O|o)=ENRON/.*?\>") 
    balise2=re.compile(r"\<.*?\>")
    balise3=re.compile(r"\<\..*?\>")
    bal=balise.search(names)
    bal2=balise2.search(names) 
    bal3=balise3.search(names)

    point_virgule=re.compile(r";")
    ptvirgule=point_virgule.search(names)
    virgule=re.compile(r",")
    vrg=virgule.search(names)

    address=re.compile(r" [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+") 
    address2=re.compile(r"(.*)@")
    
    add=address.search(names)
    add2=address2.search(names)
    
    names=re.sub(r"""\'|\:|"|@ENRON|\/|\\|\(.*?\)""", "",names)

    if not vrg and not bal:                  
        if bal2 or bal3:
            names=re.sub(r"<\..*?>","",names)
            names=re.sub(r"<.*?>","",names)
            
        if add2:                                       
            names=str.title(re.sub(r'[\._-]', ' ',add2.group(1))).strip() # Pour récupérer le nom dans une adresse mail
            names=names.strip()
            return names
         
        return names

    names=re.sub(r"\.","",names)

    if ptvirgule :
        if vrg:
            names=re.sub(virgule, "", names)
        names=names.split('; ')
        
    if bal3:
        names=re.sub(r"\<\..*?\>","",names)
    
    if bal:     
        
        if add:                                         
            a=re.findall(address,names)
            print(a)
            names=re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"," ",names)
            for ad in a:
                print(ad) 
                ad=ad.replace(ad, ad + r" <balise>")       # Ajouter une balise avant de spliter, et remplacer l'adresse par le nom
                names+=ad
        
        if not vrg:
            names=re.sub(r"<.*?>","",names)
            if add2:   
                return str.title(re.sub(r'[\._-]', ' ',add2.group(1))).strip()
            names=names.strip() 
            return names
            
        if vrg:
            names=re.sub(virgule, "", names) 
            bal2=balise2.search(names) 
            if bal2:  
                names.strip() 
                names=re.split(balise2,names)
            
        else: 
            names=names.strip() 
            names=re.split(balise,names)

    
    elif bal2:
        if vrg:  
            names=re.sub(virgule, "", names)
        names.strip() 
        names=re.split(balise2,names)

    else:
        if vrg:
            names=names.strip() 
            names=re.split(virgule,names)
            
    if names[-1] == '':                     # Retirer le dernier élément si c'est un vide
        del names[-1]
        
    names = [n.strip() for n in names]      # Pour chaque élément, on retire les espaces blancs à gauche et à droite des noms
  
    return names

def namerep(names):
    names=re.sub(r"[\"\']", "",names)  # On supprime les caractères " et '
    names=re.sub(r"\=\s", "",names)    # On supprime les caractères =
    
    crochet=re.compile(r"\[.*?\]")
    cro=crochet.search(names)

    point_virgule=re.compile(r";")
    ptvirgule=point_virgule.search(names)

    virgule=re.compile(r", ")
    vrg=virgule.search(names)
    
    balise=re.compile(r"\</O=ENRON.*?\>")
    
    address2=re.compile(r"(.*)@")
    add2=address2.search(names)

    names=names.strip()

    if add2:                                                
        a=re.findall(address2,names)
        names=re.sub(r"<[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+>"," ",names)
        for ad in a:
            ad=ad.replace(ad, ad[1:len(ad)-1] + r" <balise>") # Ajouter une balise avant de spliter, et remplacer l'adresse par le nom
        names=re.sub(r"@ENRON","",names)
     
    if cro:
        names=re.sub(crochet,"",names)
    
    bal=balise.search(names)
    
    if not (vrg or ptvirgule):
        names=names.strip()
        names=re.sub(r"\>.*", "",names)
        names=re.sub(r"\<","",names)
        names=re.sub(virgule," ",names)
        names=re.sub(r"\=[0-9]*", "",names)
        return [names]
    
    if ptvirgule and not vrg:
        names=names.strip()
        names=re.sub(r"\=[0-9]*", "",names)
        names=re.split('; ',names)
        return names
        
    if not vrg:
        names=names.strip()
        names=re.sub(r"\=[0-9]*", "",names)
        return names
    
    if vrg:
        nb_vrg=vrg.group().count(',')  # On compte le nombre de virgules pour déterminer le format des noms
        
        if ptvirgule and nb_vrg==1:
            names=re.sub(virgule, " ", names)
            names=re.sub(r"\=[0-9]*", "",names)
            names=re.split(r'; ',names)
            return names
        
        if nb_vrg==1:
            names=re.sub(r"\>", "",names)
            names=re.sub(virgule, " ", names)
            names=re.sub(r"\=[0-9]*", "",names)
            return names
        
        if not ptvirgule and not cro and not bal:
            names=re.sub(r"\=[0-9]*", "",names)
            names=re.split(virgule, names)
            return names
        
        if bal:
            names=re.sub(virgule, " ", names)
            names=re.split(balise,names)
            
        if ptvirgule :
            names=re.sub(r"\<.*\>","",names)
            names=re.sub(virgule, " ", names)
            names=re.split(r'; ',names)
        
        else:
            names=re.sub(r"\=[0-9]*", "",names)
            names=re.split(virgule, names)
         
    if names[-1] == '':
        del names[-1]

    if type(names)==list:                      # Eviter un découpage d'un nom par caractère
        names = [n.strip() for n in names]
    
    return names