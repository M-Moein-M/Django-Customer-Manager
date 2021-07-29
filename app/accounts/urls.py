from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.redirectHome, name='home'),
    path('customer-page/', views.home, name='customer_page'),
    path('customer/<str:customer_id>/<str:page>', views.customer, name='customer'),

    path('products/', views.products, name='products'),
    path('admin-products/', views.adminProducts, name='admin_products'),
    path('customer-products/', views.customerProducts, name='customer_products'),
    path('products/new/', views.newProduct, name='new_product'),
    path('products/edit/<str:pk>', views.editProduct, name='edit_product'),
    path('products/delete/<str:pk>', views.deleteProduct, name='delete_product'),

    path('order/new/<str:pk>', views.createOrder, name='create_order'),
    path('order/update/<str:pk>', views.updateOrder, name='update_order'),
    path('order/all/<str:page>', views.showOrders, name='all_order'),
    path('order/delete/<str:pk>', views.deleteOrder, name='delete_order'),

    path('register', views.RegisterPage.as_view(), name='register'),
    path('login', views.LoginPage.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),

    path('admin-page/', views.adminPage, name='admin_page'),

    path('account', views.accountSettings, name='account_settings'),

    path('reset_password',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_complete'),
]
