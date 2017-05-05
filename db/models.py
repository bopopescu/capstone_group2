from django.db import models

# Create your models here.
from django.db import models


class Bankaccount(models.Model):
    sellerID = models.IntegerField(primary_key=True)
    accountNo = models.CharField(max_length=10, primary_key=True)
    bankName = models.CharField(max_length=20,primary_key=True)

class Buyer(models.Model):
    userID = models.IntegerField(primary_key=True)

class Category(models.Model):
    catName = models.CharField(max_length=30)
    catID = models.AutoField(primary_key=True)

class Commentrating(models.Model):
    commentID = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=100)
    star=models.DecimalField(decimal_places=1,max_digits=6)
    sellerID =models.IntegerField(primary_key=True)
    buyerID = models.IntegerField()
    orderID = models.IntegerField()

class Hashtag(models.Model):
    productID = models.IntegerField(primary_key=True)
    hashtag = models.CharField(max_length=30,primary_key=True)

class Likes(models.Model):
    buyerID = models.IntegerField(primary_key=True)
    catID = models.IntegerField(primary_key=True)
    likeFirstHand=models.BooleanField()

class Moneytransfer(models.Model):
    amount = models.DecimalField(decimal_places=1,max_digits=6)
    transferID= models.AutoField(primary_key=True)
    orderID = models.IntegerField()
    sellerID= models.IntegerField()

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    confirmedStatus = models.BooleanField()
    amount = models.IntegerField()
    paymentTimeStamp = models.CharField(max_length=30)
    paymentSlip = models.BinaryField()
    buyerID = models.IntegerField()
    productID = models.IntegerField()
    orderTime = models.TimeField()
    bankid = models.IntegerField()

class Product(models.Model) :
    productID=models.AutoField(primary_key=True)
    price=models.DecimalField(decimal_places=1,max_digits=6)
    secondHandStatus=models.BooleanField()
    deliveryFee=models.DecimalField(decimal_places=1,max_digits=6)
    catID=models.IntegerField()
    subcatID=models.IntegerField()
    sellerID=models.IntegerField()
    isActive=models.BooleanField()
    productPic=models.BinaryField()
    des=models.CharField(max_length=50)
class Seller(models.Model) :
    emailAddress = models.CharField(max_length=30)
    userID=models.IntegerField(primary_key=True)
    avgstar=models.DecimalField(decimal_places=1,max_digits=6)


class Shipmentconfirmation(models.Model):
    status=models.BooleanField()
    buyerID=models.IntegerField()
    orderID=models.IntegerField(primary_key=True)

class Soldproduct(models.Model):
    sellerID = models.IntegerField()
    productID=models.IntegerField(primary_key=True)

class Subcategory(models.Model):
    subCatID=models.AutoField(primary_key=True)
    catID=models.IntegerField(primary_key=True)
    subCatName=models.CharField(max_length=20)

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    phoneNumber = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

class Wishlist(models.Model):
    buyerID = models.IntegerField(primary_key=True)
    productID = models.IntegerField(primary_key=True)


