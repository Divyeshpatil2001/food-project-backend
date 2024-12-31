from rest_framework.views import APIView
from rest_framework import status
from .razorpay_serializers import CreateOrderSerializer,TransactionModelSerializer
from rest_framework.response import Response
from razorpay_backend.api.razorpay.main import RazorpayClient
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import Transaction 

import json


rz_client = RazorpayClient()

class CreateOrderAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        print("Request data:", request.data)
        Create_Order_Serializer = CreateOrderSerializer(
            data = request.data
        )
        if Create_Order_Serializer.is_valid():
            print("andr")
            try:
                order_response = rz_client.create_order(
                    amount=Create_Order_Serializer.validated_data.get("amount"),
                    currency=Create_Order_Serializer.validated_data.get("currency")
                )
            except Exception as e:
                print("Razorpay error:", str(e))
                return Response(
                    {
                        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "message": "Razorpay order creation failed",
                        "error": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            print(order_response)
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
        
class RazorpayWebhook(APIView):
    @csrf_exempt
    def post(self, request):
        payload = request.body
        event = None

        try:
            event = json.loads(payload)
        except ValueError as e:
            # Invalid payload
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle the event based on the type
        if event['event'] == 'payment.authorized':
            # Example: You can update your database or trigger actions here
            payment_id = event['payload']['payment']['entity']['id']
            order_id = event['payload']['payment']['entity']['order_id']
            signature = event['payload']['payment']['entity']['signature']
            amount = event['payload']['payment']['entity']['amount']

            # Verify payment and save transaction
            try:
                rz_client.verify_payment(razorpay_order_id=order_id, razorpay_payment_id=payment_id, razorpay_signature=signature)
                Transaction.objects.create(payment_id=payment_id, order_id=order_id, signature=signature, amount=amount)
            except Exception as e:
                # Handle verification failure
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'status': 'success'})