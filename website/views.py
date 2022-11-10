from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import requests
from  requests.auth import HTTPBasicAuth
import base64
import datetime
from decouple import config


def home(request):
    return render(request, 'home.html', {})


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }
        message = '''
        New message: {}

        From: {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '', ['snextech001@gmail.com'])

        # Send An Email
        # send_mail(
        #     name, # subject
        #     subject,
        #     message, # message
        #     email, # from email
        #     ['snextech001@gmail.com'], # To email
        #     fail_silently=False,
        # )

        return render(request, 'contact.html', {'name': name})
    else:
        return render(request, 'contact.html', {})



def about(request):
    return render(request, 'about.html', {})


def services(request):
    return render(request, 'services.html', {})

def loan(request):
    global cash, number, amount
    if request.method == 'POST':
        amount = request.POST['amount']
        number = request.POST['number']
        reason = request.POST['reason']

        data = {
            'amount': amount,
            'number': number,
            'reason': reason,
        }

        cash = 0.1 * int(amount)
        lipa_mpesa()
        # print(cash)
        return render(request, 'loan.html', {'name': number})

    else:
        return render(request, 'loan.html', {})


def apply(request):
    
    if request.method == 'POST':
        fname = request.POST['fname'] 
        lname = request.POST['lname']
        number = request.POST['idno']

        data = {
            'fname': fname,
            'lname': lname,
            'number': number,
        }
        # print(data)
        return render(request, 'loan.html', {'fname': fname})

    else:
        return render(request, 'apply.html', {})


def ac_token():
    #Mpesa details
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    data = (requests.get(mpesa_auth_url, auth = HTTPBasicAuth(consumer_key, consumer_secret))).json()

    return data['access_token']



def lipa_mpesa():
    #Mpesa details
        consumer_key = config('consumer_key')
        consumer_secret = config('consumer_secret')
        base_url = 'https://billionbabyloans.herokuapp.com/api/payments/lnm/'

        mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        access_token = ac_token()
        saa = datetime.datetime.now()
        timestamp_format = saa.strftime("%Y%m%d%H%M%S")
        # phone = PHONE.get()
        businessshortcode = "6077238"

        passkey = config('passkey') #pass_key
        

        pd_decode = businessshortcode+passkey+timestamp_format

        ret = base64.b64encode(pd_decode.encode())

        pd = ret.decode('utf-8')

        headers = {"Authorization": "Bearer %s" % access_token}
        # print(access_token)
        request_body = {

            "BusinessShortCode":"6077238",    
            "Password": pd,    
            "Timestamp":timestamp_format,    
            "TransactionType": "CustomerPayBillOnline",    
            "Amount":cash,    
            "PartyA":number,    
            "PartyB":"6077238",    
            "PhoneNumber":number,    
            "CallBackURL":base_url,    
            "AccountReference":"BETTERLIFE-LOANS",    
            "TransactionDesc":"Fee Payment"
            }
        # print(number)

        lipa_response = requests.post(mpesa_endpoint, json = request_body, headers=headers)
        return lipa_response.json()

