from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render, redirect,reverse
import json
from authentication.forms import CheckoutForm
from .models import Products
import requests

# Home page
def landing_page(request):
    name = request.session.get('name', '')
    products = Products.objects.all()
    print("Listing products.........")
    print(products);
    product1 = {
        'id': products[0].id,
        'productName': products[0].productName,
        'price': products[0].price,
        'imageName': products[0].imageName,
        'imageId': products[0].imageId
    }
    product2 = {
        'id': products[1].id,
        'productName': products[1].productName,
        'price': products[1].price,
        'imageName': products[1].imageName,
        'imageId': products[1].imageId
    }
    product3 = {
        'id': products[2].id,
        'productName': products[2].productName,
        'price': products[2].price,
        'imageName': products[2].imageName,
        'imageId': products[2].imageId
    }
    product4 = {
        'id': products[3].id,
        'productName': products[3].productName,
        'price': products[3].price,
        'imageName': products[3].imageName,
        'imageId': products[3].imageId
    }
    product5 = {
        'id': products[4].id,
        'productName': products[4].productName,
        'price': products[4].price,
        'imageName': products[4].imageName,
        'imageId': products[4].imageId
    }
    product6 = {
        'id': products[5].id,
        'productName': products[5].productName,
        'price': products[5].price,
        'imageName': products[5].imageName,
        'imageId': products[5].imageId
    }
    product7 = {
        'id': products[6].id,
        'productName': products[6].productName,
        'price': products[6].price,
        'imageName': products[6].imageName,
        'imageId': products[6].imageId
    }
    product8 = {
        'id': products[7].id,
        'productName': products[7].productName,
        'price': products[7].price,
        'imageName': products[7].imageName,
        'imageId': products[7].imageId
    }
    return render(request, "index.html", {"name": name, 'product1': product1, 'product2': product2, 'product3':product3,'product4':product4, 'product5':product5,'product6':product6,'product7':product7, 'product8': product8})

# order full detail
def order_detail(request, id, productName):
    name = request.session['name']
    product = {
        'name': productName,
        'id': id
    }
    return render(request, 'order-detail.html', {'product': product, 'name':name})

def previewOrders(request):
    name = request.session.get('name', '')
    subtotal = 0
    total = 0
    if request.method == 'POST':
        try:
            itemList = json.loads(request.body.decode('utf-8'))
            
            # calculate suubtotal
            for item in itemList:
                item['total'] = float(item['price']) * float(item['quantity'])
                subtotal = subtotal + float(item['total'])
            
            # Print request
            print(itemList)    
            request.session['orders'] = itemList # Save items in session
            request.session['subtotal'] = subtotal
            total = subtotal + 10
            request.session['total'] = total
            request.session['name'] = name
            return redirect('preview-orders')
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {str(e)}")  # Print the error message to the console
            return render(request, 'index.html', {'name': name})
        
    else:
        orderItems = request.session['orders'] # Retrieve order from session
        subtotal = request.session['subtotal']
        total = request.session['total']
        request.session['name'] = name
        return render(request,'preview-order.html', {'name': name, 'orderdItems': orderItems, 'subtotal': subtotal, 'total': total})
    
    
    
def shipping(request):
    name = request.session.get('name', '')
    totals = 0;
    if(request.method == 'POST'):
        orders = json.loads(request.body.decode('utf-8'))
        print(orders)
        for item in orders:
            totals = totals + (int(float(item['price'])) * int(float(item['quantity'])))
        request.session['name'] = name
        request.session['shipping'] = orders
        request.session['total'] = totals
        return render(request, "shipping.html", {'name': name, 'total': totals})
    else:
        request.session['name'] = name
        totals = request.session['total']
        print(totals)
        return render(request,'shipping.html', {'name': name, 'total': totals})
    
    
# def checkout(request):
#     name = request.session.get('name', '')
#     print(name)
#     if(request.method == 'POST'):
#         request.session['name'] = name
#         form = CheckoutForm(request.POST)
#         if form.is_valid():
#             request.session['name'] = name
#             orders = request.session['shipping']
#             print("final order.........")
#             print(orders)
#             return render(request, "message.html") 
#         else:
#             request.session['name'] = name
#             return render(request, "shipping.html", {'name': name})
#     else:
#         print("Entered checkout..........GET")
#         request.session['name'] = name 
#         return redirect('shipping')          

def checkout(request):
    # Print session data for debugging
    print("Session contents:")
    for key, value in request.session.items():
        print(f"{key}: {value}")

    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        print(email)
        full_name = f"{first_name} {last_name}"  # Concatenate first and last name

        # Retrieve the order and total from the session
        orders = request.session.get('orders')
        if not orders or not isinstance(orders, list):
            return JsonResponse({"status": "error", "message": "No orders found in session."}, status=400)
        
        # Assuming you want to process the first order in the list
        order = orders[0]
        order_id = order.get('id')  # Order ID from session
        amount = order.get('total')  # Total amount from session

        if not order_id or not amount:
            return JsonResponse({"status": "error", "message": "Invalid order data in session."}, status=400)

        # Prepare payload for the middleware
        payload = {
            "customer_id": "cust_001",  # Replace with dynamic customer ID as needed
            "email": email,
            "name": full_name,
            "order_id": order_id,  # Use ID from session orders
            "amount": amount,  # Use total from session orders
            "success_url": "https://example.com/success",  # Replace with actual success URL
            "cancel_url": "https://example.com/cancel",  # Replace with actual cancel URL
        }

        try:
            # Call the checkout middleware
            response = requests.post(
                "http://localhost:5000/payment/checkout",  # Middleware endpoint
                json=payload,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            response_data = response.json()

            # Handle the middleware response
            if response.status_code == 200 and "data" in response_data and "checkout_url" in response_data["data"]:
                checkout_url = response_data["data"]["checkout_url"]
                print(f"Redirecting to checkout URL: {checkout_url}")
                return redirect(checkout_url)
            else:
                print(f"Error in middleware response: {response_data}")
                return JsonResponse({"status": "error", "message": "Failed to create checkout session."}, status=500)

        except Exception as e:
            print(f"Exception occurred while calling middleware: {str(e)}")
            return JsonResponse({"status": "error", "message": "An error occurred while processing your request."}, status=500)
    
    # Redirect to shipping for non-POST requests
    return redirect('shipping')
    
    
def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'pr_1MoBy5LkdIwHu7ixZhnattbh',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='YOUR_DOMAIN' + '/success.html',
            cancel_url='YOUR_DOMAIN' + '/cancel.html',
        )
    except Exception as e:
        print(e,'............')
        print(checkout_session.url)
        return redirect(checkout_session.url)

    return redirect(checkout_session.url)           