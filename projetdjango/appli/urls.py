from django.urls import path
from appli import views

urlpatterns = [
     path('', views.index, name='index'),
     path('employees', views.employees, name='Employés'),
     path('employees/name', views.employees_name, name='Employés Nom'),
     path('employees/email', views.employees_email, name='Employés Email'),
     path('employees/echanges', views.employees_echanges, name='Employés Email'),
     path('employees/liste', views.employees_liste, name='Liste'),
     path('couples', views.couples, name="Couples d'employés"),
     path('days', views.days, name='Jours'),
     path('mails', views.mails, name='Mails'),
]