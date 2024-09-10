from rest_framework import serializers
from .models import MedicineList,CategoriesList,MedicineCategory

# serializer for CategoriesList
class CategoriesListSerializer(serializers.ModelSerializer):
    medicines = serializers.SerializerMethodField()
    class Meta:
        model = CategoriesList
        fields = ['category_id','category_name', 'medicines']
        
    def get_medicines(self,obj):
        medicines = MedicineCategory.objects.filter(category_id=obj.category_id)
        return [medicine.medicine_id.medicine_name for medicine in medicines]

# serializer for MedicineCategory
class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = '__all__'

# serializer for MedicineList
class MedicineListSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    class Meta:
        model = MedicineList
        fields = ['medicine_id','medicine_name','categories']
    def get_categories(self,obj):
        category_list = MedicineCategory.objects.filter(medicine_id=obj.medicine_id)
        category_names = [category.category_id.category_name for category in category_list]
        return category_names
