from django.contrib.auth import login
from django.contrib.auth.models import User


from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from authentication.serializers import LoginUserSerializer, UserSerializer, RegisterSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            return Response({
                "user": UserSerializer(user,context=self.get_serializer_context()).data,
                "token":  token
            })
        return Response(serializer.data, status=status.HTTP_401_BAD_REQUEST)



class LoginView(KnoxLoginView):
    serializer_class = LoginUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None) 

    def get_context_data(self, *args, **kwargs):
        return {'request': self.request}
    




