from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password':{ 'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(
                validated_data['username'], 
                validated_data['email']
            )

            user.set_password(validated_data['password'])
            user.save()

            return user
