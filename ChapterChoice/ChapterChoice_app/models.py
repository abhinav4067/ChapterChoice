from django.db import models

# Create your models here.
from email.policy import default
from django.db import models




# Create your models here.
from django.contrib.auth.models import AbstractUser
#Abstract user instead of user in case of variable users


class Login(AbstractUser):
    userType=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50,null=True)
    def str(self):
        return self.username





# models of user

class user_reg(models.Model):
    user=models.OneToOneField(Login,on_delete=models.CASCADE,null=True)
    u_name=models.CharField(max_length=50,null=True)
    u_mobile=models.IntegerField(null=True)
    location=models.TextField(max_length=100,null=True)
    u_email=models.EmailField(null=True)
    dob=models.DateField( null=True)
    gender=models.TextField(null=True,max_length=100)
    u_password=models.CharField(max_length=50,null=True)
    u_cpassword=models.CharField(max_length=50,null=True)
    






class Book(models.Model):
    Book_name=models.TextField(max_length=100,null=True)
    Book_description=models.TextField(max_length=300,null=True)
    Book_price=models.IntegerField(null=True)
    Book_image1=models.ImageField(null=True) 
    Book_image2=models.ImageField(null=True) 
    Book_image3=models.ImageField(null=True) 
    Book_image4=models.ImageField(null=True) 
    priority=models.IntegerField(default=5)
    Book_category=models.CharField(max_length=100,null=True)
    Book_brand=models.CharField(max_length=100,null=True)
    Book_offer=models.IntegerField(default=1)
    Book_qty=models.IntegerField(default=1)


    def is_in_stock(self):
        return self.Book_qty > 0
    

    def __str__(self):
        return self.Book_name

class review(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    user_review=models.TextField(max_length=500,null=True)
    user_rating=models.IntegerField(default=0)
    review_date=models.DateField(null=True)
    Book_id=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    review_like=models.IntegerField(null=True)

class cart(models.Model):

    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    Book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
    cart_amount=models.IntegerField(null=True) 
    qty=models.IntegerField(null=True,default=1)




class orders(models.Model):

    CART_STAGE=0
    ORDER_CONFIRMED=1
    ORDER_PROCESSED='ORDER_PROCESSED'
    ORDER_DELIVERD='ORDER_DELIVERD'
    ORDER_REJECTED='ORDER_REJECTED'
    STATUS_CHOICE=((ORDER_PROCESSED,'ORDER_PROCESSED'),
                   (ORDER_DELIVERD,'ORDER_DELIVERD'),
                   (ORDER_REJECTED,'ORDER_REJECTED'))
    order_status=models.TextField(choices=STATUS_CHOICE,default=CART_STAGE )               
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    Book_id=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    order_amount=models.IntegerField(null=True)
    ordered_date=models.DateField(null=True)
    ordered_qty=models.IntegerField(null=True)
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=50,null=True)
    email=models.EmailField(null=True)
    mobile_num=models.CharField(max_length=12,null=True)
    street_address=models.CharField(max_length=300,null=True)
    pincode=models.CharField(max_length=10,null=True)
    city=models.CharField(max_length=50,null=True)
    country=models.CharField(max_length=50,null=True)
    



    

class payment(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    amount=models.IntegerField(null=True)
    payment_date=models.DateField(null=True)


# models of supplier.
    


class supplier_reg(models.Model):
    supplier_full_name=models.CharField(max_length=100)
    supplier_email=models.EmailField()
    supplier_mob_number=models.PositiveIntegerField(null=True)
    supplier_password=models.TextField()
    supplier_cpassword=models.TextField()


class wishlist(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    Book_id=models.ForeignKey(Book,on_delete=models.CASCADE,default=None)
    

class category(models.Model):

    category_name=models.CharField(max_length=50,null=True)




# models of admin.
    

       



