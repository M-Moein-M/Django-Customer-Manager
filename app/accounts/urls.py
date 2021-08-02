from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.RedirectHome.as_view(), name='home'),
    path('customer-page/', views.Home.as_view(), name='customer_page'),
    path('customer/<str:customer_id>/<str:page>', views.CustomerOrders.as_view(), name='customer'),

    path('products/', views.Products.as_view(), name='products'),
    path('admin-products/', views.Products.as_view(), name='admin_products'),
    path('customer-products/', views.Products.as_view(), name='customer_products'),

    path('packs/new/', views.NewPack.as_view(), name='new_pack'),
    path('packs/edit/<str:pk>', views.EditPack.as_view(), name='edit_pack'),

    path('products/new/', views.NewProduct.as_view(), name='new_product'),
    path('products/edit/<str:pk>', views.EditProduct.as_view(), name='edit_product'),
    path('products/edit/add-to-pack/<str:pk>', views.AddProductToPack.as_view(), name='add_product_to_pack'),
    path('products/delete/<str:pk>', views.DeleteProduct.as_view(), name='delete_product'),

    path('order/new/<str:pk>', views.CreateOrder.as_view(), name='create_order'),
    path('order/update/<str:pk>', views.UpdateOrder.as_view(), name='update_order'),
    path('order/all/<str:page>', views.ShowOrders.as_view(), name='all_order'),
    path('order/delete/<str:pk>', views.DeleteOrder.as_view(), name='delete_order'),

    path('register', views.RegisterPage.as_view(), name='register'),
    path('login', views.LoginPage.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),

    path('admin-page/', views.AdminPage.as_view(), name='admin_page'),

    path('account', views.AccountSettings.as_view(), name='account_settings'),

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
