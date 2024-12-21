from django.db import models
import json
from django.utils import timezone

# Custome registration form model
class Customer(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    firstName = models.CharField(max_length=100, db_column='first_name', null=True)
    lastName = models.CharField(max_length=100, db_column='last_name', null=True)
    otherName = models.CharField(max_length=100, db_column='other_name', null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    phone = models.CharField(unique=True, max_length=15, null=True)
    address = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=50, null=True)
    postcode = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=10, null=False, default='Inactive')
    confirmationCode = models.CharField(max_length=10, db_column='confirmation_code', null=True)
    createdAt = models.DateTimeField(db_column='created_at', auto_now_add=True)

    
    class Meta:
        db_table = 'customer'

    def __str__(self):
        Customer = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'otherName': self.otherName,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'address': self.address,
            'country': self.country,
            'postcode': self.postcode,
            'status': self.status,
            'confirmationCode': self.status,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
        }
        return json.dumps(Customer)