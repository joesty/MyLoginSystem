from multiprocessing import context
from django.contrib.auth.models import User
from rest_framework import viewsets, generics,response
from api.serializers import BooksSerializer, LoginSerializer, StudentSerializer, UserSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate, get_user_model
from api.models import Books, Student

User = get_user_model()

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BooksSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class RegisterAPI(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            #serializer.data['username'],
            serializer.data['email'],
            serializer.data['password']
        )
        user.set_password(serializer.data['password'])
        user.save()
        return response.Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.create(user=user).key
        })

class LoginAPI(generics.GenericAPIView):

    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = authenticate(username=serializer.initial_data['username'], password=serializer.initial_data['password'])
        if user == None:
            return response.Response({
                "user": "error"
            })
        return response.Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get_or_create(user=user)[0].key
        })

class LogoutAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return response.Response('Logout')