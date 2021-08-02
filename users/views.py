from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer
from .models import User

from utility.helpers import gettoken


class Register(APIView):

    def post(self, request):
        response = dict()
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response['error'] = False
        response['message'] = 'Signup Successful!'
        response['data'] = serializer.data

        return Response(response)


class LoginView(APIView):

    def post(self, request):
        response = dict()
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if not user.is_active:
            response["error"] = True
            response["message"] = 'This account is not active.'
            return Response(response)

        if user is None:
            raise AuthenticationFailed('We do not recognize this account.')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        token = gettoken(email, password)
        response['error'] = False
        response['message'] = 'Login Successful!'
        response['token'] = token["access"]

        return Response(response)
