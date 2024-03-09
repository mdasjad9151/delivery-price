import io
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from  django.views.decorators.csrf import csrf_exempt
from .serializers import PricingRequestSerializer,PricingResponseSerializer, OrganizationSerializer, ItemSerializer, PricingSerializer
from .models import Organization,Item,Pricing
from decimal import Decimal



# Create your views here.
def index(request):
    return JsonResponse({'guide': '''BASE_URL = https://delivery-poje.onrender.com/ End-points:

api/price
api/create/organization/
api/create/item/
api/create/pricing/
The api/price endpoint is used to obtain the dynamic delivery price calculated based on the provided data, while the other three are utilized to add new tuples to the given tables.

Test API: For testing purposes, you must install the Python Requests library or another testing platform such as Postman by adding the body element of the code.

Response testing:

import requests import json

URL = "https://delivery-poje.onrender.com/api/price/"

def delivery_response(): #body

data={
    'zone':'central',
    'organization_id': '005',
    'total_distance': 12.0,
    'item_type': 'perishable'
}

json_data = json.dumps(data)
print(json_data)
r =  requests.post(url=URL, data=json_data)
if r.status_code == 200:

    print(r.json())
else:
    print(error)
delivery_response()

To add more tuples in Organization: BASE_URL = 'https://delivery-poje.onrender.com/api/'

def create_organization(): url = BASE_URL + 'create/organization/' print(url) data = { 'id': '005', 'name': 'Organization 1' } response = requests.post(url, json=data) if response.status_code == 200: print('org added') else: print("error")

create_organization()

To add more tuples in Item: def create_item(): url = BASE_URL + 'create/item/' print(url) data = { 'id': '001', 'item_type': 'perishable', 'description': 'Perishable Item 1' } response = requests.post(url, json=data)

print('item added')
create_item() To add more tuples in Pricing:

def create_pricing(): url = BASE_URL + 'create/pricing/' data = { 'organization_id': '005', 'item_id': '001', 'zone': 'central', 'base_distance_in_km': 5.0, 'km_price': 1.5, 'fix_price': 10.0 } response = requests.post(url, json=data)

print('price added')
create_pricing()
    '''})

def home(request):
    return redirect('index')
@csrf_exempt
def calculate_delivery_price(request):
    total_price = None
    if request.method == 'POST':
        json_data =  request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream=stream)
        serializer = PricingRequestSerializer(data=python_data)
        if serializer.is_valid():
            zone = serializer.validated_data['zone']
            organization_id = serializer.validated_data['organization_id']
            total_distance = serializer.validated_data['total_distance']
            item_type = serializer.validated_data['item_type']
            if item_type.lower() == 'non-perishable':
                return JsonResponse({'total_price': 0.0})

            else:
                try:
                    pricing_info = Pricing.objects.filter(
                        organization_id=organization_id,
                        zone=zone
                    ).first()
                except:
                    return JsonResponse({'error': 'No Data Found'})

                if pricing_info:
                    # Extract pricing details
                    base_distance = float(pricing_info.base_distance_in_km)
                    per_km_price = float(pricing_info.km_price)
                    fix_price = float(pricing_info.fix_price)

                        # Calculate additional distance beyond the base distance
                    additional_distance = max(float(total_distance) - base_distance, 0)

                        # Calculate total price
                    total_price = fix_price + additional_distance * per_km_price
                        
                        # Round total price to two decimal places
                    total_price = round(total_price, 2)
                    if total_price is not None:
                        response_data = {'total_price': total_price}
                        response_serializer = PricingResponseSerializer(response_data)
                        return JsonResponse(response_serializer.data)
                    else:
                        return JsonResponse({'error': 'Pricing information not found for the given parameters'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    # return HttpResponse("HII")




@csrf_exempt
def create_organization(request):
    if request.method == 'POST':
        json_data =  request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream=stream)
        serializer = OrganizationSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
def create_item(request):
    if request.method == 'POST':
        json_data =  request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream=stream)
        serializer = ItemSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})


@csrf_exempt
def create_pricing(request):
    if request.method == 'POST':
        json_data =  request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream=stream)
        serializer = PricingSerializer(data=python_data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})


