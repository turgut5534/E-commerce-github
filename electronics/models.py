from django.db import models
from django.db.models import base
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name= models.CharField(max_length=50)
    image= models.ImageField(upload_to="categories", null=True, blank=True)
    created_at= models.DateTimeField(auto_now=True)
    modified_at= models.DateTimeField(auto_now=True)
    deleted_at= models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Marka(models.Model):
    name=models.CharField(max_length=50)
    image= models.ImageField(upload_to="brands", null=True, blank=True)
    amount= models.IntegerField(null=True, blank=True)
    category= models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Discount(models.Model):
    name= models.CharField(max_length=20)
    description = models.TextField()
    discount_percent= models.IntegerField()
    is_active= models.BooleanField()
    created_at= models.DateTimeField(auto_now=True)
    modified_at= models.DateTimeField()
    deleted_at= models.DateTimeField(blank=True , null=True)

    def __str__(self):
        return self.name

class Spec(models.Model):
    name= models.CharField(max_length=50)
    category= models.ManyToManyField(Category, null=True)

    def __str__(self):
        return self.name

class Specs(models.Model):
    spec = models.ForeignKey(Spec, on_delete=models.CASCADE)
    value= models.CharField(max_length=50)

    def __str__(self):
        return self.spec.name+" "+self.value

class Product(models.Model):
    image = models.ImageField(upload_to="laptops")
    imagetwo = models.ImageField(upload_to="laptops", null=True, blank=True)
    imagethree = models.ImageField(upload_to="laptops", null=True, blank=True)
    imagefour = models.ImageField(upload_to="laptops", null=True, blank=True)
    marka= models.ForeignKey(Marka, on_delete=models.CASCADE, null=True)
    model = models.CharField(max_length=50)
    slug= models.SlugField(unique=True, db_index=True)
    price = models.FloatField()
    discount_price= models.FloatField(null=True, blank=True)
    discount_applied = models.BooleanField(null=True)
    weight = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
    warranty= models.IntegerField()
    stock= models.IntegerField()
    is_new=models.BooleanField()
    is_featured= models.BooleanField()
    created_at= models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_at= models.DateTimeField(auto_now=True, blank=True, null=True)
    specs= models.ManyToManyField(Specs, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug=slugify(self.model)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.model


class Payment(models.Model):
    holder= models.CharField(max_length=50)
    number= models.CharField(max_length=50)
    expiry= models.CharField(max_length=6, null=True)
    cvv = models.IntegerField()
    kind= models.CharField(max_length=20, null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.holder

class Address(models.Model):
    kind = models.CharField(max_length=20, null=True, blank=True)
    city= models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    full_address = models.TextField(null=True)

    def __str__(self):
        return self.city

class UserInfo(models.Model):
     image = models.ImageField(upload_to="users", blank=True, null=True)
     sex= models.CharField( max_length=10,null=True)
     b_date= models.DateField(null=True)
     user = models.OneToOneField(User ,on_delete=models.CASCADE)
     tel= models.BigIntegerField(null=True, blank=True)
     address = models.ManyToManyField(Address, blank=True)

     def __str__(self):
        return self.user.username

class Card(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product= models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity= models.IntegerField()
    price = models.IntegerField(null=True)
    created_at= models.DateTimeField(auto_now=True)
    modified_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class WishList(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    product= models.ManyToManyField(Product)
    created_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class OrderDetail(models.Model):
    order_code= models.CharField(max_length=15, null=True)
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True, auto_now=True)
    shipping_date= models.DateField(null=True, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    status= models.CharField(max_length=50, null=True)
    product = models.ManyToManyField(Product, null=True)
    total= models.FloatField()
    is_cancelled= models.BooleanField(null=True)
    is_returned= models.BooleanField(null=True)
    payment= models.ForeignKey(Payment, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user_name= models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField(max_length=300)
    rating= models.IntegerField(null=True)
    date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="commentsofproduct")

    def __str__(self):
        return self.product.model

class Contact(models.Model):
    name= models.CharField(max_length=50)
    email= models.EmailField()
    subject= models.CharField(max_length=50)
    message= models.TextField()

    def __str__(self):
        return self.name

class VirtualCard(models.Model):
    holder= models.CharField(max_length=50)
    number= models.CharField(max_length=50)
    expiry= models.CharField(max_length=6)
    cvc = models.CharField(max_length=50)
    kind= models.CharField(max_length=20, null=True)
    amount= models.IntegerField()

    def __str__(self):
        return self.holder

class UpdateEmail(models.Model):
    email= models.EmailField(unique=True)

    def __str__(self):
        return self.email