from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect,reverse
import json
from authentication.forms import CheckoutForm

# Home page
def landing_page(request):
    name = request.session['name']
    return render(request, "index.html", {"name": name})

# order full detail
def order_detail(request, id, productName):
    name = request.session['name']
    product = {
        'name': productName,
        'id': id
    }
    return render(request, 'order-detail.html', {'product': product, 'name':name})

def previewOrders(request):
    name = request.session['name']
    subtotal = 0
    total = 0
    if request.method == 'POST':
        try:
            itemList = json.loads(request.body.decode('utf-8'))
            
            # calculate suubtotal
            for item in itemList:
                item['total'] = int(item['price']) * int(item['quantity'])
                subtotal = subtotal + int(item['total'])
            
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
    name = request.session['name']
    totals = 0;
    if(request.method == 'POST'):
        orders = json.loads(request.body.decode('utf-8'))
        print(orders)
        for item in orders:
            totals = totals + (int(item['price']) * int(item['quantity']))
        request.session['name'] = name
        request.session['shipping'] = orders
        request.session['total'] = totals
        return render(request, "shipping.html", {'name': name, 'total': totals})
    else:
        request.session['name'] = name
        totals = request.session['total']
        print(totals)
        return render(request,'shipping.html', {'name': name, 'total': totals})
    
    
def checkout(request):
    name = request.session['name']
    print(name)
    if(request.method == 'POST'):
        request.session['name'] = name
        form = CheckoutForm(request.POST)
        if form.is_valid():
            request.session['name'] = name
            orders = request.session['shipping']
            print("final order.........")
            print(orders)
            return render(request, "message.html") 
        else:
            request.session['name'] = name
            return render(request, "shipping.html", {'name': name})
    else:
        print("Entered checkout..........GET")
        request.session['name'] = name 
        return redirect('shipping')              