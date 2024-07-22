from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json
import requests

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import Request, SharedDetails
from .serializers import RequestSerializer, SharedDetailsSerializer

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
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Request submitted successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def requests_page(request):
    requests = Request.objects.all()
    return render(request, 'requests.html', {'requests': requests})

@api_view(['PATCH'])
def handle_request_action(request, pk):
    try:
        request_instance = Request.objects.get(pk=pk)
    except Request.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    action = request.data.get('action')
    if action == 'approve':
        shared_data = {detail: True for detail in request_instance.requested_details.split(',')}
        SharedDetails.objects.create(company_name=request_instance.company_name, shared_data=shared_data)
        request_instance.delete()
        return Response({'success': 'Request approved and details shared.'}, status=status.HTTP_200_OK)
    elif action == 'deny':
        request_instance.delete()
        return Response({'success': 'Request denied.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)