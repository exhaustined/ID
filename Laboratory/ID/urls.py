from django.urls import path
from . views import *
urlpatterns = [
    path('',index,name='index'),
    path('scan_qr/',index, name='scan_qr'),
    path('shared_details/', shared_details, name='shared_data'),
]