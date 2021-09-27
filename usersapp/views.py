from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Description of the POST method from swagger_auto_schema via method_decorator",
    responses={201: ReadOnlyUserSerializer}))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="description of the PUT method from swagger_auto_schema via method_decorator",
    responses={200: ReadOnlyUserSerializer}))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="description the PATCH from swagger_auto_schema via method_decorator",
    responses={200: ReadOnlyUserSerializer}))
class UsersAPIViewSet(ModelViewSet):
    queryset = User.objects.all()


    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ReadOnlyUserSerializer
        return WriteOnlyUserSerializer


    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = self.get_serializer_class()(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    """ I`ve documented these two methods of the ModelViewSet class,
        because I wanted to demonstrate the implementation of the decorator:
        (@method_decorator from django.utils.decorators) on the ModelViewSet class.
        Also thera are implemented create() and update() methods by me in serializers.py module.
    
    
    @swagger_auto_schema(responses={200: ReadOnlyUserSerializer})
    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        user = User.objects.get(pk=self.kwargs.get('pk', None))
        serializer = self.get_serializer_class()(user, data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: ReadOnlyUserSerializer})
    def partial_update(self, request, *args, **kwargs):
        serializer_data = request.data
        user = User.objects.get(pk=self.kwargs.get('pk', None))
        serializer = self.get_serializer_class()(user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
