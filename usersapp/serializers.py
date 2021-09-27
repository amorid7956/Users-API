from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class ReadOnlyUserSerializer(ModelSerializer):
    class Meta:
        ref_name = 'ReadOnlyUserSerializer'
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active','last_login', 'is_superuser')


class WriteOnlyUserSerializer(ModelSerializer):

    class Meta:
        ref_name = 'WriteOnlyUserSerializer'
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'is_active')


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
