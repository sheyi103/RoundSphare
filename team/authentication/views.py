from django.shortcuts import render, redirect

from authentication.service import AuthenticationService
from .forms import RegistrationForm, CustomLoginForm, EditCustomerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail

# Registration route handler
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
    
        if form.is_valid():
            password = form.cleaned_data.get('password')
            hashed_password = make_password(password)
            customer = form.save(commit=False)
            customer.password = hashed_password
            customer.save()
            request.session['name'] = form.cleaned_data['email']
            
            message = 'This is to inform you that you have succesfully registered for Team3 Shadeball.'
            from_email = 'nwokochibuokem@gmail.com'
            recipient_list = [form.cleaned_data['email']]

            # Send email
            send_mail('Team3 ShadeBall Registration', message, from_email, recipient_list)
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
            print("...........")
            print(form.cleaned_data)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = AuthenticationService().getCustomer(email)
            if not check_password(password, user.password):
                f = CustomLoginForm(initial={
                    'email': email,
                    'password': ''
                })
                return render(request, 'login.html', {"form": f, "error": "Invalid login credentials"})
        
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
            'county': customer.county,
            'postcode': customer.postcode,
            
        })
        print(customer.country)
        return render(request, 'edit-customer.html', {'form': form})
