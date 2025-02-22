from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime

# Create your views here.
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000
CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.

@login_required
def send_request(request):
    description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
    email = request.user.email
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, CallbackURL=CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

@login_required
def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            user = request.user
            user.special_user = datetime.now() + timedelta(days=30)
            user.save()
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
