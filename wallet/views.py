from django.db.models import Sum
from decimal import Decimal
from django.views.generic.list import ListView
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from facility.forms import UserTypeRulesForm
from facility.models import Facility_SubRules_set, Setting_Facility, Facility, Setting_UserType, UserType_Rules
from wallet.forms import UserForm, UserProfileInfoForm,CoinTransactionForm, TransactionApprovalForm, UserProfileInfoUpdateForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .decorators import superuser_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views import View
from .models import User, UserProfileInfo, Transaction,CoinTransaction,AdminPointAward
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework import status
from api.models.BookingModel import Booking
from django.core.serializers.json import DjangoJSONEncoder

import json




# added increment 2
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# added increment 3
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

#added increment 4
from walletAPI.models import VendorTransaction

def is_verified_user(user):
    return user.is_verified  # Check if the user is a verified user

def is_teacher_user(user):
    return user.is_staff  # Check if the user is a staff member (teacher)

def is_superuser(user):
    return user.is_superuser  # Check if the user is a superuser
    
# changed 12/14 3:31 am
class IndexView(View):
    def get(self, request):
        # Fetch filtered data using database queries
        facilities = Setting_Facility.objects.filter(isdeleted=0).order_by('-created_at')
        displays = Facility_SubRules_set.objects.all().order_by('-created_at')
        facility = Facility.objects.filter(isdeleted=0).order_by('-created_at')

        # Filter data using database queries
        filtered_data = []
        for sf in facilities:
            matching_display = displays.filter(facility=sf.facility.id).first()
            if matching_display:
                # Get the Facility object where facility.id matches sf.facility.id
                matching_facility = facility.filter(id=sf.facility.id).first()
                if matching_facility:
                    # Append a dictionary containing 'sf', 'dp', and 'facility_name' to filtered_data
                    filtered_data.append({
                        'sf': sf,
                        'dp': matching_display,
                        'facility_name': matching_facility.facilityname
                    })

        # Check if 'description' field exists in the model
        if hasattr(Facility_SubRules_set, 'description'):
            # Retrieve the description from the first display record if available
            first_display = displays.first()
            message = "RULES"
            messages.info(request, message)

        return render(request, 'wallet/index.html', {'filtered_data': filtered_data})


class SpecialView(View):
    @method_decorator(login_required)
    def get(self, request):
        return HttpResponse("You are logged in. Nice!")

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('wallet:index'))

class RegisterView(View):
    def get(self, request):
        registered = False
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        return render(request, 'wallet/registration.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        })

    def post(self, request):
        registered = False

        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data['email']
            first_name = profile_form.cleaned_data['first_name']
            last_name = profile_form.cleaned_data['last_name']

            if User.objects.filter(email=email).exists() or UserProfileInfo.objects.filter(first_name=first_name,last_name=last_name).exists():
                message = f"A user with the same first name, last name, or email already exists."
                messages.error(request,message)
            else:
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.is_active = True
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                registered = True

                message = f"Registration is successful! Please activate your account at the activation kiosk."
                messages.info(request, message)

                return render(request, 'wallet/registration.html', {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered,
                    'success_message': ''
                })

        else:
            message = f"Invalid Inputs"
            messages.error(request, message)
            return render(request, 'wallet/registration.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered,
            })


class UserLoginView(View):
    def get(self, request):
        return render(request, 'wallet/login.html', {})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user:
            if user.is_active and user.is_verified:
                login(request, user)
                if user.is_superuser:
                    user_profile = UserProfileInfo.objects.get(user=user)
                    firstname = user_profile.first_name
                    request.session['firstname'] = firstname
                    return redirect('wallet:index')
                else:
                    return redirect('wallet:index')
            else:
                message = f" {email} is not Verified"
                messages.warning(request, message)
                return render(request, 'wallet/login.html', {})
        else:
            message = f" Invalid login details supplied."
            messages.error(request, message)
            return render(request, 'wallet/login.html', {})
                    
            
            # print("Someone tried to login and failed.")
            # print("They used email: {} and password: {}".format(email, password))
            # Show an alert when the login details are invalid



class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        firstname = request.session.get('firstname') 
        if request.user.is_superuser:
            try:
                # Get the current user's profile
                profile = UserProfileInfo.objects.get(user_id=request.user)
                email = User.objects.get(email=request.user)
                coin_balance = profile.coin_balance
                point_balance = profile.point_balance
                

                # Get all students and rank them by the amount of points
                students_ranking = UserProfileInfo.objects.filter(user__is_superuser=False, user__is_staff=False).annotate(
                    total_points=Sum('point_balance')
                ).order_by('-total_points')

                # Query recent approved transactions
                recent_transactions = CoinTransaction.objects.filter(
                    requestee=request.user,
                    is_completed=True
                ).order_by('-date_in_receipt')[:3]  # Limit to 3 most recent transactions

            except UserProfileInfo.DoesNotExist:
                coin_balance = 0.0
                point_balance = 0.0
                students_ranking = []
                recent_transactions = []

            context = {
                'coin_balance': coin_balance,
                'point_balance': point_balance,
                'email': email,
                'firstname': firstname,
                'students_ranking': students_ranking,
                'recent_transactions': recent_transactions,
            }

            return render(request, 'wallet/dashboard.html', context)
        else:
            response_data = {'message': 'You do not have permission to access this page.'}
            return JsonResponse(response_data, status=403)
        

# def dis_base(request):
#     firstname = request.session.get('firstname') 
#     return render(request, 'base.html', {'firstname':firstname})

def create_usertype(request):
    firstname = request.session.get('firstname') 
    usertype = UserType_Rules.objects.all()
    if request.method == 'POST':
        user_typers = UserTypeRulesForm(request.POST)

        if user_typers.is_valid():
            new_usert =  user_typers.save()
            Setting_UserType.objects.create(user_type=new_usert)
            user_typers.save()
    else:
        user_typers = UserTypeRulesForm() 
    return render(request, 'user_list.html', {'firstname':firstname, 'usertype':usertype, 'user_typers':user_typers})
        
        
class UserListView(View):
    template_name = 'wallet/user_list.html'
    @method_decorator(login_required)
    def get(self, request):
        firstname = request.session.get('firstname') 
        usertype = UserType_Rules.objects.all()
        user_typers = UserTypeRulesForm()
        transactions = Transaction.objects.all().order_by('-date')

        # Fetch the users
        users = UserProfileInfo.objects.all()

        if request.method == 'POST':
            # Check if the form submitted is the account type update form
            if 'changeAccountTypeForm' in request.POST:
                user_id_to_change = request.POST.get('user_id')
                selected_user_type = request.POST.get('newAccountType')

                user = get_object_or_404(User, id=user_id_to_change)
                user_type_instance = get_object_or_404(UserType_Rules, user_type=selected_user_type)

                user.user_type = user_type_instance
                user.save()

                messages.success(request, 'Account type updated successfully.')

                # Rest of your view logic...

                return redirect('your_redirect_url')  # Redirect to the appropriate page

        # Continue with the rest of your view logic...

        context = {
            'users': users,
            'firstname': firstname,
            'usertype': usertype, 
            'user_typers': user_typers,
            'transactions': transactions,
        }

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    def post(self, request):
            recipient_id = request.POST.get('recipient')
            sender_id = request.POST.get('sender')
            raw_points = request.POST.get('points')

            try:
                # Convert the raw_points to Decimal and validate if it's non-negative
                points = float(raw_points)
                if points < 0:
                    return JsonResponse({'error': 'Points must be non-negative'})
                else:
                    recipient = get_user_model().objects.get(id=recipient_id)
                    sender = get_user_model().objects.get(id=sender_id)
                    recipient_profile = UserProfileInfo.objects.get(user_id=recipient.id)
                    sender_profile = UserProfileInfo.objects.get(user_id=sender.id)

                    recipient_profile.point_balance += points
                    recipient_profile.save()

                    transaction = Transaction.objects.create(recipient=recipient, sender=sender, points=points)

                    users = UserProfileInfo.objects.all()
                    user_data = []
                    for user in users:
                        full_name = f"{user.first_name} {user.last_name}"
                        user_data.append({
                            'email': user.user.email,
                            'id': user.profile_id,
                            'name': full_name,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'point_balance': user.point_balance,
                        })

                    return JsonResponse({'users': user_data})

            except (get_user_model().DoesNotExist, UserProfileInfo.DoesNotExist):
                return JsonResponse({'error': 'Invalid input or user does not exist'})
        

class UserTypeRulesView(View):
    template_name = 'wallet/user_list.html'  # Change 'your_app' to your actual app name

    def get(self, request):
        usertype = UserType_Rules.objects.all()
        user_typers = UserTypeRulesForm()
        
        context = {
            'usertype': usertype,
            'user_typers': user_typers,
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        usertype = UserType_Rules.objects.all()
        user_typers = UserTypeRulesForm(request.POST)

        if user_typers.is_valid() and 'submit_user_type_rules_form' in request.POST:
            new_usert = user_typers.save()
            Setting_UserType.objects.create(user_type=new_usert)
            user_typers.save()

            # Redirect to a different view or URL after form submission
            return redirect(reverse('wallet:userlist'))

        # If the form is not valid or the submit button is not pressed
        context = {
            'usertype': usertype,
            'user_typers': user_typers,
        }

        return render(request, self.template_name, context)
    
class UpdateAccountTypeView(View):
    template_name = 'wallet/user_list.html'

    @method_decorator(login_required)
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        selected_user_type = request.POST.get('newAccountType')

        # Get the UserType_Rules instance based on the selected user type
        user_type_instance = get_object_or_404(UserType_Rules, user_type=selected_user_type)

        # Assign the UserType_Rules instance to the user_type field
        user.user_type = user_type_instance
        user.save()

        # Now you can access the user_user_type_id from the UserType_Rules instance
        user_user_type_id = user_type_instance.id

        # Serialize only relevant information from the User object
        serialized_user = {
            'id': user.id,
            'email': user.email,
            # Add more fields as needed
        }

        # Assuming you need some context data for rendering the template
        context = {
            'users': [serialized_user],  # Convert to a list for serialization
            'user_type_rules': UserType_Rules.objects.all(),
            'user_user_type_id': user_user_type_id,
            # Add more context data as needed
        }

        try:
            # Try to serialize the context to JSON using Django's JSON encoder
            serialized_context = json.dumps(context, cls=DjangoJSONEncoder)
            return JsonResponse({'success': True, 'message': 'Account type updated successfully', 'data': serialized_context})
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error serializing context to JSON: {e}")
            return JsonResponse({'error': 'Failed to serialize context to JSON'})


class UserDashboardView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_verified_user))
    def get(self, request):
        try:
            profile = UserProfileInfo.objects.get(user_id=request.user)
            user=User.objects.get(email=request.user)
            first_name=profile.first_name
            email=User.objects.get(email=request.user)
            coin_balance = profile.coin_balance
            point_balance = profile.point_balance
            usertype=user.user_type_id
            email=user.email
        except UserProfileInfo.DoesNotExist:
            coin_balance = 0.0
            point_balance = 0.0

        context = {
            'coin_balance': coin_balance,
            'point_balance': point_balance,
            'first_name':first_name,
            'email':email,
            'usertype':usertype,
        }
        return render(request, 'wallet/userDashboard.html',context)
    
class PointsDashboardView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_verified_user))
    def get(self, request):
        try:
            
            profile = UserProfileInfo.objects.get(user_id=request.user)
            coin_balance = profile.coin_balance
            point_balance = profile.point_balance
            first_tname = profile.first_name
            last_name = profile.last_name
            user_profile = UserProfileInfo.objects.get(user=request.user)
            transactions = Transaction.objects.filter(recipient=user_profile.user)
            user=User.objects.get(email=request.user)
            email=user.email
            vendor_transactions = VendorTransaction.objects.filter(customer=user_profile.user, currency='Points')
            Bpoint_transactions = Booking.objects.filter(user=profile.user,points__gt=0)
        except UserProfileInfo.DoesNotExist:
            coin_balance = 0.0
            point_balance = 0.0
            transactions = []
            
        
        context = {
            'coin_balance': coin_balance,
            'point_balance': point_balance,
            'first_name':first_tname,
            'last_name':last_name,
            'transactions': transactions,
            'vendor_transactions': vendor_transactions,
            'Bpoint_transactions':Bpoint_transactions,
            'email':email,
        }


        return render(request, 'wallet/pdash.html', context)
    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++INCREMENT2++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class CoinTransactionCreateAndDashboardView(LoginRequiredMixin, View):
    model = CoinTransaction
    form_class = CoinTransactionForm
    template_name = 'wallet/cointransaction_create_and_dashboard.html'
    success_url = reverse_lazy('wallet:coin-transaction-create')
    success_message = "Transaction was successfully created."
    @method_decorator(user_passes_test(is_verified_user))

    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfileInfo.objects.get(user_id=request.user)
            user=User.objects.get(email=request.user)
            email=user.email
            point_balance = profile.point_balance
            coin_balance = profile.coin_balance
            first_tname = profile.first_name
            last_name = profile.last_name
            vendor_transactions = VendorTransaction.objects.filter(customer=profile.user, currency='Coins')
            Bcoin_transactions = Booking.objects.filter(user=profile.user,coins__gt=0)
        except UserProfileInfo.DoesNotExist:
            coin_balance = 0.0

        form = CoinTransactionForm(user=request.user)
        coin_transactions = CoinTransaction.objects.filter(requestee=request.user)

        context = {
            'form': form,
            'coin_balance': coin_balance,
            'point_balance': point_balance,
            'first_name': first_tname,
            'last_name': last_name,
            'Bcoin_transactions': Bcoin_transactions,
            'vendor_transactions': vendor_transactions,
            'coin_transactions':coin_transactions,
            'email':email,
        }

        return render(request, 'wallet/cointransaction_create_and_dashboard.html', context)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            messages.success(request, self.success_message)
            alert_message = 'Top-up request successfully sent.'
            success_data = {'success': True, 'message': alert_message}
            return JsonResponse(success_data)
        else:
            messages.error(request, "Form is not valid. Please check the fields.")
            alert_message = 'Top-up request failed.'
            error_data = {'success': False, 'message': alert_message}
            return JsonResponse(error_data)



@method_decorator(login_required, name='dispatch')
class TransactionApprovalView(View):
    template_name = 'wallet/transaction_approval.html'
    form_class = TransactionApprovalForm

    def get(self, request):
        firstname = request.session.get('firstname') 
        if request.user.is_superuser:
            transactions = CoinTransaction.objects.all()
            return render(request, self.template_name, {'transactions': transactions, 'form': self.form_class(),'firstname':firstname,})
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
        


    

class SuccessRedirectView(View):
    def get(self, request):
        return redirect('wallet/success')
    


# Custom user test function to check if the user is a superuser


@login_required
@user_passes_test(is_superuser)
def approve_transaction(request):
    if request.method == 'POST':
        reference_code = request.POST.get('reference_code')

        # Fetch the transaction by reference code and update its status and requestee's balance
        try:
            transaction = CoinTransaction.objects.get(reference_code=reference_code)
            if not transaction.is_completed:
                transaction.is_completed = True
                transaction.is_denied = False
                transaction.save()

                # Update the requestee's coin balance here
                requestee_profile = UserProfileInfo.objects.get(user=transaction.requestee)
                requestee_profile.coin_balance += transaction.amount
                requestee_profile.save()

                # Return a success response
                return JsonResponse({"status": "success", "message": "Transaction approved successfully."})

        except CoinTransaction.DoesNotExist:
            pass

    # If the transaction approval fails or it's not a POST request, return an error response
    return JsonResponse({"status": "fail", "message": "Transaction approval failed."})

@login_required
@user_passes_test(is_superuser)
def deny_transaction(request):
    if request.method == 'POST':
        reference_code = request.POST.get('reference_code')

        # Fetch the transaction by reference code and update its status
        try:
            transaction = CoinTransaction.objects.get(reference_code=reference_code)
            if not transaction.is_denied:
                transaction.is_completed = False
                transaction.is_denied = True
                transaction.save()

                # Return a success response
                return JsonResponse({"status": "success", "message": "Transaction denied successfully."})

        except CoinTransaction.DoesNotExist:
            pass

    # If the transaction denial fails or it's not a POST request, return an error response
    return JsonResponse({"status": "fail", "message": "Transaction denial failed."})


class GetTransactionDetailsView(UserPassesTestMixin, View):
    def test_func(self):
        # Check if the user is a superuser
        return self.request.user.is_superuser

    def get(self, request):
        reference_code = request.GET.get('reference_code', None)

        # Fetch the transaction details by reference code
        try:
            transaction = CoinTransaction.objects.get(reference_code=reference_code)

            # Create a dictionary with the transaction details
            transaction_data = {
                'reference_code': transaction.reference_code,
                'requestee': transaction.requestee.email,  # Assuming 'requestee' is a ForeignKey to User
                'amount': transaction.amount,
                'date_in_receipt': transaction.date_in_receipt.strftime('%Y-%m-%d %H:%M:%S'),  # Format the date as desired
                'status': 'COMPLETED' if transaction.is_completed and not transaction.is_denied else 'DENIED' if transaction.is_denied and not transaction.is_completed else 'PENDING',
                'image_receipt_url': transaction.image_receipt.url,
                'created_at':transaction.created_at,
            }

            return JsonResponse(transaction_data)
        except CoinTransaction.DoesNotExist:
            pass

        # If the transaction details retrieval fails or it's not a valid GET request, return an error response
        return JsonResponse({'status': 'fail', 'message': 'Transaction details retrieval failed.'})

# Increment 3

class SettingsView(LoginRequiredMixin, View):
    template_name = 'wallet/settings.html'
    @method_decorator(user_passes_test(is_verified_user))

    def get(self, request):
        try:
                profile = UserProfileInfo.objects.get(user_id=request.user)
                user = User.objects.get(email=request.user)
                email = user.email
                coin_balance = profile.coin_balance
                point_balance = profile.point_balance
                first_tname = profile.first_name
                last_name = profile.last_name
                profile_picture = profile.profile_picture if profile.profile_picture else 'user.png'
        except UserProfileInfo.DoesNotExist:
                # Handle the case when the user profile does not exist
                coin_balance = 0
                point_balance = 0
                first_name = ""
                last_name = ""
                profile_picture = None  # Set a default or leave it as None

        context = {
                'coin_balance': coin_balance,
                'point_balance': point_balance,
                'first_name':first_tname,
                'last_name':last_name,
                'profile_picture':profile_picture,
                'email':email,
            }
        return render(request, self.template_name, context)
    


class ChangePasswordView(PasswordChangeView):
    template_name = 'wallet/change_password.html'
    
    @method_decorator(user_passes_test(is_verified_user))
    def form_valid(self, form):
        print("okay")
        response = super(ChangePasswordView, self).form_valid(form)

        # Print form errors
        if form.errors:
            print(form.errors)

        messages.success(self.request, 'Your password has been changed successfully.')
        form.data = form.initial  # Clear the form data
        return response
    
    success_url = reverse_lazy('wallet:change-password')

#Increment 4
method_decorator(csrf_exempt)  # Use csrf_exempt for this view since you will be making an AJAX request
# class UpdateAccountTypeView(View):
#     def post(self, request, id):
#         user = get_object_or_404(get_user_model(), id=id)
#         is_superuser = request.POST.get('isSuperuser') == 'true'
#         is_staff = request.POST.get('isStaff') == 'true'
#         # user.user_type = "teacher"
#         try:
#             user.is_superuser = is_superuser
#             user.is_staff = is_staff
            
#             user.save()
#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
    
#     @method_decorator(login_required)
#     def get(self, request):
#         if request.user.is_superuser:
#             try:
#                 user_profile = UserProfileInfo.objects.get(user=request.user)
#                 transactions = Transaction.objects.all
#             except UserProfileInfo.DoesNotExist:
#                 transactions = []

#             users = UserProfileInfo.objects.all()
#             context = {
#                 'users': users,
#                 'transactions': transactions,
#             }
#             return render(request, 'wallet/user_list.html', context)
#         else:
#             return HttpResponseForbidden("You do not have permission to access this page.")





# teacher
class TeacherUserListView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_teacher_user))
    @method_decorator(user_passes_test(is_verified_user))
    def get(self, request):
        try:
            # Filter transactions by the current user as sender
            user = User.objects.get(email=request.user)
            profile = UserProfileInfo.objects.get(user_id=request.user)
            email = user.email
            coin_balance = profile.coin_balance
            point_balance = profile.point_balance
            transactions = Transaction.objects.filter(sender=request.user)
            users = UserProfileInfo.objects.filter(user__is_staff=False, user__is_superuser=False)
            userT = get_user_model().objects.all()
            teacher_profile = UserProfileInfo.objects.get(user=request.user)  # Get the teacher's profile
            points_to_give = teacher_profile.points_to_give
        except UserProfileInfo.DoesNotExist:
            transactions = []

        context = {
            'email':email,  
            'user':user,
            'coin_balance':coin_balance,
            'point_balance':point_balance,
            'users': users,
            'transactions': transactions,
            'userT': userT,
            'teacher_profile': teacher_profile,
            'points_to_give': points_to_give,
        }
        return render(request, 'wallet/teacher/teacher_user_list.html', context)

    @method_decorator(csrf_protect)
    def post(self, request):
        recipient_id = request.POST.get('recipient')
        sender_id = request.POST.get('sender')
        points = float(request.POST.get('points'))

        try:
            recipient = get_user_model().objects.get(id=recipient_id)
            sender = get_user_model().objects.get(id=sender_id)

            # Check if the recipient is a regular user (not a superuser or teacher)
            if recipient.is_staff or recipient.is_superuser:
                return JsonResponse({'success': False, 'error': 'Teacher users can only give points to regular users.'})

            recipient_profile = UserProfileInfo.objects.get(user_id=recipient.id)
            sender_profile = UserProfileInfo.objects.get(user_id=sender.id)

            # Check if the teacher has enough points_to_give
            if sender_profile.points_to_give >= points:
                sender_profile.points_to_give -= points
                sender_profile.save()

                recipient_profile.point_balance += points
                recipient_profile.save()

                transaction = Transaction.objects.create(recipient=recipient, sender=sender, points=points)

                users = UserProfileInfo.objects.all()
                user_data = []
                for user in users:
                    full_name = f"{user.first_name} {user.last_name}"
                    user_data.append({
                        'email': user.user.email,
                        'id': user.profile_id,
                        'name': full_name,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'point_balance': user.point_balance,
                    })
                return JsonResponse({'success': True, 'users': user_data})
            else:
                print('wrong')
                return JsonResponse({'success': False, 'error': 'Not enough points to award.'},status=400)

        except (get_user_model().DoesNotExist, UserProfileInfo.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'User not found.'}, status=400)





# Bonus Content



class AdminAwardPointsToTeacherView(View):
    template_name = 'wallet/admin_award_points_to_teacher.html'

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def get(self, request):
        firstname = request.session.get('firstname')
        # Retrieve a list of teacher users who have is_staff set to true
        try:
            # Filter both User and UserProfileInfo by is_staff
            teachers = User.objects.filter(is_staff=True)
            teacher_profiles = UserProfileInfo.objects.filter(user__in=teachers)
        except UserProfileInfo.DoesNotExist:
            teachers = []
            teacher_profiles = []

        context = {
            'teachers': teachers,
            'teacher_profiles': teacher_profiles,
            'firstname':firstname,
        }
        return render(request, self.template_name, context)

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def post(self, request):
        user_id = request.POST.get('teacher')
        points_awarded = float(request.POST.get('points_awarded', 0))

        try:
            teacher = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'Selected teacher not found.')
            return JsonResponse({'error': 'Selected teacher not found.'}, status=400)

        if points_awarded <= 0:
            messages.error(request, 'Points awarded must be greater than 0.')
            return JsonResponse({'error': 'Points awarded must be greater than 0.'}, status=400)

        AdminPointAward.objects.create(admin=request.user, teacher=teacher, points_awarded=points_awarded)

        teacher_profile = UserProfileInfo.objects.get(user=teacher)
        teacher_profile.points_to_give += points_awarded
        teacher_profile.save()

        messages.success(request, f'{points_awarded} points awarded to {teacher.email}.')
        
        # Return the points_awarded in the response
        return JsonResponse({'points_awarded': points_awarded, 'teacher_email': teacher.email})
    

# RFID
class ActivateAccountView(View):
    template_name = 'wallet/activation.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        rfid_value = request.POST.get('rfid_value')
        print(rfid_value)

        user = authenticate(request, email=email, password=password)
        print(user)

        if user:
            # Check if the user exists and is not active
            user_profile = UserProfileInfo.objects.get(user=user)
            print(user)
            print(user_profile)
            

            if not user.is_verified:
                # Check if the user is not verified
                if user_profile.rfid_value is None:
                    # If the RFID value is initially null, store the submitted RFID value
                    user_profile.rfid_value = rfid_value
                    user_profile.save()
                    print(user_profile.rfid_value)

                if rfid_value == user_profile.rfid_value:
                    # If the RFID value matches the stored value, activate the user's account
                    user.is_active = True
                    user.is_verified = True  # Mark the user as verified
                    user.save()
                    return HttpResponse('''
                        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                        <script>
                            document.addEventListener("DOMContentLoaded", function () {
                                Swal.fire({
                                    icon: 'success',
                                    title: 'Account Activated',
                                    text: 'Your account has been successfully activated.',
                                }).then(function() {
                                    window.location.href = "/wallet/activate_account/";
                                });
                            });
                        </script>
                    ''')
                else:
                    return HttpResponse('''
                        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                        <script>
                            document.addEventListener("DOMContentLoaded", function () {
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Invalid RFID value',
                                    text: 'The RFID value provided is invalid.',
                                }).then(function() {
                                    window.location.href = "/wallet/activate_account/";
                                });
                            });
                        </script>
                    ''')
            else:
                # return JsonResponse({'success': False, 'message': 'The account is already verified and active.'})
                return HttpResponse('''
                    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                    <script>
                        document.addEventListener("DOMContentLoaded", function () {
                            Swal.fire({
                                icon: 'error',
                                title: 'Account Already Active',
                                text: 'The account is already verified and active.',
                            }).then(function() {
                                window.location.href = "/wallet/activate_account/";
                            });
                        });
                    </script>
                ''')
                
        else:
            # return JsonResponse({'success': False, 'message': 'Invalid login details supplied or the account is already active.'})
            return HttpResponse('''
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function () {
                        Swal.fire({
                            icon: 'error',
                            title: 'Invalid Login Details',
                            text: 'Invalid login details supplied or the account is already active.',
                        }).then(function() {
                            window.location.href = "/wallet/activate_account/";
                        });
                    });
                </script>
            ''')

# Grab values
class ScanAndDisplayRFIDView(View):
    template_name = 'wallet/profile.html'
    def get(self, request):
            return render(request, self.template_name, {'user_info': None})
    def post(self, request):
        rfid_value = request.POST.get('rfid_value')
        try:
            user_profile = UserProfileInfo.objects.get(rfid_value=rfid_value)
            print(user_profile.profile_picture)
            return render(request, self.template_name, {'user_info': user_profile})
        except UserProfileInfo.DoesNotExist:
            return render(request, self.template_name, {'user_info': None, 'error_message': 'User not found for the specified RFID value.'})



class EditUserProfileView(View):
    template_name = 'wallet/edit_user_profile.html'
    @method_decorator(user_passes_test(is_verified_user))
    @method_decorator(login_required)
    def get(self, request):
        try:
            
            profile = UserProfileInfo.objects.get(user_id=request.user)
            user = User.objects.get(email=request.user)
            email = user.email
            coin_balance = profile.coin_balance
            point_balance = profile.point_balance
            first_tname = profile.first_name
            last_name = profile.last_name
            profile_picture = profile.profile_picture if profile.profile_picture else 'user.png'
            user_profile = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            # Handle the case when the user profile does not exist
            coin_balance = 0
            point_balance = 0
            first_name = ""
            last_name = ""
            profile_picture = None  # Set a default or leave it as None
        
        form = UserProfileInfoUpdateForm(instance=user_profile)

        context = {
            'coin_balance': coin_balance,
            'point_balance': point_balance,
            'first_name':first_tname,
            'last_name':last_name,
            'profile_picture':profile_picture,
            'email':email,
            'form': form,
        }
        return render(request, 'wallet/edit_user_profile.html', context)
    def post(self, request):
            user_profile = request.user.profile
            form = UserProfileInfoUpdateForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('wallet:usrdashboard')  # Redirect to the user's profile page
            return render(request, self.template_name, {'form': form, 'user_profile': user_profile})


#  ACCOUNT STATUS
class AccountStatusView(View):
    def post(self, request, user_id, *args, **kwargs):
        try:
            user = get_user_model().objects.get(id=user_id)
            
            action = request.POST.get('action')  # 'enable' or 'disable'
            if action == 'enable':
                user.is_active = True
            elif action == 'disable':
                user.is_active = False

            user.save()

            return JsonResponse({'success': True})

        except get_user_model().DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class GetUserStatusView(View):
    def get(self, request, user_id, *args, **kwargs):
        try:
            user = get_user_model().objects.get(id=user_id)
            status = "Active" if user.is_active else "Inactive"
            return JsonResponse({'status': status})

        except get_user_model().DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

