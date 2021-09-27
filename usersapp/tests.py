from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient,  APITestCase
from django.contrib.auth.models import User
from .views import UsersAPIViewSet


class TestUsersViewSet(TestCase):

    def setUp(self):
        self.creator = User.objects.create_superuser(username='django1', email='django1@email.ru', password='geekbrains')


    def test_get_project_list_guest(self):
        factory = APIRequestFactory()
        request = factory.get('/api/v1/users/')
        view = UsersAPIViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_project_list_authorized(self):
        factory = APIRequestFactory()
        request = factory.get('/api/v1/users/')
        force_authenticate(request, self.creator)
        view = UsersAPIViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAnotherProjectViewSet(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', email='admin@admin.com', password='admin123456')
        data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/api-token-auth/', data=data, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')


    def test_get_list(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Returns the only one instance(it is admin, which was created in setUp() method), therefore in default database
    # exists one user. Request other id`s returned "Not found"
    def test_get_detail_user(self):
        response = self.client.get('/api/v1/users/1/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
