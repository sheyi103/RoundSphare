from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.hashers import make_password
from .models import Customer

class LoginViewTest(TestCase):

    @patch('authentication.service.AuthenticationService')  # Mock AuthenticationService
    def test_login_post_valid_credentials(self, MockAuthService):
        # Create a user and hash their password
        password = 'pppppp'
        hashed_password = make_password(password)
        # Mock Customer obect
        user = Customer.objects.create(
            id=1,
            firstName='Test',
            lastName='Mock',
            otherName='',
            email='nwokochibuokem@gmail.com',
            password=hashed_password,
            phone='09030552581',
            address='No address',
            country='My country',
            county='eCounty',
            postcode='111'
        )

        # Mock getCustomer to return the created user
        mock_auth_service = MockAuthService.return_value
        mock_auth_service.getCustomer.return_value = user

        # Simulate POST request with valid credentials
        response = self.client.post(reverse('login'), {
            'email': 'nwokochibuokem@gmail.com',
            'password': password
        })

        # Check if redirection to 'home' occurred
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, reverse('home'))

        # Check that session data was set
        self.assertEqual(self.client.session['name'], user.email)
        
        
    @patch('authentication.service.AuthenticationService')  # Mock AuthenticationService
    def test_login_post_invalid_credentials(self, MockAuthService):
        # Create a user with a password
        password = 'pppppp'
        hashed_password = make_password(password)
        # Mock Customer obect
        user = Customer.objects.create(
            id=1,
            firstName='Test',
            lastName='Mock',
            otherName='',
            email='nwokochibuokem@gmail.com',
            password=hashed_password,
            phone='09030552581',
            address='No address',
            country='My country',
            county='eCounty',
            postcode='111'
        )

        # Mock getCustomer to return the created user
        mock_auth_service = MockAuthService.return_value
        mock_auth_service.getCustomer.return_value = user

        # Simulate POST request with invalid password
        response = self.client.post(reverse('login'), {
            'email': 'nwokochibuokem@gmail.com',
            'password': 'wrongpassword'  # Incorrect password
        })
        
        # Check if the response contains the error message
        self.assertContains(response, "Invalid password")
        self.assertEqual(response.status_code, 200)  # The form should be returned with errors
    
