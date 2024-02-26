from rest_framework import serializers
from .models import Organization, Item, Pricing

class PricingRequestSerializer(serializers.Serializer):
    zone = serializers.CharField(max_length=100)
    organization_id = serializers.CharField(max_length=10)
    total_distance = serializers.FloatField()
    item_type = serializers.CharField(max_length=100)

class PricingResponseSerializer(serializers.Serializer):
    total_price = serializers.FloatField()




class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'