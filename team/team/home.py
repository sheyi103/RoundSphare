from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect,reverse
import json

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
        print("Entered Get........")
        print(name)
        orderItems = request.session['orders'] # Retrieve order from session
        print(orderItems)
        subtotal = request.session['subtotal']
        total = request.session['total']
        print(total)
        request.session['name'] = name
        return render(request,'preview-order.html', {'name': name, 'orderdItems': orderItems, 'subtotal': subtotal, 'total': total})
    
    
    
def checkout(request):
    name = request.session['name']
    if(request.method == 'POST'):
        orders = json.loads(request.body.decode('utf-8'))
        print(orders) 
        return render(request, "shipping.html")
    else:
        return render(request,'shipping.html', {'name': name})       