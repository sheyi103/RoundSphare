from django.shortcuts import render, redirect
from .forms import RegistrationForm, CustomLoginForm
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

# Generate JWT Token
def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

# Registration route handler
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
    
        if form.is_valid():
            print(form.cleaned_data) # Debugging print statement
            
            # Save user after validation
            user = form.save()

            # Generate and save JWT token
            tokens = generate_jwt_token(user)
            request.session['jwt_token'] = tokens['access']
            request.session['name'] = user.email
            
            return redirect('home')
    else:
        f = RegistrationForm(initial={
            'name': '',
            'email': '',
            'password': '',
            'password1': '',
            'address': ''
        })
        return render(request, 'register.html', {'form': f})

# Login route handler
def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:  # Successful authentication
                request.session['user_id'] = user.id
                request.session['name'] = user.get_full_name()

                # Generate and save JWT token
                tokens = generate_jwt_token(user)
                request.session['jwt_token'] = tokens['access']

                return redirect('home')
            else:
                f = CustomLoginForm(initial={
                    'email': email,
                    'password': ''
                })
                return render(request, 'login.html', {"form": f, "error": "Invalid login credentials"})
        else:        
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
        return render(request, 'login.html', {'form': f})  

# API Subscription Endpoint
def request_api_token(request):
    if request.method == 'GET':
        jwt_token = request.session.get('jwt_token', None)
        
        if jwt_token:
            return JsonResponse({"token": jwt_token}, status=200)
        else:
            return JsonResponse({"error": "User not authenticated or no token found"}, status=401)
