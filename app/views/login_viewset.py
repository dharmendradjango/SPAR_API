from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from app.serilaizers.login_serializer import UserSerializer
from rest_framework.authtoken.models import Token
from app.models.user_model import CustomToken, User
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# from django.utils import timezone

# # Replace 'your_token_key_here' with the actual token key
# token = CustomToken.objects.filter(key='1bcfcebc-cb10-430e-81d2-da8c8a031f14').first()

# if token:
#     print(f"Token: {token.key}, Expires At: {token.expires_at}, Is Expired: {token.is_expired()}")
# else:
#     print("Token not found.")


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_409_CONFLICT)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                CustomToken.objects.filter(user=user).delete()  # Remove old tokens if any
                token, created = CustomToken.objects.get_or_create(user=user)  # Create a new token
                return Response({
                    "user": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "mobile": user.mobile,
                        "username": user.username,
                        "role_id": user.role_id,
                        "uid": user.uid,
                        "status": user.status,
                        "reg_date": user.reg_date
                    },
                    "token": token.token_key
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            

# class UserLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             # token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 "user": {
#                     "id":user.id,
#                     "username": user.username,
#                     "email": user.email, 
#                     "first_name":user.first_name,
#                     "last_name":user.last_name,
#                     "role":user.role
#                 },
#                 "message":"Login successful",
#                 "token": token.key
#             })
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class CustomAuthToken(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Authenticate user and get a token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
            },
            required=['username', 'password'],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication token'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                }
            ),
        }
    )

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(password, user.password):  # Check if the provided password matches the stored hash
            CustomToken.objects.filter(user=user).delete()  # Delete any existing tokens
            token, created = CustomToken.objects.get_or_create(user=user)  # Create a new token
            return Response({
                'token': str(token.token_key),
                'user_id': user.pk,
                'email': user.email,
                'username': user.username
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token_key = request.data.get("token")
        try:
            token_obj = CustomToken.objects.get(token_key=token_key)
            if token_obj.is_expired():
                return Response({"detail": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
            token_obj.delete()  # Invalidate the used token
            new_token = CustomToken.objects.create(user=token_obj.user)
            return Response({
                "token": str(new_token.token_key),
            })
        except CustomToken.DoesNotExist:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            token_key = request.auth.token_key
            CustomToken.objects.filter(token_key=token_key).delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except CustomToken.DoesNotExist:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)