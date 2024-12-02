from django.shortcuts import render, redirect
from .forms import RegistrationForm, CustomLoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages

# Registration route handler
def register(request):
    if request.method == "POST":
        print('...............1')
        form = RegistrationForm(request.POST)
    
        if form.is_valid():
            print('After validation..........')
            print(form.cleaned_data)#result {'name': 'Chibuokem Nwoko', 'email': 'nwokochibuokem@gmail.com', 'password': 'pass', 'password1': 'pass', 'address': '44B Femi Okunnu Estate Phase 1,Lekki, Lagos'}
            password = form.cleaned_data.get('password')
            hashed_password = make_password(password)
            customer = form.save(commit=False)
            customer.password = hashed_password
            customer.save()
            request.session['name'] = form.cleaned_data['email']
            return redirect('home')
        else:
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
        'county': '',
        'postcode': ''
        })
        return render(request, 'register.html', {'form': f})
    
    # Login route handler
def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        
        # verify login details
        if form.is_valid():
            print(form.cleaned_data)
            print(form.cleaned_data['username'])
            request.session['name'] = form.cleaned_data['username']
            return redirect('home')  
        else:        
            f = CustomLoginForm(initial={
            'username': form.data.get('username'),
            'password': ''
            })
            return render(request, 'login.html', {"form": f})   
        # request is get
    else:
        f = CustomLoginForm(initial={
            'username': '',
            'password': ''
            })      
        return render(request,'login.html', {'form': f})