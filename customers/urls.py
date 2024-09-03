from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from customers import views

urlpatterns = [
        path('customerlist/', views.CustomerListView.as_view(),name='customer-list'),
        path('customerdetails/<int:pk>/', views.CustomerDetailView().as_view(),name='single-customer-detail'),
        path('customerverification/<int:pk>/generate-otp/', views.GenerateOTPView.as_view(), name='generate-otp'),
        path('customerverification/<int:pk>/validate-otp/',views.ValidateOTPView.as_view(), name='validate-otp'),
        ]

urlpatterns = format_suffix_patterns(urlpatterns)
