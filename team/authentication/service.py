
from authentication.models import Customer


class AuthenticationService():
    
    def getCustomer(self, email):
        customer = Customer
        custInfo = customer.objects.get(email=email)
        return custInfo
    
    def editCustomer(self, cleanedData ):
        customerObj = Customer
        customer = customerObj.objects.get(email=cleanedData.get('email'))
        customer.firstName = cleanedData.get('firstName')
        customer.lastName = cleanedData.get('lastName')
        customer.otherName = cleanedData.get('otherName')
        customer.phone = cleanedData.get('phone')
        customer.save()
        return customer