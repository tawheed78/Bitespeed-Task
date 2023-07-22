from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Contact
from django.views.decorators.csrf import csrf_exempt

#To bypass the csrf protection
@csrf_exempt
def identify_user(request):

    #Getting data into the required variables
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        phoneNumber = data.get('phoneNumber')

        #Finding contact details containing either similar email or phone number in separate variables if not then setting them as None.
        try:
            primary_contact_email = list(Contact.objects.filter(email=email).all())
        except Contact.DoesNotExist:
            primary_contact_email = []


        try:
            primary_contact_phone = list(Contact.objects.filter(phoneNumber=phoneNumber).all())
        except Contact.DoesNotExist:
            primary_contact_phone = []

        #If both the variables are None that means data does not exist and a new data is created.
        if len(primary_contact_email)==0 and len(primary_contact_phone)==0:
            primary_contact = Contact.objects.create(email=email, phoneNumber=phoneNumber, linkPrecedence='primary')
            
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
            #Getting combined data with similar contacts and sorting them old to new to get the oldest one and set the linkPrecedence as Primary.
            primary_contact_combined = list(set(primary_contact_phone+primary_contact_email))
            primary_contact_combined.sort(key=lambda x: x.createdAt)

            primary_contact_old = primary_contact_combined[0]
            primary_contact_old.linkPrecedence = 'primary'
            primary_contact_old.save()

            #Appending the data with Primary Precedence to be the first one.
            emailList = [primary_contact_old.email]
            phoneList = [primary_contact_old.phoneNumber]
            secondary_contacts=[]

            #Looping through all the data except the primary one to set linkPrecedence as Secondary
            for i in range(1, len(primary_contact_combined)):
                secondary_contact = primary_contact_combined[i]
                secondary_contact.linkPrecedence = 'secondary'
                secondary_contact.linkedId = primary_contact_old
                secondary_contact.save()
                
                #If the primary contact email does not exist only then we append it to avoid email duplicates and same for phone number.
                if len(primary_contact_email)==0:
                    emailList.append(secondary_contact.email)
                if len(primary_contact_phone)==0:
                    phoneList.append(secondary_contact.phoneNumber)
                secondary_contacts.append(secondary_contact.id)
            
            #Creating the secondary contact
            new_contact = Contact.objects.create(email=email, phoneNumber=phoneNumber, linkPrecedence='secondary', linkedId=primary_contact_old)
            
            if len(primary_contact_email)==0:
                emailList.append(new_contact.email)
            if len(primary_contact_phone)==0:
                phoneList.append(new_contact.phoneNumber)
            secondary_contacts.append(new_contact.id)

            response_data = {
            "contact": {
                "primaryContactId": primary_contact_old.id,
                "emails": emailList,
                "phoneNumber": phoneList,
                "secondaryContactIds": secondary_contacts,
                }
            }
            return JsonResponse(response_data, status=200)       
    
    return JsonResponse({"message":"Invalid information"}, status=405)