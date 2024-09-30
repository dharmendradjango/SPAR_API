from rest_framework import serializers
from app.models.user_model import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = [
            'id','first_name', 'last_name', 'email', 'mobile', 'username', 'password', 'password2',
            'file', 'role_id', 'uid', 'status', 'reg_date'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        hashed_password = make_password(validated_data['password'])
        user = User(
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
            mobile=validated_data.get('mobile', ''),
            username=validated_data['username'],
            password=hashed_password,
            file=validated_data.get('file', ''),
            role_id=validated_data.get('role_id', None),
            uid=validated_data.get('uid', None),
            status=validated_data.get('status', True),  # Assuming the user is active by default
            reg_date=validated_data.get('reg_date', timezone.now())  # Assuming current time
        )

        user.save()
        return user
    
    