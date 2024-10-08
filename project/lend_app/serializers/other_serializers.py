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


class ItemSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())

    class Meta:
        model = Item
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class EquipmentStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentStock
        fields = '__all__'

class AssignItemToStockSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    organization_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        try:
            data['item'] = Item.objects.get(id=data['item_id'])
        except Item.DoesNotExist:
            raise serializers.ValidationError("Item does not exist")

        try:
            data['organization'] = Organization.objects.get(id=data['organization_id'])
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization does not exist")

        # ตรวจสอบว่า quantity ต้องเป็นค่าบวก
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")

        return data

    def create(self, validated_data):
        item = validated_data['item']
        organization = validated_data['organization']
        quantity = validated_data['quantity']

        # ใช้ get_or_create เพื่อไม่ให้เกิดปัญหา id ซ้ำกัน
        equipment_stock, created = EquipmentStock.objects.get_or_create(
            item=item,
            organization=organization,
            defaults={'quantity': quantity, 'available': quantity}
        )

        # ถ้ามีอยู่แล้ว (ไม่ได้สร้างใหม่) ก็ทำการอัปเดตจำนวน
        if not created:
            equipment_stock.quantity += quantity
            equipment_stock.available += quantity
            equipment_stock.save()

        return equipment_stock



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
