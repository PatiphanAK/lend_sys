from rest_framework import serializers
from ..models import Organization, Category, Borrower, Approver, Item, EquipmentStock, BorrowQueue, BorrowRequest
from django.utils import timezone
from .user_serializers import UserSerializer

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
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class EquipmentStockSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField(read_only=True)
    organization = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EquipmentStock
        fields = ['id', 'item', 'organization', 'quantity', 'available', 'is_available']


class CreateEquipmentStockSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), source='item')

    class Meta:
        model = EquipmentStock
        fields = ['item_id', 'organization', 'quantity', 'available', 'is_available']

    def validate(self, data):
        if 'available' not in data:
            data['available'] = data['quantity']
        return data


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
    approver = serializers.PrimaryKeyRelatedField(queryset=Approver.objects.all(), required=False)
    borrower = serializers.PrimaryKeyRelatedField(queryset=Borrower.objects.all(), required=False)

    class Meta:
        model = BorrowRequest
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Request context is required")

        approver = attrs.get('approver')
        borrower = attrs.get('borrower')

        borrow_date = attrs.get('borrow_date')
        expected_return_date = attrs.get('expected_return_date')
        return_date = attrs.get('return_date')
        status = attrs.get('status')

        # Validate date range
        if return_date and borrow_date:
            if return_date < borrow_date:
                raise serializers.ValidationError(
                    "Return date must be after the borrow date.",
                    code='invalid_date_range'
                )

        # Validate borrow date is not in the past
        if borrow_date and borrow_date < timezone.now().date():
            raise serializers.ValidationError(
                "Borrow date must not be in the past.",
                code='invalid_borrow_date'
            )
        
        #Validate expected return date is not in the past
        if expected_return_date and expected_return_date < timezone.now().date():
            raise serializers.ValidationError(
                "Expected return date must not be in the past.",
                code='invalid_expected_return_date'
            )
        # Validate expected return date is after the borrow date
        if expected_return_date and borrow_date:
            if expected_return_date < borrow_date:
                raise serializers.ValidationError(
                    "Expected return date must be after the borrow date.",
                    code='invalid_date_range'
                )
            
        # Validate return date is not in the past
        if return_date and return_date < timezone.now().date():
            raise serializers.ValidationError(
                "Return date must not be in the past.",
                code='invalid_return_date'
            )

        # Validate approver for approved/rejected/returned status
        if status in ['APPROVED', 'REJECTED', 'RETURNED'] and not approver:
            raise serializers.ValidationError(
                f"Approver is required when the request is {status.lower()}",
                code='approver_required'
            )

        # Validate if returned, the approver must be the same as the original approver
        if self.instance and status == 'RETURNED':
            original_approver = self.instance.approver
            if original_approver and approver != original_approver:
                raise serializers.ValidationError(
                    "The person returning the item must be the same as the approver.",
                    code='approver_mismatch'
                )

        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('status') == 'RETURNED':
            instance.equipment_stock.available += instance.quantity
            instance.equipment_stock.save()
            # ตรวจสอบและประมวลผลคิว
            BorrowQueue.objects.filter(equipment_stock=instance.equipment_stock).order_by('queue_position').first().process_queue()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Request context is required")

        borrower = Borrower.objects.get(user=request.user)
        validated_data['borrower'] = borrower
        
        return super().create(validated_data)
    

class OrganizationStockSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = EquipmentStock
        fields = ['item', 'quantity', 'available']

class BorrowItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class ReturnItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class BorrowQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowQueue
        fields = '__all__'

    def create(self, validated_data):
        equipment_stock = validated_data['equipment_stock']
        quantity = validated_data['quantity']
        borrower = validated_data['borrower']

        # ตรวจสอบว่าของในคลังเพียงพอหรือไม่
        if equipment_stock.available >= quantity:
            # สร้าง BorrowRequest อัตโนมัติ
            borrow_request = BorrowRequest.objects.create(
                equipment_stock=equipment_stock,
                borrower=borrower,
                quantity=quantity,
                status='PENDING'
            )
            # อัปเดต available ใน EquipmentStock
            equipment_stock.available -= quantity
            equipment_stock.save()

            # ลบ BorrowQueue ที่เกี่ยวข้อง
            related_queues = BorrowQueue.objects.filter(equipment_stock=equipment_stock, borrower=borrower)
            if related_queues.exists():
                related_queues.delete()
            return borrow_request
        else:
            # สร้าง BorrowQueue
            queue_position = BorrowQueue.objects.filter(equipment_stock=equipment_stock).count() + 1
            borrow_queue = BorrowQueue.objects.create(
                equipment_stock=equipment_stock,
                borrower=borrower,
                queue_position=queue_position,
                quantity=quantity
            )
            return borrow_queue
