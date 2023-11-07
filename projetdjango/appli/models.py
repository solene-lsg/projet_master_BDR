from django.db import models

# Create your models here.


# Création du modèle de données : tables..

class Employee(models.Model):
    
    name = models.CharField(max_length=100,unique=True,null=False)
    category = models.CharField(max_length=30,null=True)
    mail_box= models.CharField(max_length=20,unique=True, null=True)

    def __str__(self):
        return f"{self.id}, {self.name}, {self.category}, {self.mail_box}"


class Address(models.Model):
    
    employee_id = models.ForeignKey(Employee,on_delete=models.CASCADE,null=False)
    email_address = models.EmailField(max_length=150, unique=True,null=False)

    def __str__(self):
        return f"{self.id}, {self.employee_id}, {self.email_address}"


class Conversation(models.Model):
    conversation_id = models.BigIntegerField(primary_key=True)
    message_id = models.CharField(max_length=100, unique=True, null=False)
    subject = models.CharField(max_length=400, null=False)
    number_mails = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.conversation_id}, {self.message_id}, {self.subject}, {self.number_mails}"
    

class Communication(models.Model):
    communication_id = models.BigIntegerField(primary_key=True)
    conversation_id = models.ForeignKey(Conversation,on_delete=models.CASCADE,null=False)
    sender = models.EmailField(max_length=150, null=False)
    receiver = models.EmailField(max_length=500, null=False)
    type_receiver = models.CharField(max_length=10, null=False)
    type_exchange = models.CharField(max_length=10, null=False)
    date_mail = models.DateTimeField(null=False)
    
    def __str__(self):
        return f"{self.communication_id}, {self.conversation_id}, {self.sender}, {self.receiver}, {self.type_receiver}, {self.type_exchange}, {self.date_mail}"
    

class Address_Communication(models.Model):
    address_id = models.ForeignKey(Address,on_delete=models.CASCADE,null=False)
    communication_id = models.ForeignKey(Communication,on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return f"{self.address_id}, {self.communication_id}"


class Extern(models.Model):   
    name = models.CharField(max_length=100,unique=True,null=False)
    email_address = models.EmailField(max_length=200, unique=True,null=False)

    def __str__(self):
        return f"{self.id}, {self.name}, {self.email_address}"


class Communication_Extern(models.Model):
    extern_id = models.ForeignKey(Extern,on_delete=models.CASCADE,null=False)
    communication_id = models.ForeignKey(Communication,on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return f"{self.extern_id}, {self.communication_id}"


class Content(models.Model):
    conversation_id = models.ForeignKey(Conversation,on_delete=models.CASCADE,null=False)
    content = models.CharField(max_length=10000, null=True)
    number_words = models.IntegerField(null=True)
    filename = models.BooleanField(max_length=10, null=True)
    date_mail = models.DateTimeField(null=False)

    def __str__(self):
        return f"{self.id}, {self.conversation_id}, {self.content}, {self.number_words}, {self.filename}, {self.date_mail}"
  
    
class Word(models.Model):
    conversation_id = models.ForeignKey(Conversation,on_delete=models.CASCADE,null=False)
    keyword = models.CharField(max_length=500, null=False)
    occurence = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.id}, {self.conversation_id}, {self.keyword}, {self.occurence}"
    
