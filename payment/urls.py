from django.urls import path
from .views import send_request, verify

app_name = 'payment'

urlpatterns = [
    path('request/', send_request, name='request'),
    path('verify/', verify , name='verify'),
    
]