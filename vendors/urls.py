from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('vendorlist/',views.ListAllVendors.as_view(), name='vendor-list'),
    path('vendordetails/',views.VendorDetailsEntryView.as_view(), name='vendor-details-entry'),
    path('singlevendor/<str:name>',views.SingleVendorDetailsView.as_view(),name='single-vendor-details'),
    path('vendorcredentials/',views.GetVendorCredentials.as_view(),name='vendor-credentials'),
    path('singlevendorcredentials/<int:id>',views.GetSingleVendorCredentials.as_view(),name='single-vendor-credentials'),
    path('supplies/',views.VendorMedsSupplyListView.as_view(), name = 'vendor-meds-supply-list'),
    path('supplies/<int:pk>', views.VendorMedsSupplyDetailView.as_view(), name = 'vendor-meds-supply-detail'),
    path('supplies/<int:vendor_id>/medicine/add/', views.VendorMedicineLinkView.as_view(), name = 'vendor-medicine-add'),
    path('supplies/<int:vendor_id>/medicine/create/',views.VendorMedicineCreateView.as_view(), name='vendor-medicine-create'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
