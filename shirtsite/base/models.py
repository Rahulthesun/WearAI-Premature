from django.db import models
from django.contrib.auth.models import User

c=[
    ('small','S'),
    ("medium" , 'M'),
    ("Large",'L'),
    ("Extra Large" , 'XL',),
]
    

# Create your models here.

class imageui(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    request = models.TextField(null=False,blank=False)
    url = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.request

class Order(models.Model):
    image = models.ForeignKey(imageui,on_delete=models.CASCADE,unique=True)
    size = models.TextField(choices=c , null=False,blank=False)
    price = models.IntegerField(default=499,blank=False,null=False)
    #customer-details
    name=models.CharField(max_length=200)
    email=models.EmailField()
    phone=models.CharField(max_length=10,null=False,blank=False)
    address=models.TextField(null=False,blank=False)

    def __str__(self):
        return self.name
    







    


