from typing import List
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Contact

def identify_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        phone_number = data.get('phone_number')

        try:
            primary_contact = Contact.objects.get(email=email) or Contact.objects.get(phone_number=phone_number)
        except:
            Contact.objects.create(email=email, phone_number=phone_number, link_precedence='primary')

        if primary_contact.link_precedence == 'primary':
            primary_contact.link_precedence = 'secondary'
            primary_contact.save()
        
        secondary_contact = Contact.objects.create(email=email, phone_number=phone_number, link_precedence='primary', linkedId = primary_contact.id)
        secondary_contact.save()

        response_data = {
            "contact": {
                "primaryContactId": primary_contact.id,
                "emails": List[email],
                "phone_number": List[phone_number],
                "secondaryContactIds": secondary_contact.id
            }
        }
        return JsonResponse(response_data, status=200)
    
    return JsonResponse({"message":"Invalid information"}, status=405)


