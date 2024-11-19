from gc import get_objects
from django.http import Http404
from .models import VendorList,VendorDetails,VendorCredentials,VendorMedsSupply
from medicines.models import MedicineList
from .serializers import VendorListSerializer,VendorDetailsSerializer,VendorDetailsCreateSerializer,VendorCredentialsSerializer,VendorMedsSupplySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

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
                    if details_serializer.is_valid():
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
    """
    get vendor-medicine model fields of all the entries
    """
    def get(self, request):
        supplies = VendorMedsSupply.objects.all()
        serializer = VendorMedsSupplySerializer(supplies, many=True)
        return Response(serializer.data)
    
class VendorMedsSupplyDetailView(APIView):
    """
    functions for getting, posting and deleting medicinal supplies of individual vendors
    """
    def get(self, request, pk):
        try:
            supply = VendorMedsSupply.objects.get(pk=pk)
            serializer = VendorMedsSupplySerializer(supply)
            return Response(serializer.data)
        except VendorMedsSupply.DoesNotExist:
            return Response({"error: supply details does not exist"},status = status.HTTP_400_BAD_REQUEST)

class VendorMedicineLinkView(APIView):
    """
    View containing post route to link vendor and his chosen medicine from medicine search
    """

    # Post route to link vendor with their chosen medicine by taking vendor_id from URL params and medicine_id as a payload
    def post(self, request, vendor_id):
        
        # Validate if the vendor exists
        try:
            vendor = VendorList.objects.get(vendor_id=vendor_id)
        except VendorList.DoesNotExist:
            return Response({"error":"Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        # Extract and validate medicine_id from the request body
        medicine_id = request.data.get('medicine_id','')
        print(medicine_id)
        if not medicine_id:
            return Response({"error":"'medicine_id' field is required as a payload with some value."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate id the medicine exists
        try:
            medicine = MedicineList.objects.get(medicine_id=medicine_id)
        except MedicineList.DoesNotExist:
            return Response({"error":"Medicine not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the link already exists
        if VendorMedsSupply.objects.filter(vendor_id=vendor, medicine_id=medicine).exists():
            return Response({"message":"This medicine is already linked to the vendor"}, status=status.HTTP_200_OK)
        
        # Create Link
        VendorMedsSupply.objects.create(vendor_id=vendor.vendor_id,medicine_id=medicine.medicine_id)
        return Response({"message":"Medicine Linked Successfully"}, status=status.HTTP_201_CREATED)

class VendorMedicineCreateView(APIView):
    """
    View containg a post method for vendor to create/register an unfound medicine from the medicine-search into the MedicineList
    """
    
    def post(self, request, vendor_id):
        # This method allows vendor to add a new medicine entry into the MedicineList if the medicine that the vendor is searching for is not found or has already been registered
        """
        1. Validate the vendor that is trying to add the medicine with vendor_id from the URL
        2. Check if the payload has medicine_name and validate if it has some value or not
        3. Check if the medicine with provided medicine_name already exists or create a new entry in the database
        4. If the medicine exists then check if the link is present between the vendor and the medicine and respond back if the link exists
        5. If the link does not exist then create a new entry of link in VendorMedsSupply with the medicine instance therefore created or returned from step 3.
        6. Return appropriate reponses stating of both the cases - New medicine entry is created and linked | Existing medicine entry is linked.
        """
        # Validate that the vendor exists
        try:
            vendor = VendorList.objects.get(vendor_id = vendor_id)
        except VendorList.DoesNotExist:
            return Response({"error":"Vendor does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Extract and Validate the medicine name from the request body
        medicine_name = request.data.get('medicine_name')
        if not medicine_name:
            return Response({"error":"'medicine_name' field is required as a payload with some appropriate name of the medicine"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if medicine already exists
        medicine, created = MedicineList.objects.get_or_create(medicine_name = medicine_name)

        # Check if the vendor-medicine link already exists
        if VendorMedsSupply.objects.filter(vendor_id=vendor, medicine_id=medicine).exists():
            return Response({"message":"This medicine has an entry and is already linked to the vendor"}, status=status.HTTP_200_OK)
        
        # Else link the medicine instance (newly created or already present) to the vendor
        VendorMedsSupply.objects.create(vendor_id=vendor.vendor_id,medicine_id=medicine.medicine_id)

        # Respond with appropriate success message
        if created:
            return Response({"message":"New medicine created and linked successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"Existing medicine linked successfully"}, status=status.HTTP_200_OK)
        

