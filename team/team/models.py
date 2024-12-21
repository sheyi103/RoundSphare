from django.db import models
import json
from django.utils import timezone

class Products(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    productName = models.CharField(max_length=200, db_column='product_name')
    imageName = models.CharField(max_length=500, db_column='image_name')
    imageId = models.IntegerField(db_column='image_id')
    price = models.FloatField(default=0.0)
    createdAt = models.DateTimeField(db_column='created_at', auto_now_add=True)
    
    class Meta:
        db_table = 'products'
        
    def __str__(self):
        Products = {
            'id': self.id,
            'productName': self.productName,
            'imageName': self.imageName,
            'imageId': self.imageId,
            'price': self.price,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
        }
        return json.dumps(Products)  
    
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    orderId = models.CharField(null=False, db_column='order_id', max_length=6)
    customerId = models.IntegerField(db_column='customer_id')
    productId =models.IntegerField(db_column='product_id')
    paymentStatus = models.CharField(db_column='payment_status', max_length=200)
    shippingAddress = models.CharField(db_column='shipping_address', max_length=200)
    country = models.CharField(max_length=50)
    county = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    postCode = models.CharField(db_column='postcode', max_length=50)
    dateCreate = models.DateTimeField(db_column='created_at', auto_now_add=True)
    
    class Meta:
        db_table = 'order'
        
    def __str__(self):
        Order = {
            'id': self.id,
            'orderId': self.orderId,
            'customerId': self.customerId,
            'productId': self.productId,
            'paymentStatus': self.paymentStatus,
            'shippingAddress': self.shippingAddress,
            'country': self.country,
            'county': self.county,
            'phone': self.phone,
            'postCode': self.postCode,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
        }
        return json.dumps(Order)     