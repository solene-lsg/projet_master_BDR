#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetbdr.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django
django.setup()

from appli.models import Employee,Address
import xml.etree.ElementTree as ET

#chemin = 'C:/Users/Solène/Documents/Angers/Master1/Semestre2/UE4-OutilsNumeriquesInformatique/BasesDonnéesRelationnelles/Projet/Peuplement/employes_enron.xml'
#path = chemin.encode(encoding="mbcs")
#path1 = path.decode("utf8")

chemin='employes_enron.xml'
    
def readXML(chemin):
    """
    Remplir la table Employee en parcourant les mails de la base
    """
    chemin = str(chemin)
    tree = ET.parse(chemin)
    root = tree.getroot()

    #Employee
    for i in root:                              # Récupérer les données : i = employé
        category=i.get('category')              # Fonction get car c’est un attribut
        lastname=i.find('lastname').text        # Fonction find car pas un attribut et .text pour récupérer le texte entre les balises
        firstname=i.find('firstname').text
        name = firstname + ' ' + lastname       # Concaténation du nom
        mailbox=i.find('mailbox').text

        # Exportation dans la table Employee
        current_employee = Employee(name=name, category=category, mail_box=mailbox) 
        current_employee.save()
        
        #Address
        for e in i.iter('email'):               # email n’est pas forcément unique pour un employé
            address=e.get('address')
            # Exportation dans la table Address
            address=Address(employee_id=current_employee,email_address=address)
            address.save()