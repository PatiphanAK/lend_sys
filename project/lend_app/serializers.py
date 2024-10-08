from rest_framework import serializers
from .models import Organization, Category, Borrower, Approver, Item, EquipmentStock, BorrowRequest, BorrowQueue
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class BorrowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    profile_image = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = Borrower
        fields = ('id', 'profile_image', 'description',
                  'username', 'password', 'email', 'first_name', 'last_name')

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
        user_serializer.is_valid(raise_exception=True)  # Raise an error if the user data is invalid
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


class ApproverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Approver
        fields = ('id', 'description', 'profile_image', 'username', 'email', 'first_name', 'last_name', 'password', 'organization')

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
        user_serializer.is_valid(raise_exception=True)  # Raise an error if the user data is invalid
        user = user_serializer.save()  # Create the user
        
        # Create the approver
        approver = Approver.objects.create(user=user, **validated_data)

        # Add user to Approver group
        approver_group, created = Group.objects.get_or_create(name='Approver')
        user.groups.add(approver_group)
        return approver

class ApproverListSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer เพื่อรวมข้อมูล User
    class Meta:
        model = Approver
        fields = ('id', 'profile_image', 'description', 'user')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class EquipmentStockDetailSerializer(serializers.ModelSerializer):
    item = ItemSerializer()  # รวม serializer ของ Item

    class Meta:
        model = EquipmentStock
        fields = ['item', 'organization', 'quantity', 'available']


class EquipmentStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentStock
        fields = '__all__'


class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = '__all__'

    def validate(self, attrs):
        borrow_date = attrs.get('borrow_date')
        return_date = attrs.get('return_date')

        # Validate date range
        if return_date and borrow_date:
            if return_date < borrow_date:
                raise serializers.ValidationError(
                    "Return date must be after the borrow date.",
                    code='invalid_date_range'
                )

        # Validate borrow date is not in the past
        if borrow_date < timezone.now():
            raise serializers.ValidationError(
                "Borrow date must not be in the past.",
                code='invalid_borrow_date'
            )

        # Validate return date is not in the past
        if return_date < timezone.now().date():
            raise serializers.ValidationError(
                "Return date must not be in the past.",
                code='invalid_return_date'
            )

        return attrs


class BorrowQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowQueue
        fields = '__all__'
