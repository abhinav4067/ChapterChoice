from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('authentication-register/',views.user_registration,name='authentication-register'),
    path('authentication-login/', views.login1, name='authentication-login'),
    path('account-dashboard/',views.dashboard,name='account-dashboard'),
   
    path('add_Book/',views.add_Book,name='add_Book'),
  
    path('account-orders/',views.account_orders,name='account-orders'),
    path('about-us/',views.about_us,name='about-us'),
    path('Book-details/<id1>',views.Book_details,name='Book-details'),
    path('account-profile/',views.account_profile,name='account-profile'),
    path('account-edit-profile/',views.update_profile,name='account-edit-profile'),
    path('account-saved-address/',views.account_saved_address,name='account-saved-address'),
    path('address/',views.address1,name='address'),
    path('addToCart/<id>',views.addToCart,name='addToCart'),
    path('removeCart/<id>',views.removeCart,name='removeCart'),
    path('addToWishlist/<id>',views.addToWishlist,name='addToWishlist'),
    path('RemoveWishlist/<id>',views.RemoveWishlist,name='RemoveWishlist'),

    path('authentication-reset-password/',views.reset_password,name='authentication-reset-password'),
    
    path('billing-details/',views.billing_details,name='billing-details'),
    
   
    path('cart/',views.cart1,name='cart'),  
    path('addToWishlistFromCart/<id>',views.addToWishlistFromCart,name='addToWishlistFromCart'),
    path('contact-us/',views.contact_us,name='contact-us'),
    path('payment-method/',views.payment_method,name='payment-method'),
    path('wishlist/',views.wishlist1,name='wishlist'),
    path('addToCartFromWish/<id>',views.addToCartFromWish,name='addToCartFromWish'),

    path('all-Books/', views.all_Books,name='all-Books'), 
    path('addToWishlistFromAllBooks/<id>',views.addToWishlistFromAllBooks,name='addToWishlistFromAllBooks'),
    path('addToCartFromAllBooks/<id>',views.addToCartFromAllBooks,name='addToCartFromAllBooks'),
    path('navbar/',views.navbar,name='navbar'),
    path('footer/',views.footer,name='footer'),
    path('SignOut/',views.SignOut,name='SignOut'),
    path('search/',views.search,name='search'),
    path('addToCartFromSearch/<id>',views.addToCartFromSearch,name='addToCartFromSearch'),
    path('addToWishlistFromSearch/<id>',views.addToWishlistFromSearch,name='addToWishlistFromSearch'),
    
    
    
   

]