from rest_framework import serializers
from .models import CustomerList,CustomerDetails,CustomerSearch,CustomerOTP



# serializer for CustomerDetails
class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = ['customer_id','customer_contact','customer_coordinates']

# serializer for CustomerList
class CustomerListSerializer(serializers.ModelSerializer):
    details = CustomerDetailsSerializer(source='customerdetails',read_only=True)
    class Meta:
        model = CustomerList
        fields = ['customer_id','customer_name','details']

# serializer for CustomerSearch
class CustomerSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSearch
        fields = ['customer_id','customer_search']

# serializer for customer otp
class CustomerOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOTP
        fields = '__all__'
