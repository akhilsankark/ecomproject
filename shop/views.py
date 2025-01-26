from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ProductForm
from .models import Product, Cart, CartItem
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    tshirt= Product.objects.get(pk=6)
    tshirt.name="T-Shirt kakashi"
    tshirt.save()

    ref = Product.objects.get(pk=5)
    ref.name = "Godrej 5star"
    ref.save()

    product=Product.objects.all()
    #  product = Product.objects.filter('stock'>10)
    return render(request, 'home.html', {'product': product})

@login_required
def homepage(request):
    product = Product.objects.all()
    #  product = Product.objects.filter('stock'>10)
    return render(request, 'homepage.html', {'product': product})

@login_required
def add_products(request):
    if request.method == 'POST':
        productform = ProductForm(request.POST,request.FILES)
        if productform.is_valid():
            productform.save()
            return redirect('home')
    productform = ProductForm()
    return render(request,'add_products.html',{'forms':productform})

@login_required
def edit_products(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        productform = ProductForm(request.POST,request.FILES, instance=product)
        if productform.is_valid():
            productform.save()
            return redirect('home')

    productform = ProductForm(instance=product)

    return render(request, 'edit_products.html', {'forms': productform})

@login_required
def delete_products(request, pk):
    product=Product.objects.get(pk= pk)
    product.delete()
    return redirect('home')



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)

            if user.groups.filter(name='Seller').exists():
                messages.success(request, "Welcome Seller! Redirecting to your homepage.")
                return redirect('homepage')
            else:

                messages.success(request, "Welcome! Redirecting to the product page.")
                return redirect('userdash')

        else:
            messages.error(request, "Invalid Credentials")
            return redirect('signin')

    return render(request, 'signin.html')

def signup(request):
    if request.method == "POST":
        username =request.POST['username']
        password1 = request.POST['password1']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']

        myuser = User.objects.create_user(username=username, password=password1, email=email)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        return redirect('signin')
    return render(request,'signup.html')




def signout(request):
    logout(request)
    return redirect('home')

def products(request):
    product=Product.objects.all()
    #  product = Product.objects.filter('stock'>10)
    return render(request, 'products.html', {'product': product})




def seller_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']

        myuser = User.objects.create_user(username=username, password=password1, email=email)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        seller_group = Group.objects.get(name='Seller')
        myuser.groups.add(seller_group)

        return redirect('signin')
    return render(request, 'seller_signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            cart = request.GET.get('cart', 'default_redirect_url')
            return redirect(view_cart)
        else:

            return render(request, 'signin.html', {'error': 'Invalid credentials'})
    return render(request, 'signin.html')


def userdash(request):
    product=Product.objects.all()
    #  product = Product.objects.filter('stock'>10)
    return render(request, 'userdash.html', {'product': product})

@login_required
def add_prod_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'user': request.user})
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
        cart_item.save()
        if not created and cart_item.quantity >= product.stock:
            messages.error(request, "Cannot add more items than available stock.")
    return redirect('view_cart')

@login_required
def view_cart(request):
    total = 0
    counter = 0
    cart_items = None

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except Cart.DoesNotExist:
        pass

    return render(request, 'cartpage.html', {'cart_items': cart_items, 'total':total, 'counter':counter, 'cart':cart})

@login_required
def remove_prod_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')


@login_required
def remove_prod(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, product=product, cart=cart)
    cart_item.delete()

    return redirect('view_cart')


