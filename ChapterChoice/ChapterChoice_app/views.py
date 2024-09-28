
from pyexpat.errors import messages
from django.shortcuts import redirect, render

from django.db.models import Avg
# Create your views here.
from datetime import date
from django.shortcuts import render
from . models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError





# Create your views here.


def user_registration(request):
    if request.method == 'POST':
        name = request.POST["u_name"]
        email = request.POST["email"]
        password = request.POST["pass"]
        cpassword = request.POST["cpass"]
        phone_number = request.POST['phone_num']
        location = request.POST['location']
        gender = request.POST['gender']
        dob = request.POST['dob']
        
        # Check if a user with the same email already exists
        if Login.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('authentication-register')  # Redirect to avoid form resubmission

        # Additional logic to check password match
        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('authentication-register')  # Redirect to avoid form resubmission

        try:
            # Create login and user registration entries
            login = Login.objects.create_user(username=email, password=password, userType='customer', viewpassword=password)
            login.save()
            obj = user_reg.objects.create(user=login, u_name=name, u_mobile=phone_number, gender=gender, dob=dob, location=location, u_email=email, u_password=password, u_cpassword=cpassword)
            obj.save()
            messages.success(request, "Registration successful.")
            return redirect('authentication-login')  # Redirect to the login page
        
        except IntegrityError:
            # Handle any IntegrityErrors (e.g., duplicate email)
            messages.error(request, "An error occurred during registration.")
            return redirect('authentication-register')  # Redirect to avoid form resubmission

    return render(request, 'authentication-register.html')


def login1(request):
    
    if request.POST:
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(username=email,password=password)
        if user:
            login(request,user)
            request.session["user_ID"]=user.id
            return redirect('index') 
        else:
            wrong_message="wrong password"
            messages.error(request,wrong_message)   

    
    return render(request,'authentication-login.html') 


def SignOut(request):
    logout(request)
    return redirect('index')
def dashboard(request):
    return render(request,'account-dashboard.html')  

def add_Book(request):
    if request.POST:
        select=request.POST["select"]
        description=request.POST["description"]
        Book_price=request.POST["price"]
        Book_img=request.FILES["img"]
        obj=Book.objects.create(Book_name=select,Book_description=description,Book_price=Book_price,Book_image=Book_img)
        obj.save()
    return render(request,'add_Book.html')
   




@login_required(login_url='authentication-login')
def account_orders(request):
    user_id = request.session.get("user_ID")
    reg_id = user_reg.objects.get(user__id=user_id)
    
    data = orders.objects.filter(user_id__id=reg_id.id)
    
    
   
   
    
    return render(request,'account-orders.html',{"order_details":data}) 


def about_us(request):
    return render(request,'about-us.html')



@login_required(login_url='authentication-login')
def account_profile(request):
    user_id = request.session.get("user_ID")
    
    data = user_reg.objects.filter(user__id=user_id)
   

    return render(request,'account-profile.html',{"data":data})

@login_required(login_url='authentication-login')
def update_profile(request):
    user_id = request.session.get("user_ID")
    reg_id = user_reg.objects.get(user__id=user_id)

    if 'update' in request.POST:
        new_name = request.POST.get('u_name')
        new_email = request.POST.get('u_email')
        new_mobile = request.POST.get('u_mobile')
        new_gender = request.POST.get('u_gender') 
        new_dob = request.POST.get('u_dob')
        new_location = request.POST.get('u_location')

        # Update only if new value is provided; otherwise, keep the old value
        if new_name:
            reg_id.u_name = new_name
        if new_email:
            reg_id.u_email = new_email
        if new_mobile:
            reg_id.u_mobile = new_mobile
        if new_gender:
            reg_id.gender = new_gender
        if new_dob:
            reg_id.dob = new_dob
        if new_location:
            reg_id.location = new_location
        
        # Save the changes to the database
        reg_id.save()

        return redirect('account-profile')

    return render(request, 'account-edit-profile.html')










def account_saved_address(request):
    return render(request,'account-saved-address.html')


def address1(request):
    return render(request,'address.html')
 

def reset_password(request):
    return render(request,'authentication-reset-password.html')



def blog_post(request):
    return render(request,'blog-post.html')



@login_required(login_url='authentication-login')
def cart1(request):
    user_id = request.session.get("user_ID")
    reg_id = user_reg.objects.get(user__id=user_id)
    
    data = cart.objects.filter(user_id__id=reg_id.id)
   
    count = data.count()
   

    

    offer_price=0
    zipped_price=[]
    total=0
    for i in data:
        if i.qty is not None and i.Book_id.Book_price is not None and i.Book_id.Book_offer is not None:
            Book_price=i.Book_id.Book_price
            off_percentage=i.Book_id.Book_offer
            offered_price=int(Book_price) * (int(off_percentage) /100)
            offer_price=int(Book_price) - int(offered_price)
            total+=i.qty * offer_price
        zipped_price.append((i,offer_price))  
     
    offer=0
    offer_amount=0
    if  total >= 50000: 
         offer=int(total) * (int(2)/100)
         offer_amount=int(total) - int(offer) 
        


    
    bag_offer_price=0
        

    if total<=5000:
        grand_total=total+50
    else:
        grand_total=total

  
    
    context = {
        'count': count,
        'cart1': data,
        'grand_total':grand_total,
        'total': total,
        'offer_price':offer_price,
        'bag_offer_price':bag_offer_price,
        'zipped_price':zipped_price,
        'offer_amount_bag':offer_amount,
        'offer':offer,
        

    }

    return render(request, 'cart.html', context)


@login_required(login_url='authentication-login')
def addToWishlistFromCart(request,id):

    data=Book.objects.get(id=id)
  
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=wishlist.objects.create(user_id=user,Book_id=data)
    obj.save()
    
       
    return redirect('cart')



def contact_us(request):
    return render(request,'contact-us.html')

def payment_method(request):
    return render(request,'payment-method.html')
def index(request):
    # Fetch the featured and latest books, excluding those with quantity less than one
    featured_Book = Book.objects.filter(Book_qty__gte=1).order_by('priority')[:4]
    latest_Book = Book.objects.filter(Book_qty__gte=1).order_by('-id')[:8]
    
    # Prepare lists to hold processed data with discount information
    featured_books_with_price = []
    latest_books_with_price = []
    
    # Calculate price and offer details for featured books
    for book in featured_Book:
        original_price = book.Book_price
        offer_percentage = book.Book_offer
        discounted_price = original_price - (original_price * offer_percentage / 100)
        
        featured_books_with_price.append({
            'book': book,
            'original_price': original_price,
            'offer_percentage': offer_percentage,
            'discounted_price': discounted_price,
        })
    
    # Calculate price and offer details for latest books
    for book in latest_Book:
        original_price = book.Book_price
        offer_percentage = book.Book_offer
        discounted_price = original_price - (original_price * offer_percentage / 100)
        
        latest_books_with_price.append({
            'book': book,
            'original_price': original_price,
            'offer_percentage': offer_percentage,
            'discounted_price': discounted_price,
        })
    
    # Pass the processed data to the context
    context = {
        'featured_books_with_price': featured_books_with_price,
        'latest_books_with_price': latest_books_with_price,
    }
    
    return render(request, 'index.html', context)



@login_required(login_url='authentication-login')
def addToCart(request,id):
   
   
    data=Book.objects.get(id=id)
    amt=data.Book_price
    quantity=1
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=cart.objects.create(user_id=user,Book_id=data,qty=quantity,cart_amount=amt)
    obj.save()
    
       
    return redirect('index')
@login_required(login_url='authentication-login')

def addToCartFromWish(request,id):
   
    data=Book.objects.get(id=id)
    amt=data.Book_price
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=cart.objects.create(user_id=user,Book_id=data,cart_amount=amt)
    obj.save()
    
       
    return redirect('wishlist')

@login_required(login_url='authentication-login')
def removeCart(request,id):
    cart_remove=cart.objects.get(id=id)
    cart_remove.delete()


    return redirect('cart')
    

@login_required(login_url='authentication-login')

def addToWishlist(request,id):

    data=Book.objects.get(id=id)
    
   
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=wishlist.objects.create(user_id=user,Book_id=data)
    obj.save()
    
       
    return redirect('index')

@login_required(login_url='authentication-login')
def addToWishlistFromAllBooks(request,id):

    data=Book.objects.get(id=id)
    
   
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=wishlist.objects.create(user_id=user,Book_id=data)
    obj.save()
    
       
    return redirect('all-Books')

@login_required(login_url='authentication-login')
def addToCartFromAllBooks(request,id):
   
   
    data=Book.objects.get(id=id)
    amt=data.Book_price
    quantity=1
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=cart.objects.create(user_id=user,Book_id=data,qty=quantity,cart_amount=amt)
    obj.save()
    
       
    return redirect('all-Books')



def RemoveWishlist(request,id):
    wish_remove=wishlist.objects.get(id=id)
    wish_remove.delete()    
    return redirect('wishlist')



@login_required(login_url='authentication-login')
def Book_details(request, id1):
    u_id = request.session['user_ID']
    user = user_reg.objects.get(user__id=u_id)
    data = Book.objects.get(id=id1)

    if 'savereview' in request.POST:
        review1 = request.POST["review"]
        rating = request.POST["rating"]
        current_date = date.today()
        obj = review.objects.create(user_review=review1, user_rating=rating, review_date=current_date, user_id=user,
                                    Book_id=data)
        obj.save()

    reviews = review.objects.filter(Book_id=data)
 
    count = reviews.count()
   

    
    
    count_5star=review.objects.filter(Book_id=data, user_rating=5).count()
    count_4star=review.objects.filter(Book_id=data, user_rating=4).count()
    count_3star=review.objects.filter(Book_id=data, user_rating=3).count()
    count_2star=review.objects.filter(Book_id=data, user_rating=2).count()
    count_1star=review.objects.filter(Book_id=data, user_rating=1).count()
    sum_of_rating=review.objects.filter(Book_id=data)
    sum=0
    for s in sum_of_rating:
        sum+=s.user_rating
        
    average_rating=None
    if count>0:
     average_rating=round(int (sum) / int(count))
    price = data.Book_price
    off = data.Book_offer
    offer_price = 0
    if price is not None and off is not None:
        result = int(price) * (int(off) / 100)
        offer_price = int(price) - int(result)

    context = {
        'data': data,
        'offer_price': offer_price,
        'off': off,
        'reviews': reviews,
        'count': count,
        'average_rating': average_rating,
        'count_5star':count_5star,
        'count_4star':count_4star,
        'count_3star':count_3star,
        'count_2star':count_2star,
        'count_1star':count_1star,
        
    }

    if 'addToCart' in request.POST:
        qty = request.POST['qty']
        amt = offer_price
        amt = int(amt) * int(qty)
        u_id = request.session['user_ID']
        user = user_reg.objects.get(user__id=u_id)
        obj = cart.objects.create(user_id=user, Book_id=data, qty=qty, cart_amount=amt)
        obj.save()

    if 'wishlist' in request.POST:
        u_id = request.session['user_ID']
        user = user_reg.objects.get(user__id=u_id)
        obj = wishlist.objects.create(user_id=user, Book_id=data)
        obj.save()

    return render(request, 'Book-details.html', context)



def navbar(request):
    
    return render(request,'navbar.html')


@login_required(login_url='authentication-login')
def wishlist1(request):
    user_id=request.session.get("user_ID")
    reg_id=user_reg.objects.get(user__id=user_id)
    
    data=wishlist.objects.filter(user_id__id=reg_id.id)

    count=wishlist.objects.filter(user_id__id=reg_id.id).count()
    context={'count':count,
             'wishlist1':data
             
             }
   

    
    return render(request,'wishlist.html',context)

def all_Books(request):
    # Fetch all books with quantity greater than or equal to one
    Books = Book.objects.filter(Book_qty__gte=1)
    zipped_data = []

    for data in Books:
        price = data.Book_price
        off = data.Book_offer
        offer_price = 0
        
        if price is not None and off is not None:
            result = int(price) * (int(off) / 100)
            offer_price = int(price) - int(result)
        else:
            offer_price = int(price)
        
        zipped_data.append((data, offer_price))

    context = {
        'zipped_data': zipped_data
    }

    return render(request, 'all-Books.html', context)




def footer(request):
    return render(request,'footer.html')
def search(request):
    Book_name = None
    Book_author = None
    combined_results = None
    books_with_offer = []

    if 'search' in request.POST:
        searchtxt = request.POST.get('tosearch', '').strip()

        if searchtxt:
            # Fetch books based on name and author
            Book_name = Book.objects.filter(Book_name__icontains=searchtxt).order_by('-id')
            Book_author = Book.objects.filter(Book_author=searchtxt).order_by('-id')

            # Combine the results and remove duplicates using `distinct()`
            combined_results = (Book_name | Book_author).distinct()

            # Calculate the offer details for each book
            for book in combined_results:
                before_offer_price = book.Book_price
                offer_percentage = book.Book_offer
                after_offer_price = before_offer_price * (1 - offer_percentage / 100)

                # Create a dictionary to store the book's data along with offer info
                books_with_offer.append({
                    'book': book,
                    'before_offer_price': before_offer_price,
                    'offer_percentage': offer_percentage,
                    'after_offer_price': after_offer_price,
                })

    context = {
        "books_with_offer": books_with_offer,
    }

    return render(request, 'search.html', context)



@login_required(login_url='authentication-login')
def addToWishlistFromSearch(request,id):

    data=Book.objects.get(id=id)
    
   
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=wishlist.objects.create(user_id=user,Book_id=data)
    obj.save()
    
       
    return redirect('search')

@login_required(login_url='authentication-login')
def addToCartFromSearch(request,id):

    data=Book.objects.get(id=id)
    
   
    u_id=request.session['user_ID']
    user=user_reg.objects.get(user__id=u_id)
    obj=cart.objects.create(user_id=user,Book_id=data)
    obj.save()
    
       
    return redirect('search')










    




def billing_details(request):

    user_id = request.session.get("user_ID")
    reg_id = user_reg.objects.get(user__id=user_id)
    
    data = cart.objects.filter(user_id__id=reg_id.id)


   

    offer_price=0
    zipped_price=[]
    total=0
    for i in data:
        if i.qty is not None and i.Book_id.Book_price is not None and i.Book_id.Book_offer is not None:
            Book_price=i.Book_id.Book_price
            off_percentage=i.Book_id.Book_offer
            offered_price=int(Book_price) * (int(off_percentage) /100)
            offer_price=int(Book_price) - int(offered_price)
            total+=i.qty * offer_price
        zipped_price.append((i,offer_price))  
     
    offer=0
    offer_amount=0
    if  total >= 50000: 
         offer=int(total) * (int(2)/100)
         offer_amount=int(total) - int(offer) 
         
        


    
    bag_offer_price=0
        

    if total <= 5000:
        grand_total=total+50
    else:
        grand_total=total

    last_total=0
    if offer_amount >= 5000:
         last_total = offer_amount
    else:
          last_total = grand_total
    
    context = {
        
        'cart1': data,
        'grand_total':grand_total,
        'total':total,
        'offer_price':offer_price,
        'bag_offer_price':bag_offer_price,
        'zipped_price':zipped_price,
        
        'offer':offer,
        'last_total':last_total
        

    }


    k=cart.qty
    print(k)
    if request.POST:  
     for item in data:  
        qty = item.qty  

        f_name = request.POST["fname"]
        l_name = request.POST["lname"]
        email = request.POST["email"]
        mobile_number = request.POST["mobile_num"]
        street_address = request.POST["street_address"]
        pincode = request.POST["pincode"]
        city = request.POST["city"]
        country = request.POST["country"]
        current_date = date.today()

        BookID = item.Book_id

        obj = orders.objects.create(user_id=reg_id, Book_id=BookID, order_amount=last_total,
                                    ordered_qty=qty, ordered_date=current_date, first_name=f_name, last_name=l_name,
                                    email=email, mobile_num=mobile_number, street_address=street_address,
                                    pincode=pincode, city=city, country=country)

        obj.save()
        Book_id = item.Book_id.id
        pro = Book.objects.get(id=Book_id)
        pro.Book_qty -= int(qty)
        pro.save()

        data.delete()
        return redirect("cart")

        
    return render(request,'billing-details.html',context)




           
    
   



    








   

    







