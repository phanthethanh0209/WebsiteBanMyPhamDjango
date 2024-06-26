from django.db import models

# Create your models here.

# class Category_Group(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    #categroup = models.ForeignKey(Category_Group, on_delete=models.SET_NULL, null=True)

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # description = models.TextField()
    # image = models.TextField()

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2) #decimal_places xác định số chữ số thập phân sau dấu chấm thập phân.
    description = models.TextField()
    image = models.TextField()
    # SoLuongTon = models.IntegerField(default=0)
    # HinhAnh = models.ImageField(upload_to='images/')

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default='user')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'product')

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)
    recipient_address = models.CharField(max_length=255)
    method_payment = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, default="Chưa xác nhận")

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        # Định nghĩa hai trường foreign key làm khóa chính
        unique_together = ('order', 'product')
