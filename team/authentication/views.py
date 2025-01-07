from django.shortcuts import render, redirect

from authentication.service import AuthenticationService
from .forms import RegistrationForm, CustomLoginForm, EditCustomerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
from team.service import Service
from django.core.mail import EmailMessage
# from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

# Registration route handler
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
    
    # Validation form input
        if form.is_valid():
            password = form.cleaned_data.get('password')
            hashed_password = make_password(password)
            customer = form.save(commit=False)
            customer.password = hashed_password
            codeService = Service()
            nums = codeService.generate_random_alphanumeric()
            nums = nums.lower()
            customer.confirmationCode = nums
            customer.save()
            
            # Send confirmation link
            message = f'''<h2>Dear {form.cleaned_data.get('firstName')} </h2><br>Please click the link below to verify your account:<br>
            <h3><a href="http://127.0.0.1:8000/confirm/{nums}" target="_self">VERIFY</a></h3>
            <br>Thank you<br>
            <b>Team3</b>'''
            from_email = 'nwokochibuokem@gmail.com'
            recipient_list = [form.cleaned_data['email']]
            
            email = EmailMessage(
                subject='Team3 ShadeBall Registration',
                body=message,
                from_email=from_email,
                to=recipient_list
            )

            # Set the content type to 'html'
            email.content_subtype = 'html'

            # Send the email
            email.send()

            return redirect('home')
        else:
            print(form.errors)
            messages = form.errors
            return redirect('register')
    else:
        f = RegistrationForm(initial={
        'firstName': '',
        'lastName': '',
        'otherName': '',
        'email': '',
        'password': '',
        'password1': '',
        'phone': '',
        'address': '',
        'country': '',
        'postcode': ''
        })
        return render(request, 'register.html', {'form': f})

    

# Login route handler
def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        
        # verify login details
        if form.is_valid():
            print("...........")
            print(form.cleaned_data)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            f = CustomLoginForm(initial={
                    'email': email,
                    'password': ''
                })
            
            # Authenticate user
            user = AuthenticationService().getCustomer(email)
            print(user)
            if(user is None):
                return render(request, 'login.html', {"form": f, "error": "Invalid email/password"})
            if not check_password(password, user.password):
                return render(request, 'login.html', {"form": f, "error": "Invalid login credentials"})
            
            if user.status=='Inactive':
                return render(request, 'login.html', {"form": f, "error": "This account has not been activated. Verify your account via the link sent to your email."})
        
            request.session['name'] = user.email
            return redirect('home')  # Redirect to home if successful
                
        else:        
            print(form.errors)
            f = CustomLoginForm(initial={
                'email': form.data.get('email'),
                'password': ''
            })
            return render(request, 'login.html', {"form": f})   

    # If request is GET
    else:
        f = CustomLoginForm(initial={
            'email': '',
            'password': ''
        })      
        return render(request,'login.html', {'form': f})
    
def logout(request):
    del request.session['name']
    return redirect('home')


def editCustomer(request):
    name = request.session.get('name')
    print(name)
    print(request.POST) 
    service = AuthenticationService()
    customer = service.getCustomer(name)
    if(request.method == 'POST'):
        form = EditCustomerForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            service.editCustomer(cleanedData)
            request.session['name'] = form.cleaned_data['email']
            return redirect('home')
        else:
            print("Failed")
            messages = form.errors
            print(messages)
            return redirect('edit-customer')
    else:
        
        form = EditCustomerForm(initial={
            'firstName': customer.firstName,
            'lastName': customer.lastName,
            'otherName': customer.otherName if customer.otherName==None else '',
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'country': customer.country,
            'postcode': customer.postcode,
            
        })
        print(customer.country)
        return render(request, 'edit-customer.html', {'form': form})
    
    
def confirm(request, id):
    print("confirm: "+id)
    if request.method == 'GET':
        if id:
            service = AuthenticationService()
            customerExists = service.getCustomerByConfirmationCode(id)
            if customerExists:
                service.confirmCustomer(id)
                return render(request, 'confirm-message.html',{'messageTitle': 'Success', 'message': 'Email confirmation was successful'})
            else:
                return render(request, 'confirm-message.html',{'messageTitle': 'Erroe', 'message': 'Email confirmation was not successful'})
            
        else:
            return redirect('home')
                
        
# API Subscription Endpoint
def request_api_token(request):
    if request.method == 'GET':
        jwt_token = request.session.get('jwt_token', None)
        
        if jwt_token:
            return JsonResponse({"token": jwt_token}, status=200)
        else:
            return JsonResponse({"error": "User not authenticated or no token found"}, status=401)
        
# Generate JWT Token
def generate_jwt_token(user):
    # refresh = RefreshToken.for_user(user)
    return {
        'access': str('refresh.access_token'),
        'refresh': str('refresh')
    }        