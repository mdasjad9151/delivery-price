from django.test import TestCase
from .models import Organization, Item, Pricing
# Create your tests here.

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create test data for organizations
        self.organization1 = Organization.objects.create(id='001', name='Org1')
        self.organization2 = Organization.objects.create(id='002', name='Org2')

        # Create test data for items
        self.item1 = Item.objects.create(id='001', type='perishable', description='Item 1')
        self.item2 = Item.objects.create(id='002', type='non-perishable', description='Item 2')

        # Create test data for pricing
        self.pricing1 = Pricing.objects.create(
            organization=self.organization1,
            item=self.item1,
            zone='central',
            base_distance_in_km=5,
            km_price=1.5,
            base_price=10
        )
        self.pricing2 = Pricing.objects.create(
            organization=self.organization2,
            item=self.item2,
            zone='central',
            base_distance_in_km=5,
            km_price=1.0,
            base_price=8
        )

    # def test_organization_creation(self):
    #     self.assertEqual(self.organization1.name, 'Org1')
    #     self.assertEqual(self.organization2.name, 'Org2')

    # def test_item_creation(self):
    #     self.assertEqual(self.item1.description, 'Item 1')
    #     self.assertEqual(self.item2.type, 'non-perishable')

    # def test_pricing_creation(self):
    #     self.assertEqual(self.pricing1.km_price, 1.5)
    #     self.assertEqual(self.pricing2.base_price, 8)

    # def test_pricing_relationships(self):
    #     self.assertEqual(self.pricing1.organization, self.organization1)
    #     self.assertEqual(self.pricing2.item, self.item2)