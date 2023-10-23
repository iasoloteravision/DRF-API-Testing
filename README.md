# How to perform a DRF APITestCase #

Creating a Django project with a basic API and an APITestCase involves several steps. Below, I'll guide you through creating a simple Django project called "MyAPI" with an API endpoint to retrieve a list of items and provide a test case for it. This example assumes you already have Django installed. If not, you can install it using pip:

```python
pip install Django
```

Here are the basic steps to build the project:

1. Create a Django project:

```python
# Create the Django project
django-admin startproject MyAPI

# Change into the project directory
cd MyAPI

# Create a Django app for the API
python manage.py startapp api
```

2. Define the model and serializer

In your `api` app, define a model in the `models.py` file and a serializer in a `serializers.py` file.

`api/models.py`:

```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

`api/serializers.py`:

```python
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name']
```

3. Create a View and URL pattern:

In your `api` app, create a view in the `views.py` file and add a URL pattern in the `urls.py` file.

`api/views.py`:

```python
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

`api/urls.py`:

```python
from django.urls import path
from .views import ItemList

urlpatterns = [
    path('items/', ItemList.as_view(), name='item-list'),
]

```

4. Configure URLs in the project:

In your project's `urls.py`, include the URLs of your app.

`MyAPI/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

5. In project's settings insert 'api' module in installed apps.

`MyAPI/settings.py`:

```bash
...

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api', 
]
...
```

6. Run Migrations

Apply migrations to create the database tables for your model:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create super user to perform item creating actions in `http://localhost:8000/admin/`

7. Run `python manage.py runserver` and check if API is running.

8. Return to command line or your preferred IDE with `Control+c`and create  an API Test case:

Now, create an APITestCase in the `tests.py` file of your api app.

`api/tests.py`:

```python
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
```

9. Run Tests:

To run your tests, use the following command in your project's root directory:

```bash
python manage.py test api
```

This will run the test case you defined in the api/tests.py file. If all is set up correctly, you should see that the test passes, as it checks whether the API endpoint for retrieving items is working as expected.

Now you have a basic Django project with an API endpoint and an APITestCase for testing it. You can extend this project by adding more views, models, and tests as needed for your application.