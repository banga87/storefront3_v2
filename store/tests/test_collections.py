from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from store.models import Collection
import pytest


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Arrange
        # Act
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate): # 403 Forbidden
        # Arrange
        authenticate()
        # Act
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection): # 400 Bad Request
        # Arrange
        authenticate(is_staff=True)
        # Act
        response = create_collection({'title': ''})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None 

    
    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):
        # Arrange
        authenticate(is_staff=True)
        # Act
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_return_200(self, api_client):
        # Arrange
        collection = baker.make(Collection)
        # Act
        response = api_client.get(f'/store/collections/{collection.id}/')
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }


    def test_id_collection_does_not_exist_404(self, api_client):
        # Arrange
        # Act
        response = api_client.get('/store/collections/999/')
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND