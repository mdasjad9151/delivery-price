import io
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from  django.views.decorators.csrf import csrf_exempt
from .pricing import PricingService
from .serializers import PricingRequestSerializer,PricingResponseSerializer, OrganizationSerializer, ItemSerializer, PricingSerializer



# Create your views here.

# @api_view(['POST'])
@csrf_exempt
def calculate_delivery_price(request):
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
            

            total_price = PricingService.calculate_total_price(zone, organization_id, total_distance, item_type)
            if total_price is not None:
                response_data = {'total_price': total_price}
                response_serializer = PricingResponseSerializer(response_data)
                return JsonResponse(response_serializer.data)
            else:
                return JsonResponse({'error': 'Pricing information not found for the given parameters'}, status=400)
        else:
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    # return HttpResponse("HII")



@api_view(['POST'])
def create_organization(request):
    serializer = OrganizationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_pricing(request):
    serializer = PricingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)