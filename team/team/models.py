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