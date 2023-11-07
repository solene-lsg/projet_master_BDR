from appli.models import Employee, Communication, Content, Word, Extern
from django.utils.timezone import datetime
from django.shortcuts import render
import json

from collections import OrderedDict

# Create your views here.

def index(request):

    template = 'index.html'

    email_exchanges = Communication.objects.all().count()         # Nombre de mails dans la base
    num_extern = Extern.objects.all().count()                     # Nombre de personnes externes à Enron
    num_intern = Employee.objects.all().count()                   # Nombre d'employés

    context = {'email_exchanges':email_exchanges,
                'num_extern':num_extern,
                'num_intern':num_intern,
    }

    return render(request, template, context)

def employees_name(request):

    template='employees/name.html'
        
    nom = request.GET.get("Nom d'un employé")
    if not nom:
        nom = ''

    # Vue pour récupérer les adresses mails des employés
    attributs_name_email = Employee.objects.raw(f""" SELECT 
                                                    emp.name AS name,
                                                    emp.category AS category,
                                                    emp.id,
                                                    add.email_address AS email,
                                                    add.id AS add_id,
                                                    add.employee_id_id
                                                FROM 
                                                    appli_employee AS emp
                                                INNER JOIN
                                                    appli_address AS add
                                                ON emp.id = add.employee_id_id
                                                WHERE name='{nom}'
    """
    )
    # Vue pour récupérer le nom et la catégorie des employés
    attributs_name = Employee.objects.raw(f""" SELECT DISTINCT
                                                    n.id,
                                                    n.name AS nom,
                                                    n.category AS category
                                                FROM ( SELECT
                                                    emp.name AS name,
                                                    emp.category AS category,
                                                    emp.id,
                                                    add.email_address AS email,
                                                    add.id AS add_id,
                                                    add.employee_id_id
                                                FROM 
                                                    appli_employee AS emp
                                                INNER JOIN
                                                    appli_address AS add
                                                ON emp.id = add.employee_id_id
                                                WHERE name='{nom}') AS n;
    """
    )

    context = {
        'attributs_name_email':attributs_name_email,
        'attributs_name':attributs_name,
        'name':nom,
        }

    return render(request, template, context)

def employees_email(request):

    template='employees/email.html'

    email = request.GET.get("Adresse email d'un employé")
    if not email:
        email = ''

    # Vue pour récupérer le nom et la catégorie des employés
    attributs_email = Employee.objects.raw(f""" SELECT 
                                                    emp.name AS name,
                                                    emp.category AS category,
                                                    emp.id,
                                                    emp.mail_box AS mail_box,
                                                    add.email_address AS email,
                                                    add.id AS add_id,
                                                    add.employee_id_id
                                                FROM 
                                                    appli_address AS add
                                                INNER JOIN
                                                    appli_employee AS emp
                                                ON emp.id = add.employee_id_id
                                                WHERE email_address='{email}'
    """
    )

    context = {
        'attributs_email':attributs_email,
        'email':email,
        }

    return render(request, template, context)

def employees_echanges(request):

    template='employees/echanges.html'

    date1 = request.GET.get('Date de début')
    if not date1:
        date1=datetime(1980,1,1)
        date1=datetime.date(date1)

    date2 = request.GET.get('Date de fin')
    if not date2:
        date2=datetime(2010,1,1)
        date2=datetime.date(date2)

    nombre_min = request.GET.get('Nombre minimum de mails échangés')
    if not nombre_min:
        nombre_min = 1

    nombre_max = request.GET.get('Nombre maximum de mails échangés') 
    if not nombre_max:
        nombre_max = 1000

    type_echange =  request.GET.get('Préciser le type des échanges : Intern ou Extern ou NA')
    if not type_echange:
        type_echange = '' 

    results = request.GET.get('Seuil du nombre de résultats')  
    if not results:
        results = 100
  
    # Vue pour récupérer les employés ayant reçu/envoyé plus/moins qu'un certain nombre de mails (détail par conversation)
    echanges = Employee.objects.raw(f""" 
                                        SELECT
                                            appli_communication.sender AS sender,
                                            appli_communication.receiver AS receiver,
                                            appli_communication.date_mail AS date_mail,
                                            appli_communication.type_exchange AS type_exchange,
                                            appli_communication.conversation_id_id AS conversation_id,
                                            appli_communication.communication_id AS id,
                                            appli_conversation.number_mails AS number_mails,
                                            appli_conversation.conversation_id
                                        FROM 
                                            appli_conversation
                                        INNER JOIN
                                            appli_communication
                                        ON appli_conversation.conversation_id = conversation_id_id
                                        WHERE  '{nombre_min}' <= number_mails
                                            AND number_mails <= '{nombre_max}'
                                            AND type_exchange = '{type_echange}'
                                            AND date_mail > '{date1}'
                                            AND date_mail < '{date2}'
                                        ORDER BY number_mails DESC
                                        LIMIT {results};
    
    """
    )
    
    nombre_min=int(nombre_min)
    nombre_max=int(nombre_max)

    entries = Communication.objects.filter(date_mail__gte=date1,date_mail__lte=date2,type_exchange=type_echange).all()

    # Dictionnaire pour sender, format {sender : nombre de mails} 
    dict_s = {}
    for entry in entries:
        if entry.sender in dict_s:
            dict_s[entry.sender] += 1
        else:
            dict_s[entry.sender] = 1

    # Dictionnaire pour receiver, format {receiver : nombre de mails} 
    dict_r = {}
    for entry in entries:
        if entry.receiver in dict_r:
            dict_r[entry.receiver] += 1
        else:
            dict_r[entry.receiver] = 1

    # Concaténation des dictionnaires
    dict1 = {}
    for entry in entries:
        if entry.sender in dict1:
            dict1[entry.sender] += 1
        else:
            dict1[entry.sender] = 1
        if entry.receiver in dict1:
            dict1[entry.receiver] += 1
        else:
            dict1[entry.receiver] = 1
    
    # Ordonner les dictionnaires suivant le nombre de mails, par ordre décroissant
    dict1 = OrderedDict(sorted(dict1.items(), key=lambda x: x[1],reverse=True))
    dict_s = OrderedDict(sorted(dict_s.items(), key=lambda x: x[1],reverse=True))
    dict_r = OrderedDict(sorted(dict_r.items(), key=lambda x: x[1],reverse=True))

    # Filtrer les dictionnaires pour ne garder que ceux respectant le nombre de mails demandé
    final_dict_s = {k:v for k,v in dict_s.items() if dict_s[k]<=nombre_max and dict_s[k]>=nombre_min}
    final_dict_r = {k:v for k,v in dict_r.items() if dict_r[k]<=nombre_max and dict_r[k]>=nombre_min}
    final_dict = {k:v for k,v in dict1.items() if dict1[k]<=nombre_max and dict1[k]>=nombre_min}
    
    context = {
        'echanges':echanges,
        'nombre_min':nombre_min,
        'nombre_max':nombre_max,
        'type_echange':type_echange,
        'date1':date1,
        'date2':date2,
        'results':results,
        'final_dict_s':final_dict_s,
        'final_dict_r':final_dict_r,
        'final_dict':final_dict,
        }

    return render(request, template, context)
    
def employees_liste(request):

    template = 'employees/liste.html'

    date1 = request.GET.get('Date de début') 
    if not date1:
        date1=datetime(1980,1,1)
        date1=datetime.date(date1)

    date2 = request.GET.get('Date de fin')
    if not date2:
        date2=datetime(2010,1,1)
        date2=datetime.date(date2)

    results = request.GET.get('Seuil du nombre de résultats') 
    if not results:
        results = 20

    email = request.GET.get("Adresse d'un employé")
    if not email:
        email = ''

    entries = Communication.objects.filter(date_mail__gte=date1,date_mail__lte=date2,type_exchange='Intern').all()
    
    liste1=[]
    for entry in entries:
        if entry.sender == email:
            liste1.append(entry.receiver)
        if entry.receiver == email:
            liste1.append(entry.sender)

    liste=list(set(liste1))  # rendre unique les éléments de la liste

    # Vue : liste des employés ayant communiqué avec un employé
    liste_employees = Employee.objects.raw(f""" SELECT 
                                                        appli_communication.sender AS sender,
                                                        appli_communication.receiver AS receiver,
                                                        appli_communication.date_mail AS date_mail,
                                                        appli_communication.type_exchange AS type_exchange,
                                                        appli_communication.communication_id AS id
                                                    FROM 
                                                        appli_communication
                                                    WHERE 
                                                        type_exchange = 'Intern'
                                                        AND date_mail > '{date1}'
                                                        AND date_mail < '{date2}'
                                                        AND (sender='{email}' OR receiver='{email}')
                                                    ORDER BY date_mail ASC
                                                    LIMIT {results};    
    
    """
    )

    context = {
        'liste_employees':liste_employees,
        'liste':liste,
        'email':email,
        'date1':date1,
        'date2':date2,
        'results':results,
        }

    return render(request, template, context)

def employees(request):

    template = 'employees.html'

    num_intern = Employee.objects.all().count()

    context = {
        'num_intern':num_intern,
    }

    return render(request, template, context)


def couples(request):

    template = 'couples.html'

    date1 = request.GET.get('Date de début') 
    if not date1:
        date1=datetime(1980,1,1)
        date1=datetime.date(date1)

    date2 = request.GET.get('Date de fin')
    if not date2:
        date2=datetime(2010,1,1)
        date2=datetime.date(date2)

    nombre_min = request.GET.get('Nombre minimum de mails échangés') 
    if not nombre_min:
        nombre_min = 1

    type_echange =  request.GET.get('Préciser le type des échanges : Intern ou Extern ou NA')
    if not type_echange:
        type_echange = '' 

    results = request.GET.get('Seuil du nombre de résultats')
    if not results:
        results = 100
    
    # Vue : couples d’employés ayant communiqué dans un intervalle de temps choisi
    couples = Employee.objects.raw(f""" SELECT 
                                                appli_communication.sender AS sender,
                                                appli_communication.receiver AS receiver,
                                                appli_communication.date_mail AS date_mail,
                                                appli_communication.type_exchange AS type_exchange,
                                                appli_communication.communication_id AS id,
                                                appli_conversation.number_mails AS number_mails,
                                                appli_conversation.conversation_id
                                            FROM 
                                                appli_conversation
                                            INNER JOIN
                                                appli_communication
                                            ON appli_conversation.conversation_id = conversation_id_id
                                            WHERE 
                                                '{nombre_min}' <= number_mails 
                                                AND type_exchange = '{type_echange}'
                                                AND date_mail > '{date1}'
                                                AND date_mail < '{date2}'
                                            ORDER BY number_mails DESC
                                            LIMIT {results};    
    
    """
    )

    nombre_min=int(nombre_min)

    liste=[]
    entries = Communication.objects.filter(date_mail__gte=date1,date_mail__lte=date2,type_exchange='Intern').all()
    for entry in entries:
        liste.append((entry.sender,entry.receiver))
    
    # Rendre unique les tuples (couples)
    for duo1 in liste:
        for duo2 in liste:
            if duo1[0]==duo2[1] and duo1[1]==duo2[0]:
                duo2=duo1

    dict = {}
    for d in liste:
        if d in dict:
            dict[d] = dict[d] + 1
        else:
            dict[d] = 1

    dict = OrderedDict(sorted(dict.items(), key=lambda x: x[1],reverse=True))
    final_dict = {k:v for k,v in dict.items() if dict[k]>=nombre_min}

    context = { 
        'couples':couples,
        'final_dict':final_dict,
        'nombre_min':nombre_min,
        'type_echange':type_echange,
        'date1':date1,
        'date2':date2,
        'results':results,
        }

    return render(request, template, context)


def days(request):

    template = 'jours.html'

    date1 = request.GET.get('Date de début')
    if not date1:
        date1=datetime(1980,1,1)
        date1=datetime.date(date1)

    date2 = request.GET.get('Date de fin')
    if not date2:
        date2=datetime(2010,1,1)
        date2=datetime.date(date2)

    type_echange =  request.GET.get('Préciser le type des échanges : Intern ou Extern ou NA')
    if not type_echange:
        type_echange = '' 
    
    # Vue : jours dans une période donnée ayant connus les plus grand nombre d’échanges de mails
    days = Employee.objects.raw(f""" SELECT 
                                                TO_CHAR(date_mail :: DATE, 'yyyy-mm-dd') AS dates,
                                                appli_communication.date_mail AS date_mail,
                                                appli_communication.type_exchange AS type_exchange,
                                                appli_communication.communication_id AS id,
                                                appli_conversation.number_mails AS number_mails,
                                                appli_communication.conversation_id_id AS conversation_id,
                                                appli_conversation.conversation_id
                                            FROM
                                                appli_conversation
                                            INNER JOIN
                                                appli_communication
                                            ON appli_conversation.conversation_id = conversation_id_id
                                            WHERE
                                                type_exchange = '{type_echange}'
                                                AND date_mail > '{date1}'
                                                AND date_mail < '{date2}'
                                            ORDER BY number_mails DESC;    
    
    """)
    
    liste=[]
    entries = Communication.objects.filter(date_mail__gte=date1,date_mail__lte=date2,type_exchange=type_echange).all()
    for entry in entries:
        datetime_object=datetime.date(entry.date_mail)
        liste.append(str(datetime_object))

    dict = {}
    for date in liste:
        if date in dict:
            dict[date] = dict[date] + 1
        else:
            dict[date] = 1

    dict = OrderedDict(sorted(dict.items(), key=lambda x: x[1],reverse=True)) # Trier par ordre décroissant des nombre de mails
    dict1=OrderedDict(sorted(dict.items())) # Trier par date
    
    # Diagramme en bâtons (nombre de mails en fonction par date)
    categories=list()
    number_series=list()
    for key,value in dict1.items():
        categories.append('%s' % key)
        number_series.append(dict1[key])

    context = {
        'dict':dict,
        'dict1':dict1,
        'days':days,
        'type_echange':type_echange,
        'date1':date1,
        'date2':date2,
        'categories': json.dumps(categories),
        'number_series': json.dumps(number_series),
        }

    return render(request, template, context)


def mails(request):

    template = 'mails.html'

    mots = request.GET.get('Donner les mots clés, séparés par une virgule')
    if not mots:
        mots = ''

    # On récupère les mots fournis qui sont séparés par une virgule, pour les lister
    mots=mots.split(',')
    mots=[m.strip() for m in mots]

    entries = Word.objects.all()
    listemots=[]
    for i in entries:
        if i.keyword in mots: # Si on rencontre un des mots demandés dans la table Word
            listemots.append((i.occurence, i.conversation_id_id))

    liste_occ=[]
    occ=0
    # On souhaite obtenir le nombre total de mots cherchés qui sont dans chaque conversation
    for t in range(len(listemots)-1):
        if (listemots[t-1])[1] == (listemots[t])[1]:  # Si on est toujours dans la même conversation
            occ+=(listemots[t])[0]                    # On augmente le nombre d'occurence de la conversation avec celui du mot actuel
            liste_occ.append((occ,(listemots[t-1])[1]))
        else:
            occ=0
        
    maxi=0
    maxi_id=0
    # On cherche la conversation ayant le maximum d'occurences des mots cherchés
    for l in liste_occ:
        if l[0]>maxi:
            maxi=l[0]
            maxi_id=l[1]

    # Vue : contenu d’une conversation, déterminée par les mots clés
    mails = Content.objects.raw(f"""SELECT DISTINCT
                                        c.content_mail AS id
                                    FROM (
                                        SELECT
                                        appli_content.content AS content_mail,
                                        appli_content.conversation_id_id,
                                        appli_content.id,
                                        appli_word.keyword AS keywords,
                                        appli_word.occurence AS occurence,
                                        appli_word.conversation_id_id,
                                        appli_word.id
                                    FROM 
                                        appli_word
                                    INNER JOIN
                                        appli_content
                                    ON appli_content.conversation_id_id = appli_word.conversation_id_id
                                    WHERE 
                                        appli_content.conversation_id_id = '{maxi_id}'
                                    ) AS c;   
    
    """)

    filename = Content.objects.filter(filename=True).count()        # Nombre de mails ayant une pièce jointe
    nofilename = Content.objects.filter(filename=False).count()     # nombre de mails n'ayant pas une pièce jointe
    
    # On reprend les mots clés fournis
    liste_mots=''
    for m in mots:
        liste_mots+= m + ' ' 

    context = {
        'mails':mails,
        'mots':liste_mots,
        'filename':filename,
        'nofilename':nofilename,
        }

    return render(request, template, context)