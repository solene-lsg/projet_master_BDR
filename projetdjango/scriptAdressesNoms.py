#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetbdr.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django
django.setup()

from appli.models import Employee, Address, Communication, Extern
from scriptCOMCONV import infos_comconv


from django.core.exceptions import ObjectDoesNotExist


def AddressNames(person): 
    """
    Prend en argument une liste de tuples (nom, adresse) issue des premiers mails
    Parcourir la liste pour ajouter les personnes dans les tables Employee ou Extern
    """
    for p in person:

        add_emp=re.compile(r"@enron.com")
        add_enron=add_emp.search(p[1])

        arobase=re.compile(r"@")
        add=arobase.search(p[1])

        if add: 
            if add_enron:
                """
                Pour chaque adresse @enron.com, on la cherche dans la table Address, et si on la trouve on ne fait rien.
                Sinon, on cherche le nom dans Employee.
                Si on ne le trouve pas, on ajoute le nom de l'employé dans la table Employee,
                puis on ajoute l'adresse associée dans la table Address
                """
                try :                                          
                    Address.objects.get(email_address=p[1])
                except ObjectDoesNotExist:                     
                    try :                             
                        Employee.objects.get(name=p[0])
                    except ObjectDoesNotExist:
                        current_employee=Employee(name=p[0])
                        current_employee.save()

                    # Insertion de l'adresse email p[1] avec le nom p[0] de Employee
                    current_address=Address(employee_id=current_employee, email_address=p[1])
                    current_address.save()
         
            else:
                """
                On procède de la même façon avec la table Extern, pour les personnes exterieures (n'étant pas dans Enron)
                """
                try : 
                    Extern.objects.get(email_address=p[1])   
                except ObjectDoesNotExist:                 
                    try : 
                        Extern.objects.get(name=p[0])         
                    except ObjectDoesNotExist:        
                        current_extern=Extern(name=p[0], email_address=p[1])
                        current_extern.save()


def update_s(): 
    """
    Parcourir sender de Communication
    Remplacer les noms par une adresse mail si possible
    """
    from django.db import transaction  

    add=re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    with transaction.atomic():
        entries = Communication.objects.select_for_update().all()
        for entry in entries:
            address=add.search(entry.sender) 
            if not address:
                # On va chercher l'adresse email associée dans les tables
                try:
                    currentemployee_s=Employee.objects.get(name=entry.sender)
                    # Récupérer l'adresse mail associée 
                    addressmail_s=Address.objects.filter(employee_id=currentemployee_s.id).first() # On récupère la première adresse mail
                    entry.sender=addressmail_s.email_address               # On remplace par l'adresse email
                    entry.save()

                except ObjectDoesNotExist:  # Si pas dans Employee
                    try:
                        currentextern_s=Extern.objects.get(name=entry.sender)
                        # Récupérer l'adresse mail associée 
                        addressmail_s=Extern.objects.filter(id=currentextern_s.id).first()
                        entry.sender=addressmail_s.email_address
                        entry.save()

                    except ObjectDoesNotExist:
                        entry.save()      

def update_r(): 
    """
    Parcourir receiver de Communication
    Remplacer les noms par une adresse mail si possible
    """
    from django.db import transaction  

    add=re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

    with transaction.atomic():
        entries = Communication.objects.select_for_update().all()
        for entry in entries:
            address=add.search(entry.receiver)
            if not address:
                try:
                    currentemployee_r=Employee.objects.get(name=entry.receiver)
                    print(currentemployee_r.id)
                    #récupérer l'addresse mail associée 
                    addressmail_r=Address.objects.filter(employee_id=currentemployee_r.id).first()
                    entry.receiver=addressmail_r.email_address
                    entry.save()

                except ObjectDoesNotExist:
                    try:
                        currentextern_r=Extern.objects.get(name=entry.receiver)
                        print(currentextern_r.id)
                        #récupérer l'addresse mail associée 
                        addressmail_r=Extern.objects.filter(id=currentextern_r.id).first()
                        entry.receiver=addressmail_r.email_address
                        entry.save()

                    except ObjectDoesNotExist:
                        entry.save()    

def update_type_exchange():
    """
    Définir le type d'un email (Intern, Extern ou NA) en fonction du couple sender-receiver
    """
    from django.db import transaction  

    address=re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    add=re.compile(r"@enron.com")
    
    with transaction.atomic():
        entries = Communication.objects.select_for_update().all()
        for entry in entries:
            address_s=address.search(entry.sender)
            address_r=address.search(entry.receiver)

            if address_s and address_r: #si les deux sont des adresses mails
                address_s=add.search(entry.sender)
                address_r=add.search(entry.receiver)
                if not address_s or not address_r:
                    entry.type_exchange='Extern'
                    entry.save()

                else:
                    entry.type_exchange='Intern'
                    entry.save()
            else:
                entry.type_exchange='NA'
                entry.save()