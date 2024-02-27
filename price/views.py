import io
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from  django.views.decorators.csrf import csrf_exempt
from .serializers import PricingRequestSerializer,PricingResponseSerializer, OrganizationSerializer, ItemSerializer, PricingSerializer
from .models import Organization,Item,Pricing
from decimal import Decimal



# Create your views here.

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
        print(python_data)
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
        print(json_data)
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream=stream)
        serializer = PricingSerializer(data=python_data)
        print(serializer.is_valid())

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors)
    else:
        print("HI")
        return JsonResponse({'error': 'Only POST requests are allowed'})
        # return HttpResponse('hi')

def data(request):
    org =  Organization.objects.all()
    item =  Item.objects.all()
    price =  Pricing.objects.all()
    return HttpResponse(org, item, price)

