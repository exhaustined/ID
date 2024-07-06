from django.shortcuts import render
import qrtools
# Create your views here.
def index(request):
    if request.method == "POST":
        qrcode = request.FILES.get('qrcodeimage')
        qrscanner = qrtools.QR()
        qrscanner.decode(qrcode)
        data = qrscanner.data.split()
        details = Details.objects.create(id=data[0],name=data[1],age=data[2],sex=data[3],caste=data[4],address=data[5],marital_status=data[6])
    return render(request, 'index.html')

def requests(request):