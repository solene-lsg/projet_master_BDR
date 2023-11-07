from django import forms
from appli.models import *


class Form(forms.ModelForm):
    """
    Formulaire des vues
    """
    date1= forms.DateTimeField(label='Date de début')
    date2= forms.DateTimeField(label='Date de fin')
    results=forms.IntegerField(label='Seuil du nombre de résultats')
    nombre_min = forms.IntegerField(label='Nombre minimum de mails échangés')
    nombre_max = forms.IntegerField(label='Nombre maximum de mails échangés') 
    type_echange =  forms.CharField(label='Préciser le type des échanges : Intern ou Extern ou NA')
    email = forms.EmailField(label="Adresse email d'un employé")
    nom = forms.CharField(label="Nom d'un employé")