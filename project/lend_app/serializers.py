from rest_framework import serializers
from .models import Organization, Category, Borrower, Approver, Item, EquipmentStock, BorrowRequest, BorrowQueue
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        borrower = Borrower.objects.create(user=user, **validated_data)
        return borrower


class ApproverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approver
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        approver = Approver.objects.create(user=user, **validated_data)
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
        if borrow_date < timezone.now().date():
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
