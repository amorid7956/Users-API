from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer

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


    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        user = User.objects.get(pk=self.kwargs.get('pk', None))
        serializer = self.get_serializer_class()(user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

