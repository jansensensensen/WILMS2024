import json
import random
import string
from rest_framework_simplejwt.authentication import JWTAuthentication
import uuid

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import *
# from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import Booking,Venue,Attendee
from api.serializers import BookingSerializer, UserRulesrializer, VenueSerializer,BookingRequestSerializer,UserSerializer,AttendeeSerializer,EventsSerializer
from wallet.models import User as WalletUser
from wallet.models import UserProfileInfo
# from rest_framework.permissions import IsAuthenticated,AllowAny
from api.jwt_util import decode_user
from datetime import datetime, date, timedelta
from rest_framework.decorators import api_view,authentication_classes,permission_classes
# from django.contrib.auth.models import User
from django.http import JsonResponse
from facility.models import CalendarEvent, UserType_Rules,Facility
# from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class CalendarController():
    # @api_view(['GET'])
    # def getAllBooking(request):        
    #     obj = Booking.objects.all()
    #     serializer = BookingSerializer(obj,many=True)
    #     return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    
    @api_view(['GET'])   
    
    def getCurrentBookings(request):
        # try:
        #     auth_header=request.META['HTTP_AUTHORIZATION']
        # except:
        #     return Response({"unauthorized":"no token"},status=status.HTTP_401_UNAUTHORIZED)
        # # pra mawa ang word na Bearer
        # token=auth_header[7:len(auth_header)+1]
        # print(token)
        # user=decode_user(token)
        # owner=user['user_id']
        # if not owner:
        #     return Response({"unauthorized":"unauthorized"},status=status.HTTP_401_UNAUTHORIZED)
        
        week_start = date.today()
        # week_start -= timedelta(days=week_start.weekday())
        week_end = week_start + timedelta(days=14)        
        obj = Booking.objects.filter(date__gte=week_start,date__lte=week_end,status="Booked",)
        serializer = BookingSerializer(obj,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @api_view(['POST'])
    def saveBooking(request):       
        if request.method=='POST':
            serializer= BookingRequestSerializer(data=request.data)   
                
            if serializer.is_valid():
                points=serializer.validated_data['points']
                coins=serializer.validated_data['coins']
                # calculate hours_difference
                date=serializer.validated_data['date']      
                startTime=serializer.validated_data['startTime']
                endTime=serializer.validated_data['endTime']
                duration=datetime.combine(date,endTime)-datetime.combine(date,startTime)
                hours_difference = (duration).total_seconds()/3600.0
                serializer._validated_data['duration']=hours_difference
                # check sa mga conflicting bookings
                startTimeConflictCount= Booking.objects.filter(startTime__gte=startTime,startTime__lte=endTime).count()
                endTimeConflictCount=Booking.objects.filter(endTime__gte=startTime,endTime__lte=endTime).count()
                # paid using coins
                userprofile=UserProfileInfo.objects.get(user=serializer.validated_data['user'])
                facility=Facility.objects.get(facilityname=serializer.validated_data['venue'])
                if points == 0:
                    if userprofile.coin_balance < coins:
                        return Response({"error": f"Insufficient coin balance. You currently have {userprofile.coin_balance} coins."},status=status.HTTP_200_OK)
                    elif userprofile.coin_balance >= coins and coins != 0:
                        userprofile.coin_balance -= coins
                        # userprofile.save()
                elif coins == 0:
                    if userprofile.point_balance < points:
                        return Response({"error": f"Insufficient point balance. You currently have {userprofile.point_balance} points."},status=status.HTTP_200_OK)
                    elif userprofile.point_balance >= points and points != 0:
                        userprofile.point_balance -= points
                date=serializer.validated_data['date']
                
                # set status to booked
                serializer._validated_data['status']='Booked'
                #generate unique reference no.
                
                random = str(uuid.uuid4()) # Convert UUID format to a Python string.
                random = random.upper() # Make all characters uppercase.
                random = random.replace("-","") # Remove the UUID '-'.
                refNo= facility.area_id+random[0:8]
            
                while Booking.objects.filter(referenceNo=refNo).count()!=0:
                     random = str(uuid.uuid4()) # Convert UUID format to a Python string.
                     random = random.upper() # Make all characters uppercase.
                     random = random.replace("-","") # Remove the UUID '-'.
                     refNo= facility.area_id+random[0:8]
                serializer._validated_data['referenceNo']=refNo
                userprofile.save()
                serializer.save()
                response_data={
                    'message':'Succesfully booked'
                }
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    def my_random_string(string_length=8):
        """Returns a random string of length string_length."""
        random = str(uuid.uuid4()) # Convert UUID format to a Python string.
        random = random.upper() # Make all characters uppercase.
        random = random.replace("-","") # Remove the UUID '-'.
        return random[0:string_length]
    
    @api_view(['GET'])
    def getEvents(request):
        week_start = date.today()
        # week_start -= timedelta(days=week_start.weekday())
        week_end = week_start + timedelta(days=14)

        obj= CalendarEvent.objects.filter(date__gte=week_start,date__lte=week_end)
        serializer= EventsSerializer(obj,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    def getRules(request,user_type):
        if user_type==None:
            return Response({"error":"user type not found"},status=status.HTTP_200_OK)
        try:
            # Add except or finally clause here
            obj=UserType_Rules.objects.get(id=user_type)
            pass
        except:
            # Handle the exception here
            return Response({"error":"user type not found"},status=status.HTTP_200_OK)
            pass
            
        serializer= UserRulesrializer(obj)
        return Response(serializer.data,status=status.HTTP_200_OK)
# class CurrentBookings(APIView):
#     # permission_classes=[IsAuthenticated,]
#     # api to get bookings within 2 weeks ra   
    
# class BookingByVenue(APIView):
#     def get(self,request,id):
#         print(id)
#         obj=Booking.objects.filter(venue=id)
#         serializer=BookingSerializer(obj,many=True)     
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
# class Users(APIView):
#     def get(self,request):
#         users=user.objects.all()
#         serializer=UserSerializer(users,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
# class AttendeeDetail(APIView):
#     def get(self,request,id):
#         obj = Attendee.objects.filter(booking=id)
#         serializer = AttendeeSerializer(obj,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    