from django.http import Http404
from .models import VendorList,VendorDetails,VendorCredentials,VendorMedsSupply
from medicines.models import MedicineList
from .serializers import VendorListSerializer,VendorDetailsSerializer,VendorDetailsCreateSerializer,VendorCredentialsSerializer,VendorMedsSupplySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

# the following will be class based views. If you are new to this approach please refer 'https://www.django-rest-framework.or/tutorial/3-class-based-views/'.

class ListAllVendors(APIView):
    """
    list all vendors
    """
    def get(self, request, format=None):
        vendor_list = VendorList.objects.all()
        serializer = VendorListSerializer(vendor_list, many=True)
        return Response(serializer.data)

class SingleVendorDetailsView(APIView):
    """
    get details of single vendor
    """
    def get(self, request, name,  format=None):
        try:
            vendor_details = VendorList.objects.get(vendor_name = name)
            serializer = VendorListSerializer(vendor_details)
            return Response(serializer.data)
        except VendorList.DoesNotExist:
            return Response({"error": "vendor does not exist"}, status = status.HTTP_404_NOT_FOUND)

class VendorDetailsEntryView(APIView):
    """
    enter and update details of a vendor
    """
    def post(self, request, format=None):
        serializer = VendorDetailsCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            vendor = VendorList.objects.get(vendor_id = request.data["vendor_id"])
            serializer = VendorListSerializer(vendor, request.data)
            # for saving only name
            if serializer.is_valid():
                serializer.save()
            # for saving details
                if request.data["details"]:
                    vendor_details = VendorDetails.objects.get(vendor_id = vendor)
                    details = serializer.data["details"]
                    details.update({"vendor_id":serializer.data["vendor_id"]})
                    details_serializer = VendorDetailsCreateSerializer(vendor_details, data = details)
                    if details_serializer.is_valid();
                        details_serializer.save()
                        return Response({"name":serializer.data,"details":details_serializer.data}, status = status.HTTP_200_OK)
                    return Response(details_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except VendorList.DoesNotExist:
            return Response({"message":"Vendor Does Not Exist"}, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            vendor = VendorList.objects.get(vendor_id = request["vendor_id"])
            vendor_details = VendorDetails.objects.filter(vendor_id = vendor)
            delete_vendor_details = vendor_details.delete()
            return Response({"message":"Vendor details deleted successfully."}, status = status.HTTP_204_NO_CONTENT)
        except VendorList.DoesNotExist:
            return Response({"message":"Vendor not found."}, status =status.HTTP_400_BAD_REQUEST)

class GetVendorCredentials(APIView):
    """
    get and create vendor credentials
    """
    def get(self,request):
        vendor_creds = VendorCredentials.objects.all()
        serializer = VendorCredentialsSerializer(vendor_creds, many=True)
        return Response(serializer.data)
#   add vendor with credentials
    def post(self, request):
        name_entry_serializer = VendorListSerializer(data=request.data)
        if name_entry_serializer.is_valid():
            name_entry_serializer.save()
            request.data.update({"vendor_id":name_entry_serializer.data["vendor_id"]})
            credentials_serializer = VendorCredentialsSerializer(data=request.data)
            if credentials_serializer.is_valid():
                credentials_serializer.save()
                return Response({"nameEntry":name_entry_serializer.data,"credentialEntry":credentials_serializer.data}, status=status.HTTP_201_CREATED)
            return Response(credentials_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(name_entry_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class GetSingleVendorCredentials(APIView):
    """
    get fields from vendorCredentials model || get credentials of a single vendor
    """
    def get(self, request, id, format=None):
        try:
            vendor_credentials = VendorCredentials.objects.get(vendor_id = id)
            serializer = VendorCredentialsSerializer(vendor_credentials)
            return Response(serializer.data)
        except:
            return Response({"status": status.HTTP_404_NOT_FOUND})

class VendorMedsSupplyListView(APIView):
    def get(self, request):
        supplies = VendorMedsSupply.objects.all()
        serializer = VendorMedsSupplySerializer(supplies, many=True)
        return Response(serializer.data)

class VendorMedsSupplyDetailView(APIView):
    def get(self, request, pk):
        try:
            supply = VendorMedsSupply.objects.get(pk=pk)
            serializer = VendorMedsSupplySerializer(supply)
            return Response(serializer.data)
        except VendorMedsSupply.DoesNotExist:
            return Response({"error: supply details does not exist"},status = status.HTTP_400_BAD_REQUEST)
