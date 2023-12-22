import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import *
# from rest_framework.views import APIView
from rest_framework import status
from api.models import Booking,Venue,Attendee
from api.serializers import BookingSerializer, VenueSerializer,BookingRequestSerializer,UserSerializer,AttendeeSerializer
from facility.models import UserType_Rules
from wallet.models import User as WalletUser,UserProfileInfo
# from rest_framework.permissions import IsAuthenticated,AllowAny
from api.jwt_util import decode_user
from datetime import datetime, date, timedelta
from rest_framework.decorators import api_view
# from django.contrib.auth.models import User
from django.http import JsonResponse
# from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
from datetime import datetime, date, timedelta
class DetailsController():
    @api_view(['GET'])
    def cancelBooking(request,id):
        # ako lng gistore ug lain variable ang id pra di libog ang query
        
        
        booking_id=id
        booking=Booking.objects.get(id=booking_id)
        print(booking.date)
        print(datetime.now().date())
        if booking.date<datetime.now().date() :
             return Response({"error":"cannot cancel past booking"},status=status.HTTP_200_OK)
        elif  (booking.date==datetime.now().date and booking.startTime<datetime.now().time()):
             return Response({"error":"cannot cancel this booking. It may be ongoing"},status=status.HTTP_200_OK)
        user=UserProfileInfo.objects.get(user=booking.user)
        # kwaon lng namo dri ang user type
        print("hello") 
        print(booking.user)
        #userDetails=WalletUser.objects.get(id=booking.user.id)
        #rules=UserType_Rules.objects.get(id=userDetails.user_type.id)
        userDetails=WalletUser.objects.get(email=booking.user)
        calculate_percent=float(0)
        rules=None
        try:
            rules=UserType_Rules.objects.get(pk=userDetails.user_type.id)
        except:
            rules=None
        if rules!=None:
            if(rules.cancel_fee==None):
                calculate_percent=30
            else:
                calculate_percent=100-rules.cancel_fee
        else:
            calculate_percent=100
        # if coins iya gamit so 0 ang points
        calculate_percent=calculate_percent/100
        print(calculate_percent)
        if booking.points==0:
            
            user.coin_balance=user.coin_balance+(booking.coins*calculate_percent)
        # if points iya gamit so 0 ang coins 
        elif booking.coins==0:
            print(calculate_percent)
            user.point_balance=user.point_balance+(booking.points*calculate_percent)
        booking.status="Cancelled"
        user.save()
        booking.save()
        serializer=BookingSerializer(booking)
        return Response(serializer.data,status=status.HTTP_200_OK)