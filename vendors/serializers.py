from rest_framework import serializers
from .models import VendorList, VendorDetails, VendorCredentials, VendorMedsSupply
from medicines.serializers import MedicineListSerializer
from medicines.models import MedicineList

# serializer for the model VendorDetails
class VendorDetailsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = VendorDetails
        fields = ['vendor_address','vendor_dln','vendor_contact','vendor_email','vendor_coordinates']


# serializer for the model VendorList and display the VendorDetails
class VendorListSerializer(serializers.ModelSerializer):
    details = VendorDetailsSerializer(source='vendordetails',read_only=True)
    class Meta:
        model = VendorList
        fields = ['vendor_id','vendor_name','details']


# serializer to create into VendorDetails
class VendorDetailsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetails
        fields = '__all__'
        
# serializer for the model VendorCredentials
class VendorCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorCredentials
        fields = ['vendor_id','vendor_email','vendor_key']

# serializer for the model VendorMedsSupply
class VendorMedsSupplySerializer(serializers.ModelSerializer):
    medicine_details = serializers.SerializerMethodField()
    class Meta:
        model = VendorMedsSupply
        fields = ['vendor_id','medicine_details']
        
    def get_medicine_details(self,obj):
        # Ensure the medicine_id references a valid MedicinesList object
        try:
            medicine = MedicineList.objects.get(medicine_id = obj.medicine_id)
            return MedicineListSerializer(medicine).data
        except MedicinesList.DoesNotExist:
            return None
