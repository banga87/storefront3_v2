from decimal import Decimal
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from store.models import Product
import pytest


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product):
        # Arrange
        # Act
        response = create_product({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_returns_403(self, create_product, authenticate): # 403 Forbidden
        # Arrange
        authenticate()
        # Act
        response = create_product({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_if_data_is_invalid_returns_400(self, authenticate, create_product): # 400 Bad Request
        # Arrange
        authenticate(is_staff=True)
        # Act
        response = create_product({'title': ''})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None 

    
    def test_if_data_is_valid_returns_201(self, authenticate, create_product, create_collection):
        # Arrange
        authenticate(is_staff=True)
        collection = create_collection({'title': 'a'})
        # Act
        response = create_product({
            'title': 'a',
            'slug': 'a',
            'description': 'a',
            'unit_price': 10.00,
            'inventory': 10,
            'collection': collection.data['id'],
            'promotions': []

        })
                # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_return_200(self, api_client):
        # Arrange
        product = baker.make(Product)
        print(product.promotions.count())
        # Act
        response = api_client.get(f'/store/products/{product.id}/')
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': product.id,
            'title': product.title,
            'slug': product.slug,
            'description': product.description,
            'unit_price': Decimal(product.unit_price),
            'inventory': product.inventory,
            'collection': product.collection.id,
            'images': [],
            'price_with_tax': product.unit_price * Decimal(1.1)
        }