from django.shortcuts import render, HttpResponse
import qrtools
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json
import requests
# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "POST":
        qr_image = request.FILES.get('qrcodeimage')

        # Convert the uploaded image to a numpy array
        nparr = np.fromstring(qr_image.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Decode the QR code
        decoded_objects = decode(img)
        # details = Details.objects.create(id=data[0],name=data[1],age=data[2],sex=data[3],caste=data[4],address=data[5],marital_status=data[6])
        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')

            # Verify data with server
            try:
                response = requests.get(f"https://issuer.ngrok.io/api/v1/enrollee-from-id/{qr_data}")
                if response.status_code == 200:
                    data = response.json()[0]
                    print(data)
                    # save_data=Details.objects.create(aadhaar_id=data['id_number'],name=data['name'], date)
                    return JsonResponse({
                        "status": "verified",
                        "data": data
                    })

                else:
                    return JsonResponse({"status": "not_verified", "message": "Data not found or invalid"})
            except requests.RequestException:
                return JsonResponse({"status": "error", "message": "Failed to connect to the server"})
        else:
            return JsonResponse({"status": "error", "message": "Unable to decode QR code"})
    return render(request, 'index.html')

def data_requests(request):
    pass