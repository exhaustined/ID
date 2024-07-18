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
from .models import SharedDetails
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
                    save_data=Details.objects.create(aadhaar_id=data['id_number'],name=data['name'], phone=data['phone'],
                                                     age=data['age'],sex=data['sex'], caste=data['caste'],
                                                     address=data['address'],marital_status=data['marital_status'])
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

def shared_details(request):
    details = SharedDetails.objects.all()
    for k in details:
        print(k.name_shared)
        print(234234)
    context = {
        'shared_details': details,
    }
    return render(request, 'shared_details.html', context)

@csrf_exempt
def request_data_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company_name = data.get('company_name')
            requested_details = data.get('requested_details')

            # Validate required fields
            if not company_name or not requested_details:
                return JsonResponse({'error': 'Invalid request.'}, status=400)

            # Create request object
            request_obj = Request.objects.create(
                company_name=company_name,
                requested_details=requested_details
            )

            return JsonResponse({'success': 'Request submitted successfully.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)