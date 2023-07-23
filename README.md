Bitespeed Backend Task: Identity Reconciliation

Usage:
The Backend service has been hosted on "https://identityreconciliation.pythonanywhere.com/identify/"

Steps:
1) Go to the URL mentioned above.
2) Open Postman => My Workspace => New 
3) Select the HTTP request as POST.
4) Enter the above mentioned URL (https://identityreconciliation.pythonanywhere.com/identify/)
5) Select Body => raw => Text = JSON
6) In the below textbox send the JSON eresponse in the format:
     {
        "email": "jas@gas.com",
        "phoneNumber": "1945"
      }
