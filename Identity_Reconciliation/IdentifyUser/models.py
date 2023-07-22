from django.db import models

class Contact(models.Model):
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    linkedId = models.ForeignKey('self',null=True, blank=True, on_delete=models.SET_NULL)
    link_precedence = models.CharField(max_length=10, default='primary')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(aut0_now = True)
    deleted_at = models.DateTimeField(null=True, blank=True)

def __str__(self):
    return self.email or self.phone_number
