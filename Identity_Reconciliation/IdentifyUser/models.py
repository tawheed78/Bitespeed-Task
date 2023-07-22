from django.db import models

class Contact(models.Model):
    phoneNumber = models.CharField(max_length=10, default='', unique=False)
    email = models.CharField(max_length=100, unique=False)
    linkedId = models.ForeignKey('self',null=True, blank=True, on_delete=models.SET_NULL)
    linkPrecedence = models.CharField(max_length=10, default='primary')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now = True)
    deletedAt = models.DateTimeField(null=True, blank=True)

def __str__(self):
    return self.email or self.phoneNumber
