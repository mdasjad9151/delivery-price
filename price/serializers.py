from rest_framework import serializers

class PricingRequestSerializer(serializers.Serializer):
    zone = serializers.CharField(max_length=100)
    organization_id = serializers.CharField(max_length=10)
    total_distance = serializers.FloatField()
    item_type = serializers.CharField(max_length=100)

class PricingResponseSerializer(serializers.Serializer):
    total_price = serializers.FloatField()