from django.urls import path
from .views import MedicineListView, MedicineDetailView, CategoriesListView, CategoriesDetailView, MedicineCategoryListView, MedicineCategoryDetailView, MedicineSearchView
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('medicines/',MedicineListView.as_view(), name = 'medicines-list'),
    path('medicines/<int:pk>/',MedicineDetailView.as_view(),name='medicine-details'),
    path('search/medicine/<str:name>',MedicineSearchView.as_view(),name='medicine-search'),
    path('categories/',CategoriesListView.as_view(), name = 'categories_list'),
    path('categories/<int:pk>/',CategoriesDetailView.as_view(), name = 'category-details'),
    path('medicine-categories/',MedicineCategoryListView.as_view(),name = 'medicine-category-list'),
    path('medicine-categories/<int:pk>/',MedicineCategoryDetailView.as_view(),name='medicine-category-details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
