from rest_framework import serializers
from ..models import Organization, Category, Borrower, Approver, Item, EquipmentStock, BorrowRequest, BorrowQueue
from django.utils import timezone
from .user_serializers import UserSerializer
from rest_framework.exceptions import ValidationError


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BorrowerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer เพื่อรวมข้อมูล User

    class Meta:
        model = Borrower
        fields = ('id', 'profile_image', 'description', 'user')


class ApproverListSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer เพื่อรวมข้อมูล User

    class Meta:
        model = Approver
        fields = ('id', 'profile_image', 'description', 'user')

class ItemSerializerforSeacrh(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    class Meta:
        model = Item
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


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
