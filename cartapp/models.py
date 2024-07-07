from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import modelformset_factory

# Create your models here.
class ProductModel(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=100,default='')
    prod_link = models.CharField(max_length=256,default='')
    prod_price = models.IntegerField(default=0)
    prod_img =models.CharField(max_length=100,default='')
    prod_description = models.TextField(blank=True,default='')
    
    class Meta:
        db_table = 'Product'
    def __str__(self):
        return self.prod_name

class OrderModel(models.Model):
    STATUS_CHOICES = (
        ('cart', 'In Cart'),
        ('ordered', 'Ordered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100,default='')
    phone = models.CharField(max_length=100,default='')
    grandtotal = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='cart')
    class Meta:
        db_table = 'Order'
    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.prod_name} in Order #{self.order.id}"

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['address', 'phone']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Phone',max_length=50,null=False,default='')
    class Meta:
        db_table = 'UserProfile'
    def __str__(self):
        return self.user.username

