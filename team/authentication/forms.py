from django import forms
from .models import Customer
from django.contrib.auth.forms import AuthenticationForm

# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['name', 'email', 'password', 'address']

# Registration process
class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

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