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


class BorrowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', write_only=True)
    email = serializers.EmailField(source='user.email', write_only=True)
    password = serializers.CharField(write_only=True)
    profile_image = serializers.URLField(required=False, allow_null=True)
    fname = serializers.CharField(
        source='user.first_name', write_only=True)  # เพิ่มฟิลด์ fname
    lname = serializers.CharField(
        source='user.last_name', write_only=True)   # เพิ่มฟิลด์ lname

    class Meta:
        model = Borrower
        fields = ['id', 'profile_image', 'description',
                  'username', 'email', 'password', 'fname', 'lname']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        username = user_data.get('username')
        password = user_data.pop('password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                {"username": "This username is already taken."})

        # Create user and set password
        user = User(**user_data)
        user.password = make_password(password)  # Hash the password
        user.save()

        # Create borrower
        borrower = Borrower.objects.create(user=user, **validated_data)

        # Add user to Borrower group
        borrower_group, created = Group.objects.get_or_create(name='Borrower')
        user.groups.add(borrower_group)

        return borrower


class ApproverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approver
        fields = '__all__'


class ApproverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', write_only=True)
    email = serializers.EmailField(source='user.email', write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Approver
        fields = ['id', 'profile_image', 'description',
                  'username', 'email', 'password']

    def create(self, validated_data):
        # Get user data
        user_data = validated_data.pop('user')
        password = user_data.pop('password')

        # Create user and set password
        user = User(**user_data)
        user.password = make_password(password)  # Hash the password
        user.save()

        # Create approver
        approver = Approver.objects.create(user=user, **validated_data)

        # Add user to Approver group
        approver_group, created = Group.objects.get_or_create(name='Approver')
        user.groups.add(approver_group)

        return approver


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


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
