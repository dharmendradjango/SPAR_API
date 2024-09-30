from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app.models.user_model import CustomToken
from rest_framework.permissions import BasePermission
import uuid

class CustomTokenAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'token':
                raise AuthenticationFailed('Invalid token header. No credentials provided.')

            token_key = parts[1]

            # Validate token format here if necessary (e.g., length or type check)
            token = CustomToken.objects.get(token_key=token_key)

        except CustomToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if token.is_expired():
            raise AuthenticationFailed('Token has expired.')

        return (token.user, token)
    

class IsUser(BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user and request.user.is_authenticated
