from django.db import models

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

# ผู้ยืม
class Borrower(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ผู้อนุมัติการยืม
class Approver(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    position = models.CharField()

    def __str__(self):
        return self.name


# อุปกรณ์ที่สามารถยืมได้
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name


# สต็อกอุปกรณ์ในหน่วยงาน
class EquipmentStock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    available = models.PositiveIntegerField(default=0)

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

    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    approver = models.ForeignKey(Approver, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.borrower.name} requests {self.quantity} {self.item.name}(s)'
    
#ต่อคิวยืมของ
class BorrowQueue(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    queue_position = models.PositiveIntegerField()
    request_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('item', 'queue_position')

    def __str__(self):
        return f'{self.borrower.name} is in queue for {self.item.name} at position {self.queue_position}'