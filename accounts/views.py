from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import viewsets
from .models import User,Profile
from .serializer import UserSerializer,ProfileSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.models import OutstandingToken
# Create your views here.
class UserViews(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    def create(self,request,*args,**kwargs):
        mutable_data = request.data.copy()
        mutable_data['password'] = make_password(mutable_data['password'])
        serializer = self.serializer_class(data=mutable_data)
        if serializer.is_valid():
            serializer.save()               
            return Response({'message':'user craete with passwordhash'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # def logout_view(self,request,*args,**kwargs):
    #     logout(request)
    
    #     return redirect('/login')
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    
class LoginViews(viewsets.ViewSet):
    @action(detail=False,methods=['post'])
    def login(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        # payload = {
        #     'id': user.id,
        #     'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     'iat':datetime.datetime.utcnow()
        # }
        
        # token = jwt.encode(payload,'secret',algorithm='HS256')
        refresh = RefreshToken.for_user(user)
        print(refresh)
        if user.is_superuser:
            # print("admin user")
            user_admin_status = True
        else:
            user_admin_status = False
        user_serializer = UserSerializer(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_admin_status':user_admin_status,
            'user_id' : user.id,
            'user_detail':user_serializer.data
        }, status=status.HTTP_200_OK)
        
        # return Response({'token':token},status=status.HTTP_200_OK)
class RefreshTokenView(APIView):
    def post(self, request):
        print(self,request)
        try:
            print("hi")
            
            refresh_token = request.data['refresh_token']
            print("refresht",refresh_token)
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            print("token",access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  
# class LogoutViews(viewsets.ViewSet):
#     @action(detail=False,methods=['post'])
#     def logout(self,request):
#         auth_header = request.META['HTTP_AUTHORIZATION']
#         # print(request.META)
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return Response({'error': 'Authorization header with Bearer token is required'}, status=status.HTTP_400_BAD_REQUEST)
#         refresh_token = auth_header.split(' ')[1]
#         # print(refresh_token, "refresh token")
    
        
#         try:
#             token = RefreshToken(refresh_token)
#             print(token, "token")
#             token.blacklist()
#             return Response({'message':'logout succesfull'},status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutViews(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def logout(self, request):
        print("ok")
        refresh_token = request.data.get("refresh_token")
        
        print(refresh_token)
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print(refresh_token)
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
