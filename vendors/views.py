from gc import get_objects
from .models import VendorList,VendorDetails,VendorCredentials,VendorMedsSupply
from medicines.models import MedicineList
from .serializers import VendorListSerializer,VendorDetailsCreateSerializer,VendorCredentialsSerializer,VendorMedsSupplySerializer,VendorIdSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter, inline_serializer
from drf_spectacular.types import OpenApiTypes


from django.shortcuts import get_object_or_404

# Create your views here.

# the following will be class based views. If you are new to this approach please refer 'https://www.django-rest-framework.or/tutorial/3-class-based-views/'.

class ListAllVendors(APIView):
    """
    This view contains a GET endpoint to retrieve a 'List Of All Registered Vendors'.
    """
    @extend_schema(
            responses={
                200: VendorListSerializer(many=True)
                }
    )
    def get(self, request, format=None):
        """
        Description: This is a GET route that is associated with the endpoint ../vendors/vendorlist.\n
        Working: 
        1. This method accesses the model that contains the entries of all registered vendors
        2. Passes that accessed model instance to a serializer
        3. Then returns the data that is given out by the serializer
        """
        vendor_list = VendorList.objects.all()
        serializer = VendorListSerializer(vendor_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SingleVendorDetailsView(APIView):
    """
    This view contains a GET endpoint to be returned with the 'Details of a Single Vendor'.
    """
    @extend_schema(
            summary="get the details of a single vendor with the requested Vendor Name",
            parameters=[
                OpenApiParameter(
                    name="name",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.PATH,
                    description="The name of the vendor to be fetched",
                    examples=[
                        OpenApiExample(
                            name="Example Vendor Name",
                            value="test_vendor_01"
                        )
                    ]
                )
            ],
            responses={
                200: VendorListSerializer(),
                404: OpenApiResponse(
                    response={
                        "type":"object",
                        "properties":{
                            "error":{
                                "type":"string",
                                "example":"vendor does not exist"
                            }
                        },
                        "description":"Not Found - Vendor Does Not Exist",
                    }
                )
            },
    )
    def get(self, request, name,  format=None):
        """
        Description: This is a GET route that is associated with the endpoint ../vendors/singlevendor/<str:name>\n
        Working:
        1. This method accesses the model that contains entries of all registered vendors by passing in the vendor's name as the parameter.
        2. Passes that accessed model instance to a serializer
        3. Then returns the data that is given out by the serializer
        """
        try:
            vendor_details = VendorList.objects.get(vendor_name = name)
            serializer = VendorListSerializer(vendor_details)
            return Response(serializer.data)
        except VendorList.DoesNotExist:
            return Response({"error": "vendor does not exist"}, status = status.HTTP_404_NOT_FOUND)

class VendorDetailsEntryView(APIView):
    """
    POST: Create a new Vendor along with the details.\n
    PUT: Update the vendor's name and/or details.\n
    DELETE: Delete vendor details using vendor_id.
    """
    @extend_schema(
            description="Create a new Vendor along with the details.",
            summary="Create Vendor Details",
            request=VendorDetailsCreateSerializer,
            responses={
                201:VendorDetailsCreateSerializer,
                400:OpenApiResponse(
                    response=OpenApiTypes.OBJECT,
                    description="Bad Request - Invalid Body Content"
                )
            },
            examples=[
                OpenApiExample(
                    name='Schema Example',
                    value={
                        "vendor_id": 0,
                        "vendor_address": "string",
                        "vendor_dln": "string",
                        "vendor_contact": "string",
                        "vendor_email": "string",
                        "vendor_coordinates": "string"
                    },      
                    request_only=True,
                    response_only=False
                ),
                OpenApiExample(
                    name='Value Example',
                    value={
                        "vendor_id":1,
                        "vendor_address":"Telangana, India",
                        "vendor_dln":"AVBGD1122F",
                        "vendor_contact":"9848238660",
                        "vendor_email":"test_vendor_01@gmail.com",
                        "vendor_coordinates":"41.40338,2.17403"
                    },
                    request_only=True,
                    response_only=False
                )
            ]
    )
    def post(self, request, format=None):
        serializer = VendorDetailsCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @extend_schema(
            description="Update the vendor's name and/or details.",
            summary="Update Any Of The Vendor's Details",
            request=VendorListSerializer,
            responses={
                200:VendorListSerializer,
                400:OpenApiTypes.OBJECT
            },
            examples=[
                OpenApiExample(
                    name='Only Name/ Minimal Entry',
                    description='If only vendor\'s name needs to be changed',
                    value={
                        "vendor_id": "int",    
                        "vendor_name": "string"
                    },
                    request_only=True,
                    response_only=False
                ),
                OpenApiExample(
                    name='Name and Details/ Brief Entry',
                    description='Use this format to change any field of the vendor\'s details',
                    value={
                        "vendor_id": 0,
                        "vendor_name": "string",
                        "details": {
                            "vendor_address": "string",
                            "vendor_dln": "string",
                            "vendor_contact": "string",
                            "vendor_email": "string",
                            "vendor_coordinates": "string"
                        }
                    },
                    request_only=True,
                    response_only=False,
                )
            ]     
    )
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

    @extend_schema(
            summary='Delete Vendor Details',
            description='Delete vendor details by passing `vendor_id` in the `request_body`. Example:`{\'vendor_id\'`:`\'integer\'}`',
            request=VendorIdSerializer,
            responses={
                204:OpenApiResponse(
                    description='NO_CONTENT',
                    response={
                        'type':'object',
                        'properties':{
                            'message':{
                                'type':'string',
                                'example':'Vendor details deleted successfully'    
                            }
                        },
                        'description':'Vendor details will be deleted'
                    }
                ),
                400:OpenApiResponse(
                    description='BAD_REQUEST',
                    response={
                        "type":"object",
                        "properties":{
                            "message":{
                                "type":"string",
                                "example":"Vendor not found."
                            }
                        },
                        "description":"Bad_Request - Vendor Not Found"
                    }
                )
            },
            examples=[
                OpenApiExample(
                    name='Delete Vendor Example',
                    description='Delete the vendor by passing vendor_id in the body',
                    value={
                        'vendor_id':1
                    },
                    request_only=True,
                    response_only=False
                )
            ]
    )
    def delete(self, request, format=None):
        try:
            vendor_id = request.data["vendor_id"]
            vendor = VendorList.objects.get(vendor_id=vendor_id)
            vendor_details = VendorDetails.objects.filter(vendor_id = vendor)
            delete_vendor_details = vendor_details.delete()
            return Response({"message":"Vendor details deleted successfully."}, status = status.HTTP_204_NO_CONTENT)
        except VendorList.DoesNotExist:
            return Response({"message":"Vendor not found."}, status =status.HTTP_400_BAD_REQUEST)

class GetVendorCredentials(APIView):
    """
    get and create vendor credentials
    """
    @extend_schema(
            description='Fetch credentials of all the vendors',
            summary='Get all vendor\'s credentials',
            responses=VendorCredentialsSerializer(many=True)
    )
    def get(self,request):
        vendor_creds = VendorCredentials.objects.all()
        serializer = VendorCredentialsSerializer(vendor_creds, many=True)
        return Response(serializer.data)

    @extend_schema(
            summary='Make an entry of vendor\'s credentials',
            description='This is the first route to be accessed before any other vendor\'s routes. When posting details via this route, the vendor will get their first entry/footprint, getting them added into the vendor_list and getting assigned with an `id` which shall then be referenced as `vendor_id` for future and subsequent api calls regarding the vendor.',
            request=inline_serializer(
                name='VendorFirstFootprint',
                fields={
                    'vendor_name':serializers.CharField(),
                    'vendor_email':serializers.CharField(),
                    'vendor_key':serializers.CharField()
                }
            ),
            responses={
                201:OpenApiResponse(
                    response={
                        'type':'object',
                        'properties':{
                            'nameEntry':{
                                'type':'object',
                                'properties':{
                                    'vendor_id':{
                                        'type':'integer'
                                    },
                                    'vendor_name':{
                                        'type':'string'
                                    },
                                    'details':{
                                        'type': ['object','null'],
                                        'description':'Additional details about the vendor (nullable)'
                                    }
                                }
                            },
                            'credentialEntry':{
                                'type':'object',
                                'properties':{
                                    'vendor_id':{
                                        'type':'integer',
                                    },
                                    'vendor_email':{
                                        'type':'string'
                                    },
                                    'vendor_key':{
                                        'type':'string'
                                    }
                                }
                            }
                        },
                        'description':'Created - Returns `nameEntry` and `credentialEntry` objects'
                    },
                    description='Enter first instance of name and credentials of the vendor'
                )
            }
    )
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
        

