from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('',views.home, name='home'),
    path('homepage/', views.homepage, name='homepage'),
    path('add_products/', views.add_products, name='add_products'),
    path('edit_products/<int:product_id>/', views.edit_products, name='edit_products'),
    path('delete_products/<int:pk>/', views.delete_products, name='delete_products'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('products/', views.products, name='products'),
    path('seller_signup/', views.seller_signup, name='seller_signup'),
    path('userdash/', views.userdash, name='userdash'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_prod_cart, name='addtocart'),
    path('remove/<int:product_id>/', views.remove_prod_cart, name='removefromcart'),
    path('prodremove/<int:product_id>/', views.remove_prod, name='completeremovecart'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)