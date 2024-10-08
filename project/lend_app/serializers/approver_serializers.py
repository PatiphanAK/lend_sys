from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from lend_app.models import Approver, Organization
from .user_serializers import UserSerializer

class ApproverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all())

    class Meta:
        model = Approver
        fields = ('id', 'description', 'profile_image', 'username',
                  'email', 'first_name', 'last_name', 'password', 'organization')

    def validate_email(self, value):
        if Approver.objects.filter(user__email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        if Approver.objects.filter(user__username=value).exists():
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

        # Create the approver
        approver = Approver.objects.create(user=user, **validated_data)

        # Add user to Approver group
        approver_group, created = Group.objects.get_or_create(name='Approver')
        user.groups.add(approver_group)
        return approver