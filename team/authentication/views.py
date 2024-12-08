from django.shortcuts import render, redirect

from authentication.service import AuthenticationService
from .forms import RegistrationForm, CustomLoginForm, EditCustomerForm
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
            'county': customer.county,
            'postcode': customer.postcode,
            
        })
        print(customer.country)
        return render(request, 'edit-customer.html', {'form': form})    