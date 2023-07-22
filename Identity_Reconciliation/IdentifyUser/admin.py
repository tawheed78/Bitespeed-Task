from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'phoneNumber', 'email', 'linkedId', 'linkPrecedence', 'createdAt', 'updatedAt', 'deletedAt' )

admin.site.register(Contact, ContactAdmin)