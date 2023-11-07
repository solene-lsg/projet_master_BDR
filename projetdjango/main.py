#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scriptXML import readXML
from scriptCOMCONV import infos_comconv
from scriptContentWord import scriptContentWord
from scriptAdressesNoms import AddressNames,update_s, update_r, update_type_exchange


if __name__=="__main__":
    directory = str(input('Quel est votre chemin pour la base de données de mail ? \n'))
    #directory = 'C:/Users/Solène/Documents/Angers/Master1/Semestre2/UE4-OutilsNumeriquesInformatique/BasesDonnéesRelationnelles/Projet/enron_mail_20150507.tar/maildir/davis-d/personal'
    xml = 'employes_enron.xml'
    readXML(xml)
    person=infos_comconv(directory)
    scriptContentWord(directory)
    AddressNames(person)
    update_s()
    update_r()
    update_type_exchange()