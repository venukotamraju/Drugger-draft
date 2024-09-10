from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomerList,CustomerDetails,CustomerSearch,CustomerOTP
from .serializers import CustomerListSerializer,CustomerDetailsSerializer,CustomerOTPSerializer
from .verification import MessageHandler

# Create your views here.

class CustomerListView(APIView):
    def get(self,request):
        customers = CustomerList.objects.all()
        serializer = CustomerListSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self,request):
        print(request.data)
        customer_serializer = CustomerListSerializer(data=request.data)
        if customer_serializer.is_valid():
            customer = customer_serializer.save()
            details_data = request.data.get('details',{})
            details_data['customer_id']=customer.customer_id
            details_serializer = CustomerDetailsSerializer(data=details_data)
            if details_serializer.is_valid():
                details = details_serializer.save()
                return Response(customer_serializer.data,status=status.HTTP_201_CREATED)
            return Response(details_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(customer_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        print(request.data)
        try:
            customer = CustomerList.objects.get(customer_id = request.data["customer_id"])
            serializer = CustomerListSerializer(customer, data = request.data)
            # FOR CUSTOMER NAME
            if serializer.is_valid():
                serializer.save()
            # FOR CUSTOMER DETAILS
                if request.data['details']:
                    details = request.data["details"]
                    details.update({"customer_id":serializer.data["customer_id"]})
                    details_instance = CustomerDetails.objects.get(customer_id = customer)
                    details_serializer = CustomerDetailsSerializer(details_instance, data = details)
                    if details_serializer.is_valid():
                        details_serializer.save()
                        return Response({"name":serializer.data,'details':details.serializer.data},status = status.HTTP_200_OK)
                    return Response({'name':serializer.data,'details':data_serializer.errors},status = HTTP_206_PARTIAL_CONTENT)
                return Response(serializer.data,status = HTTP_202_ACCEPTED)
            return Response(serializer.errors,status = HTTP_400_BAD_REQUEST)
        except CustomerList.DoesNotExist:
            return Response({"message":"Customer Does Not Exist"}, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            customer = CustomerList.objects.get(customer_id = request.data['customer_id'])
            details = CustomerDetails.objects.filter(customer_id = customer)
            details.delete()
            return Response({'message':'Customer Details Deleted Successfully'}, status = status.HTTP_204_NO_CONTENT)
        except CustomerList.DoesNotExist:
            return Response({'message':'Customer Does Not Exist'},status = status.HTTP_400_BAD_REQUEST)

class CustomerDetailView(APIView):
    def get(self,request,pk):
        try:
            customer = CustomerList.objects.get(pk=pk)
            serializer = CustomerListSerializer(customer)
            return Response(serializer.data)
        except CustomerList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GenerateOTPView(APIView):
    def post(self, request, pk):
        try:
            customer = CustomerList.objects.get(pk=pk)
            customer_details = CustomerDetails.objects.get(pk=pk)
            otp_instance, created = CustomerOTP.objects.get_or_create(customer_id=customer)
            otp_instance.generate_otp()
            serializer = CustomerOTPSerializer(otp_instance)
            # logic to send OTP to customer_contact can be added here
            message_handler_instance = MessageHandler(phone_number=customer_details.customer_contact,otp=otp_instance.otp)
            send_otp = message_handler_instance.send_otp()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except CustomerList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ValidateOTPView(APIView):
    def post(self, request, pk):
        try:
            customer = CustomerList.objects.get(pk=pk)
            otp_instance = CustomerOTP.objects.filter(customer_id=customer).latest('created_at')
            otp_provided = request.data.get('otp')
            if otp_instance.otp == otp_provided and otp_instance.is_valid():
                return Response({"message": "OTP is valid"}, status=status.HTTP_200_OK)
            return Response({"message": "OTP is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
        except (CustomerList.DoesNotExist, CustomerOTP.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)