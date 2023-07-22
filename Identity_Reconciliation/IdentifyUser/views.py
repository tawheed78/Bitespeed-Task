from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Contact
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def identify_user(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        phoneNumber = data.get('phoneNumber')

        try:
            primary_contact_email = list(Contact.objects.filter(email=email).all())

        except Contact.DoesNotExist:
            primary_contact_email = []
        try:
            primary_contact_phone = list(Contact.objects.filter(phoneNumber=phoneNumber).all())
        except Contact.DoesNotExist:
            primary_contact_phone = []

        print(primary_contact_email)
        print(primary_contact_phone)

        if len(primary_contact_email)==0 and len(primary_contact_phone)==0:
            primary_contact = Contact.objects.create(email=email, phoneNumber=phoneNumber, linkPrecedence='primary')
            
            print("created", primary_contact)
            response_data = {
            "contact": {
                "primaryContactId": primary_contact.id,
                "emails": [primary_contact.email],
                "phoneNumber": [primary_contact.phoneNumber],
                "secondaryContactIds": [],
                }
            }
            return JsonResponse(response_data, status=200)

        else:
            primary_contact_combined = list(set(primary_contact_phone+primary_contact_email))

            print(primary_contact_combined)

            primary_contact_combined.sort(key=lambda x: x.createdAt)

            primary_contact_old = primary_contact_combined[0]
            
            primary_contact_old.linkPrecedence = 'primary'
            primary_contact_old.save()

            print("primary linkprec updated")

            emailList = [primary_contact_old.email]
            phoneList = [primary_contact_old.phoneNumber]
            secondary_contacts=[]

            for i in range(1, len(primary_contact_combined)):
                secondary_contact = primary_contact_combined[i]
                secondary_contact.linkPrecedence = 'secondary'
                secondary_contact.linkedId = primary_contact_old
                secondary_contact.save()
                print("sec linkprec updated")
                if len(primary_contact_email)==0:
                    emailList.append(secondary_contact.email)
                if len(primary_contact_phone)==0:
                    phoneList.append(secondary_contact.phoneNumber)
                secondary_contacts.append(secondary_contact.id)
            print("71",secondary_contacts)
            new_contact = Contact.objects.create(email=email, phoneNumber=phoneNumber, linkPrecedence='secondary', linkedId=primary_contact_old)
            print("after")
            if len(primary_contact_email)==0:
                emailList.append(new_contact.email)
            if len(primary_contact_phone)==0:
                phoneList.append(new_contact.phoneNumber)
            secondary_contacts.append(new_contact.id)
            print("79",secondary_contacts)

            response_data = {
            "contact": {
                "primaryContactId": primary_contact_old.id,
                "emails": emailList,
                "phoneNumber": phoneList,
                "secondaryContactIds": secondary_contacts,
                }
            }
            return JsonResponse(response_data, status=200)
              

        # if phoneNumber and primary_contact.linkPrecedence=='primary':
        #     primary_contact.phoneNumber = phoneNumber
        #     primary_contact.save()


        # linkedContacts = []
        # emailList = []
        # phoneList = []
        # secondaryContacts = []

        # linkedContacts = Contact.objects.filter(linkedId = primary_contact.id)

        # emailList.append(primary_contact.email)
        # phoneList.append(primary_contact.phoneNumber)

        # for contact in linkedContacts:
        #     if contact.linkPrecedence == 'secondary':
        #         emailList.append(contact.email)
        #         phoneList.append(contact.phoneNumber)
        #         secondaryContacts.append(contact.id)


        # if primary_contact.linkPrecedence == 'primary':
        #     primary_contact.linkPrecedence = 'secondary'
        #     primary_contact.save()
        
        # secondary_contact = Contact.objects.create(email=email, phoneNumber=phoneNumber, linkPrecedence='secondary', linkedId = primary_contact)


        
    
    return JsonResponse({"message":"Invalid information"}, status=405)