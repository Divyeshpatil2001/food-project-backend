from rest_framework.views import APIView
from rest_framework import status
from .razorpay_serializers import CreateOrderSerializer,TransactionModelSerializer
from rest_framework.response import Response
from razorpay_backend.api.razorpay.main import RazorpayClient
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

rz_client = RazorpayClient()

class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        Create_Order_Serializer = CreateOrderSerializer(
            data = request.data
        )
        if Create_Order_Serializer.is_valid():
            order_response  = rz_client.create_order(
                amount=Create_Order_Serializer.validated_data.get("amount"),
                currency=Create_Order_Serializer.validated_data.get("currency")
                )
            response = {
                "status_code" : status.HTTP_201_CREATED,
                "message" : "order created",
                "data" : order_response
            }
            print(order_response)
            return Response(response,status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message" : "bad request",
                "error" : Create_Order_Serializer.errors
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
class TransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        transaction_serializer = TransactionModelSerializer(
            data = request.data
        )
        if transaction_serializer.is_valid():
            rz_client.verify_payment(
                razorpay_order_id=transaction_serializer.validated_data.get("order_id"),
                razorpay_payment_id=transaction_serializer.validated_data.get("payment_id"),
                razorpay_signature=transaction_serializer.validated_data.get("signature"),
            )
            transaction_serializer.save()
            response = {
                "status_code" : status.HTTP_201_CREATED,
                "message" : "transaction created"
            }
            return Response(response,status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "message" : "bad request",
                "error" : transaction_serializer.errors
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)