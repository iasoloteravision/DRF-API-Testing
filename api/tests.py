from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer


class ItemAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item_data = {'name': 'Test Item'}
        self.item = Item.objects.create(name='Existing Item')

    def test_get_items(self):
        response = self.client.get('/api/items/')
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
