from django.shortcuts import render, redirect
from .forms import RegistrationForm, CustomLoginForm
from django.contrib.auth import authenticate, login

# Registration route handler
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
    
        if form.is_valid():
            print(form.cleaned_data)#result {'name': 'Chibuokem Nwoko', 'email': 'nwokochibuokem@gmail.com', 'password': 'pass', 'password1': 'pass', 'address': '44B Femi Okunnu Estate Phase 1,Lekki, Lagos'}
            # user = form.save()
            request.session['name'] = form.cleaned_data['email']
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
        
        # verify login details
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:  # If authentication is successful
                request.session['user_id'] = user.id  # Store user info in session
                request.session['name'] = user.get_full_name()  # Optional: Store full name
                return redirect('home')  # Redirect to home if successful
            else:
                # Redirect back to login with an error
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
