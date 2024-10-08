from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from lend_app.models import Borrower
from .user_serializers import UserSerializer

class BorrowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    profile_image = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = Borrower
        fields = ('id', 'profile_image', 'description',
                  'username', 'password', 'email', 'first_name', 'last_name')

    def validate_email(self, value):
        if Borrower.objects.filter(user__email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        if Borrower.objects.filter(user__username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        # Use UserSerializer to create a user
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
        }

        user_serializer = UserSerializer(data=user_data)
        # Raise an error if the user data is invalid
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()  # Create the user

        # Create the borrower
        borrower = Borrower.objects.create(user=user, **validated_data)

        # Add user to Borrower group
        borrower_group, created = Group.objects.get_or_create(name='Borrower')
        user.groups.add(borrower_group)

        return borrower


class BorrowerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer เพื่อรวมข้อมูล User

    class Meta:
        model = Borrower
        fields = ('id', 'profile_image', 'description', 'user')