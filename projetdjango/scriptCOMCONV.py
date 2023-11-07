#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetbdr.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
django.setup()
from appli.models import Communication,Conversation

#chemin = directory.encode(encoding="mbcs")
#path = chemin.decode("utf8")

def infos_comconv(directory):
    """
    Remplir les tables Communication et Conversation en parcourant les mails de la base
    """

    import re
    from name import name, namerep      # Fonctions définies dans name.py
    from date import daterep, date1     # Fonctions définies dans date.py

    # Regex

    date_mail=re.compile(r"(?<=Date:\s).*?(?= \(...)")
    sent_mail=re.compile(r"(?<=Sent:\s)(\s*)(.*? (AM|PM)(?=To:))")
    subject=re.compile(r"(?<=Subject:\s).*?(?=Mime-Version|Cc:|\n{2,})")
    msg_id=re.compile(r"(?<=Message-ID: <).*?(?=.JavaMail)")

    # adresses mails et noms
    sender=re.compile(r"(?<= From:\s).*?(?= To:|Sent:|Subject:)")
    name_sender=re.compile(r"(?<= X-From:\s).*?(?= \<|X-To:)")
    sender_rep=re.compile(r"(?<= From:\s).*?(?= To:|CC:|cc:|Cc:|Subject:|Sent:)")

    receiver_to=re.compile(r"(?<= To:\s).*?(?= cc:|Subject:)")
    name_receiver_to=re.compile(r"(?<= X-To:\s).*?(?= X-cc:)")
    receiver_to_rep=re.compile(r"(?<=To:\s).*?(?=Date:|cc:|Cc:|CC:|Subject:|Sent:)")

    receiver_cc=re.compile(r"(?<= Cc:\s).*?(?=Mime-Version:)")
    rcv_cc2=re.compile(r"(?<= cc:\s).*?(?=Subject:|----- Forwarded|Sent:)",re.IGNORECASE)
    name_receiver_cc=re.compile(r"(?<= X-cc:\s).*?(?= X-bcc:)")

    receiver_bcc=re.compile(r"(?<=Bcc:\s).*?(?=X-From:)")
    name_receiver_bcc=re.compile(r"(?<= X-bcc:\s).*?(?= X-Folder:)")

    # Initialisation des paramètres
    conversation=[]
    communication=[]
    person=[]           # Liste de toutes les personnes de la base
    c=0                 # Compteur de conversations
    a=1                 # Compteur de communication
    for root, dirs, files in os.walk(directory):        # Parcourir tous les mails
        for file in files:
            c+=1
            print(file)                                 # Chemin du fichier en cours de traitement
            if file.endswith(''):
                # print('---- Conversation',c,'----')
                fichier=os.path.join(root, file)

            with open(fichier,"r",encoding="utf-8") as file:
                # Traitement de la conversation
                liste=[]                                  
                for line in file:                         # Enlever les sauts de lignes et espaces inutiles pour toute la conversation
                    line = "".join(re.split(r"^\t+", line, re.M))
                    line = "".join(re.split(r"\n+$", line, re.M))
                    line = "".join(re.split(r"\s+$", line, re.M)) 
                    liste.append(line)                    # Mettre les lignes d'une conversation dans une liste
                mail=" ".join(str(l) for l in liste)      # Pour chaque ligne de la liste, on les concatène
                
                
                #Informations communes à toute la conversation
                sujet=subject.search(mail)
                msgid=msg_id.search(mail)
                
                mail2=re.compile(r"--------- Inline attachment follows ---------.*$") # Ne pas traiter ce contenu
                mail_2=re.search(mail2, mail)
                if mail_2:
                    mail=re.sub(mail2,'',mail)
                    
                textes=re.split('-----\s*Original Message\s*-----',mail)  # Liste contenant les mails d'une conversation
            
                # Récupérer les données pour chaque mail
                k=0 
                for mail in textes:
                    k+=1                                                  # Numéro du mail dans la conversation courante
                    communication=[]
                    receiver=[]
                    
                    # Commun à tous les mails
                    if sujet:
                        sj=sujet.group()
    
                    if msgid:
                        messageID=msgid.group()
                        
                    conversation.append((c,messageID,sj,k))
                    #print(conversation)

                    # Insertion Conversation dans la base
                    for l in conversation:            
                        current_conversation=Conversation(conversation_id=c, message_id=messageID, subject=sj, number_mails=k)
                        current_conversation.save()
                    
                    if k==1:    # Premier mail de la conversation
                        date=date_mail.search(mail)
                        sender1 = sender.search(mail)
                        receiver_cc1 = receiver_cc.search(mail)
                        receiver_to1 = receiver_to.search(mail)
                        receiver_bcc1 = receiver_bcc.search(mail)
                        
                        name_sender1 = name_sender.search(mail)
                        name_receiver_cc1 = name_receiver_cc.search(mail)
                        name_receiver_to1 = name_receiver_to.search(mail)
                        name_receiver_bcc1 = name_receiver_bcc.search(mail)
                        
                        if sender1:               
                            expediteur=sender1.group()
                            if expediteur[-1]==' ':                      
                                expediteur=expediteur[0:len(expediteur)-1]
                            if name_sender1:
                                name_expediteur=name(name_sender1.group())
                                name_expediteur=re.sub(r",","",name_sender1.group())
                                person.append((name_expediteur,expediteur))     # Liste de toutes les personnes de la base
                            
                        if receiver_to1:  
                            to=receiver_to1.group().strip()
                            to=to.split(', ')
                            to=[t.strip() for t in to]                 
                            to=[t.replace('"','') for t in to]  

                            for i in to:
                                receiver.append((i,'TO'))                       # Stockage de chaque receiver avec le type de receiver (TO)
                                
                            if name_receiver_to1:
                                name_to=name(name_receiver_to1.group()) 
                                name_to=[n.replace('"','') for n in name_to]
                                if len(to) == len(name_to):
                                    for i in range(len(to)):
                                        person.append((name_to[i],to[i]))
                                    
                                
                        if receiver_cc1:  
                            cc1=receiver_cc1.group().split(', ')
                            cc1 = [cc.strip() for cc in cc1]
                            for i in cc1:
                                receiver.append((i,'CC'))                       # Stockage de chaque receiver avec le type de receiver (CC)
                                
                            if name_receiver_cc1:
                                name_cc1=name(name_receiver_cc1.group())
                                if len(cc1) == len(name_cc1):                                        
                                    for i in range(len(cc1)):                   
                                        person.append((name_cc1[i],cc1[i]))    # Liste de toutes les personnes de la base
                                
                              
                        if receiver_bcc1: 
                            bcc=receiver_bcc1.group().split(', ')
                            bcc = [b.strip() for b in bcc] 
                            for i in bcc:
                                receiver.append((i,'BCC'))                      # Stockage de chaque receiver avec son type
                            
                            if name_receiver_bcc1:
                                name_bcc=name(name_receiver_bcc1.group())
                                if len(bcc) == len(name_bcc):                                       
                                    for i in range(len(bcc)):                   
                                        person.append((name_bcc[i],bcc[i]))     # Liste de toutes les personnes de la base
                            
                        person=list(set(person)) # Unicité des tuples (commande set())
                            
                        if date: 
                            datemail=date.group()
                            datemail=date1(datemail)
                            
                        # Insertion Communication (premier mail)      
                        for i in receiver:
                            communication.append((a,c,expediteur,i[0],i[1],datemail))
                            current_communication = Communication(communication_id=a, conversation_id=current_conversation, sender=expediteur, receiver=i[0], type_receiver=i[1], type_exchange= 'NA', date_mail=datemail) 
                            current_communication.save()
                            a+=1
                     
                    else:   # Mails réponses
                        sent=sent_mail.search(mail)
                        receiver_ccrep=rcv_cc2.search(mail)
                        receiver_torep=receiver_to_rep.search(mail)
                        senderrep=sender_rep.search(mail)
                        
                        if senderrep:
                            expediteur=namerep(senderrep.group())
                            if expediteur[-1]==' ':                           
                                expediteur=expediteur[0:len(expediteur)-1]                   
                                expediteur.replace('"','')                      
                            if type(expediteur)==list and len(expediteur)==1:
                                expediteur=expediteur[0]

                        if receiver_torep: 
                            name_to_rep=namerep(receiver_torep.group())
                            if type(name_to_rep)==list and len(name_to_rep)==1:
                                name_to_rep=name_to_rep[0]
                                if name_to_rep[0]!='"' and name_to_rep[0]!='':
                                    receiver.append((name_to_rep,'TO'))

                            if type(name_to_rep)==list and len(name_to_rep)>1:
                                for i in name_to_rep:
                                    if i[0]!='"' and i[0]!='':
                                        receiver.append((i,'TO')) 
                            else:
                                receiver.append((name_to_rep,'TO'))
                            
                        if receiver_ccrep:          
                            name_cc_rep=namerep(receiver_ccrep.group())
                            if type(name_cc_rep)==list and len(name_cc_rep)>1:
                                if name_cc_rep[0]!='':
                                    for i in name_cc_rep:                   
                                        receiver.append((i,'CC')) 
                            else:
                                receiver.append((name_cc_rep,'CC'))
                            
                        if sent: #date
                            if sent.group() != '' and sent.group() != '\s':
                                date_sent=sent.group(2)
                                datemail=daterep(date_sent)

                            else :
                                datemail=datemail                           # Si on ne trouve pas la date on reprend la précédente
                                                   
                        # Insertion dans Communication (mails réponses)
                        for i in receiver:
                            communication.append((a,c,expediteur,i[0],i[1],datemail))
                            current_communication = Communication(communication_id=a, conversation_id=current_conversation, sender=expediteur, receiver=i[0], type_receiver=i[1], type_exchange= 'NA', date_mail=datemail) 
                            current_communication.save()
                            a+=1

    return person