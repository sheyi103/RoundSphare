from django import forms
from .models import Customer
from django.contrib.auth.forms import AuthenticationForm
from .service import AuthenticationService

# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['name', 'email', 'password', 'address']

# Registration process
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  
    password1 = forms.CharField(widget=forms.PasswordInput)  
     
    class Meta:
        model = Customer
        fields = ['firstName', 'lastName', 'otherName', 'email', 'password', 'phone', 'address', 'country', 'county', 'postcode']
        
         
    #Check if email exists    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('A customer with this email already exists.')
        return email

    #Check if phone number exists
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError('A customer with this phone number already exists.')
        return phone
        
    #Check if password and confirm passwords are same    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')

        # Validate that passwords match
        if password and password1:
            if password != password1:
                raise forms.ValidationError("Passwords do not match.")
        
        print(cleaned_data)
        print("++++++++++++++")
        return cleaned_data
    
    
    # Login form processor
class CustomLoginForm(forms.Form):
    email = forms.CharField(max_length=150, label='Email', widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
    
class CheckoutForm(forms.Form):
    firstName = forms.CharField(required=True)
    lastName = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(required=True)
    country = forms.ChoiceField(required=True,choices=[
            ('United States', 'United States'), 
            ('United Kingdom', 'United Kingdom')
        ])
    postcode = forms.CharField(required=True)
    county = forms.CharField()  
    card = forms.CharField(required=True)
    cvv = forms.CharField(required=True)
    expiry = forms.CharField(required=True)  
    

#Edit Customer info
class EditCustomerForm(forms.Form):
    firstName = forms.CharField(max_length=100)
    lastName = forms.CharField(max_length=100)
    otherName = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    country = forms.CharField(max_length=100)
    county = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=20)
    
    #Clean email  
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
        return email

    #Cleaan phone
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        print('Phone', phone)
        if not phone:
            raise forms.ValidationError('A customer with this phone number already exists.')
        return phone
    
        
    #Clean address 
    def clean_address(self):
        address = self.cleaned_data.get('address')

        # Validate address
        if not address:
            raise forms.ValidationError("Address can not be empty.")
        return address
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        return cleaned_data
      