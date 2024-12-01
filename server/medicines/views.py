from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MedicineList,CategoriesList,MedicineCategory
from .serializers import MedicineListSerializer,CategoriesListSerializer,MedicineCategorySerializer
from django.shortcuts import get_object_or_404
# Create your views here.

class MedicineListView(APIView):
    def get(self, request):
        medicines = MedicineList.objects.all()
        serializer = MedicineListSerializer(medicines, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = MedicineListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicineDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(MedicineList, pk=pk)
    def get(self, request, pk):
        medicine = self.get_object(pk)
        serializer = MedicineListSerializer(medicine)
        return Response(serializer.data)
    def put(self,request, pk):
        medicine = self.get_object(pk)
        serializer = MedicineListSerializer(medicine, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        medicine = self.get_object(pk)
        medicine.delete()
        return Response(status.HTTP_204_NO_CONTENT)

class CategoriesListView(APIView):
    def get(self, request):
        categories = CategoriesList.objects.all()
        serializer = CategoriesListSerializer(categories, many=True)
        return  Response(serializer.data)
    def post(self, request):
        serializer = CategoriesListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
class CategoriesDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(CategoriesList,pk=pk)
    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategoriesListSerializer(category)
        return Response(serializer.data)
    def put(self,request,pk):
        category = self.get_object(pk)
        serializer = CategoriesListSerializer(category, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    def delete(self,request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MedicineCategoryListView(APIView):
    def get(self, request):
        try:    
            medicine_categories = MedicineCategory.objects.all()
            serializer = MedicineCategorySerializer(medicine_categories, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"serializer_error":serializer.errors, "exception":e}, status = status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        data = request.data
        print(data)
        for entry in data:
            print(entry)
            serializer = MedicineCategorySerializer(data=entry)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
    
class MedicineCategoryDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(MedicineCategory, pk=pk)

    def get(self, request, pk):
        medicine_category = self.get_object(pk)
        serializer = MedicineCategorySerializer(medicine_category)
        return Response(serializer.data)

    def put(self, request, pk):
        medicine_category = self.get_object(pk)
        serializer = MedicineCategorySerializer(medicine_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        medicine_category = self.get_object(pk)
        medicine_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MedicineSearchView(APIView):
    """
    View for searching medicines either with full name or partial string
    """
    def get(self, request, *args, **kwargs):
        
        # Get the query from the URL 
        name = request.query_params.get('name','').strip()
        if not name:
            return Response({"error":"Query parameter 'name' is required. As in ../search/medicine?name='your medicine name'"},status=status.HTTP_400_BAD_REQUEST)
        
        # Search for medicines with a case-insensitive partial match, store them in "medicines"
        medicines = MedicineList.objects.filter(medicine_name__icontains=name)

        if not medicines.exists():
            return Response({"message":"No medicines found for the given search"}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the result
        serializer = MedicineListSerializer(medicines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategorySearchView(APIView):
    """
    Search for registered categories either by full string or partial string
    """
    def get(self, request, *args, **kwargs):

        """
        1. Fetch the name passed along the URL as a query string
        2. See if any matches with the name exists in CategoriesList
        3. If matches are found, return the serialized list of the filtered categories else return with a HTTP_404
        """
        
        # Get the query from the URL
        name = request.query_params.get('name','').strip()
        if not name:
            return Response({"error":"Query Parameter 'name' is required. As in ../search/category?name='your category name'"}, status=status.HTTP_400_BAD_REQUEST)

        # Search for categories with a case-insensitive partial match, store them in "categories"
        categories = CategoriesList.objects.filter(category_name__icontains=name)

        if not categories.exists():
            return Response({"message":"No categories found for the given search"}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the result
        serializer = CategoriesListSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        