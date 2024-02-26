from .models import Pricing
from decimal import Decimal

class PricingService:
    @staticmethod
    def calculate_total_price(zone, organization_id, total_distance, item_type):
        # Get pricing information based on zone and organization_id.
        # try:
        #     pricing_info = Pricing.objects.filter(
        #         organization_id=organization_id,
        #         zone=zone
        #     ).first()
        # except:
        #     return None
        if item_type == 'perishable':
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

                # Return the total price
                return total_price
            else:
                return None
        else:
            return 0
        
        
