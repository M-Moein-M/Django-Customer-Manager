from django.shortcuts import render, redirect
from .utils.account import is_user_authorized_to_visit_page, SaveCustomerSettings
from .utils.product import SaveNewProduct
from .utils.order import SaveNewOrder
from .forms import *
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
    if request.method == 'POST':
        SaveCustomerSettings(request).save_settings()
    customer = request.user.customer
    form_initial = {'name':customer.name,
                    'phone':customer.phone,
                    'email': customer.user.email}
    info_form = CustomerForm(data=form_initial, instance=customer)
    profile_pic_form = ProfilePictureForm()
    context = {'info_form': info_form,
               'profile_pic_form': profile_pic_form}

    return render(request, 'accounts/accounts_settings.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def home(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,
               'total_orders': total_orders,
                'delivered': delivered,
                'pending': pending}
    return render(request, 'accounts/user.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Account Was Created For {form.cleaned_data.get("username")}')

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def adminPage(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'customer'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def editProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        SaveNewProduct(request, edit_instance=product).create_new_product()
        return redirect('edit_product', pk=pk)
    tags = ', '.join([t.name for t in product.tags.all()])
    edit_form = NewProductForm(initial={'tags': tags},
                               instance=product)
    context = {'product_pic': product.product_pic,
               'edit_form': edit_form}
    return render(request, 'accounts/product_edit.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def newProduct(request):
    if request.method == 'POST':
        SaveNewProduct(request).create_new_product()
        return redirect('new_product')
    prodForm = NewProductForm()
    context = {'prodForm': prodForm}
    return render(request, 'accounts/new_product.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'customer'])
def customer(request, customer_id):
    authorized = is_user_authorized_to_visit_page(request.user, customer_id)
    if not authorized:
        return redirect('/')

    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,
               'orders': orders,
               'orders_count': orders_count,
               'myFilter': myFilter
               }

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def createOrder(request, pk):
    if request.method == 'POST':
        SaveNewOrder(request, pk).save_order()
        return redirect('products')

    product = Product.objects.get(id=pk)
    context = {'product_name': product.name,
               'product_pic': product.product_pic,
               'product_price': product.price,
               'new_order_form': NewOrderForm(initial={'quantity': 1})}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        return redirect('admin_page')

    context = {'product_pic': order.product.product_pic}
    return render(request, 'accounts/order_update.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete_order.html', context)
