#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetbdr.settings')
import django
django.setup()

from datetime import datetime
from django.utils.timezone import datetime, timezone, timedelta

# Fonctions utiles pour convertir la date

def date1(datemail):
    """
    Convertir la date des premiers mails de chaque conversation
    """
    datetime_object=datetime.strptime(datemail, '%a, %d %b %Y %H:%M:%S %z')     # Reconnaissance du format de la date
    UTC = timezone(timedelta(hours =-7))                                        # Fuseau horaire fixé à -0700
    datemail = datetime_object.astimezone(UTC)                                  # Convertion au format UTC

    return datemail

def daterep(datemail):
    """
    Convertir la date des mails réponses de chaque conversation
    Traitement des différents formats de dates
    """
    try:
        datemail=datetime.strptime(datemail, '%A, %B %d, %Y %I:%M %p')      # Friday, December 08, 2000 2:19 PM
        return datemail

    except ValueError:
        try:
            datemail=datetime.strptime(datemail, '%A, %d. %B %Y %H:%M')      # Montag, 11. Dezember 2000 17:22
        except ValueError:
            try:
                datemail=datetime.strptime(datemail, '%a %m/%d/%Y %I:%M %p') # Fri 01/01/2000 2:19 PM
            except ValueError:
                try:
                    datemail=datemail[4:]                                    
                    if datemail[1]=='/':                                     # Fri 1/01/2000 2:19 PM
                        datemail = '0' + datemail                            # Ajouter le 0 devant le mois pour correspondre au format
                    datemail=datetime.strptime(datemail, '%m/%d/%Y %I:%M %p')
                    return datemail
                except ValueError:
                    datemail = '2001-01-01 01:01:01+01'                      # Date par défaut si aucune ne convient

        return datemail
    