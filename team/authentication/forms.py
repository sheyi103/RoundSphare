from django import forms
from .models import Customer
from django.contrib.auth.forms import AuthenticationForm

# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['name', 'email', 'password', 'address']

# Registration process
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstName', 'lastName', 'otherName', 'email', 'password', 'phone', 'address', 'country', 'county', 'postcode']
        password = forms.CharField(widget=forms.PasswordInput)
    
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
    username = forms.CharField(max_length=150, label='Email', widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

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