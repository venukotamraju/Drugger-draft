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
