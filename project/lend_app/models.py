from django.db import models
from django.contrib.auth.models import User

# หน่วยงานที่มีอุปกรณ์ให้ยืม


class Organization(models.Model):
    ORG_TYPES = (
        ('GOV', 'Government'),
        ('EDU', 'Educational'),
        ('CORP', 'Corporate'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=4, choices=ORG_TYPES)

    def __str__(self):
        return self.name

# หมวดหมู่ของ


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


def borwer_image_path(instance, filename):
    rename_fielname = f'{instance.user.username}'
    return f'borrower_images/{rename_fielname}'

def approver_image_path(instance, filename):
    rename_fielname = f'{instance.user.username}'
    return f'approver_images/{rename_fielname}'

def item_image_path(instance, filename):
    rename_fielname = f'{instance.name}'
    return f'item_images/{rename_fielname}'


# ผู้ยืม


class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=borwer_image_path, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# ผู้อนุมัติการยืม


class Approver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=approver_image_path, null=True, blank=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.username

# อุปกรณ์ที่สามารถยืมได้


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(
        Category, related_name='items')
    item_image = models.ImageField(upload_to=item_image_path, null=True, blank=True)

    def __str__(self):
        return self.name


# สต็อกอุปกรณ์ในหน่วยงาน
class EquipmentStock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    available = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.item.name} at {self.organization.name}'


# คำขอยืมอุปกรณ์
class BorrowRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RETURNED', 'Returned'),
    )

    borrower = models.ForeignKey(
        Borrower, on_delete=models.SET_NULL, null=True)
    equipment_stock = models.ForeignKey(
        EquipmentStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    approver = models.ForeignKey(Approver, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='PENDING')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)



# ต่อคิวยืมของ


class BorrowQueue(models.Model):
    equipment_stock = models.ForeignKey(
        EquipmentStock, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    queue_position = models.PositiveIntegerField()
    request_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['equipment_stock', 'queue_position'], name='unique_queue_position'
            )
        ]
