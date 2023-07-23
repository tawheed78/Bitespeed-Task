from django.db import models

class Contact(models.Model):
    phoneNumber = models.CharField(max_length=15, unique=False, null=True)
    email = models.CharField(max_length=100, unique=False, null=True)
    # linkedId = models.ForeignKey('self',null=True, blank=True, on_delete=models.SET_NULL)
    linkedId = models.IntegerField(null=True, blank=True)
    linkPrecedence = models.CharField(max_length=10, default='primary')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now = True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email or str(self.phoneNumber)
