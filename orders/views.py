from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal

from .models import regularPizza, sicilianPizza, Toppings, Subs, Pasta, Salad, dinnerPlatters, Orders, Credits
# Create your views here.
pizzaSize = []

def index(request):
        
    context = {
        "regularPizza": regularPizza.objects.all(),
        "sicilianPizza": sicilianPizza.objects.all(),
        "toppings": Toppings.objects.all(),
        "subs": Subs.objects.all(),
        "pasta": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinnerPlatters": dinnerPlatters.objects.all(),
        "data": True
    }
    if request.user.is_authenticated:
        user = request.user.first_name+' '+request.user.last_name
        context["username"] = user

    return render(request, "menu/index.html", context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, "menu/login.html")

def register_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else: 
        return render(request, "menu/register.html")

def addUser(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    username = request.POST["username"]
    email = request.POST['email']
    password = request.POST["password"]
    data = User.objects.all()
    for d in data:
        if d.username == username:
            return render(request, 'menu/error.html', {"message":"User Already Exists!"})

    user = User.objects.create_user(first_name=fname, last_name=lname, username=username, email=email, password=password)
    Credits.objects.create(user=user, credit=0.00)
    context = {
        "message": "Successfully created account!"
    }
    return render(request, 'menu/login.html', context)

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, "menu/success.html", {"username": user.first_name+' '+user.last_name, "credit": Credits.objects.get(user=user)})
    else:
        return render(request, "menu/error.html", {"message": "Invalid Credentials!"})
    

def logout_view(request):
    logout(request)
    return render(request, "menu/login.html", {"message": "Logged out."})

def order(request, step_name):
    if request.user.is_authenticated:
        name = request.user.first_name+' '+request.user.last_name
        if step_name == 'step1':
            return render(request, "menu/order.html", {"data": "step1", "username": name})
        elif step_name.find('step2') == 0:
            category = step_name.split('-')[1]
            context = {
                "data": "step2", 
                "username": name,
                "category": category
            }
            if category == 'regularPizza':
                context["options"] = regularPizza.objects.all()
            elif category == 'sicilianPizza':
                context["options"] = sicilianPizza.objects.all()
            elif category == 'Subs':
                context["options"] = Subs.objects.all()
            elif category == 'Pasta':
                context["options"] = Pasta.objects.all()
            elif category == 'dinnerPlatters':
                context["options"] = dinnerPlatters.objects.all()
            elif category == 'Salads':
                context["options"] = Salad.objects.all()
              
            return render(request, "menu/order.html", context)
        elif step_name.find('step3') == 0:
            selection = step_name.split('-')[1]
            sel = selection.split()[1]
            if sel == 'Item' or sel == 'Items':
                category = 'sicilianPizza'
            else:
                category = 'regularPizza'
            context = {
                "data": "step3",
                 "username": name,
                 "toppings": Toppings.objects.all(), 
                 "category": category, 
                 "selection": selection
                 }
            if selection.split()[0] == '1':
                context['top'] = 1
            elif selection.split()[0] == '2':
                context['top'] = 2
            elif selection.split()[0] == '3':
                context['top'] = 3
            elif selection.split()[0] == 'Special':
                context['top'] = 5
            return render(request, "menu/order.html", context)
        else:
            return render(request, "menu/error.html", {"message": "Requested Url Not Found!", "username": name})
    else:
        render(request, "menu/error.html", {"message": "Please Log In First!"})

def disOpt(request):
    if request.user.is_authenticated:
        name = request.user.first_name+' '+request.user.last_name
        category = request.POST['category']
        step_name = 'step2-'+category
        return redirect('order', step_name=step_name)
    else:
       render(request, "menu/error.html", {"message": "Please Log In First!"}) 

def completeOrder(request):
    if request.user.is_authenticated:
        category = request.POST['category']
        selection = request.POST['menuOpt']
        size = request.POST['size']
        if category == 'regularPizza' or category == 'sicilianPizza':
            if category == 'regularPizza':
                dt = regularPizza.objects.get(pk=1)
            elif category == 'sicilianPizza':
                dt = sicilianPizza.objects.get(pk=1)
            if selection == 'Cheese':
                if size == 'small':
                    Orders.objects.create(email=request.user.email, category=category, selection=selection, topping='Cheese', progress="Payment Pending!", size=size, cost=dt.small)
                    return redirect('track')
                elif size == 'large':
                    Orders.objects.create(email=request.user.email, category=category, selection=selection, topping='Cheese', progress="Payment Pending!", size=size, cost=dt.large)
                    return redirect('track')
            else: 
                if selection == 'Special' and category == 'regularPizza':
                    selection = 'Special Topping'
                elif selection == 'Special' and category == 'sicilianPizza':
                    selection = 'Special Item'
                else:
                    pass
                pizzaSize.append(size)
                return redirect('order', step_name='step3-'+selection)
        else:
            if category == 'Subs':
                dt = Subs.objects.all()
            elif category == 'Pasta':
                dt = Pasta.objects.all()
            elif category == 'dinnerPlatters':
                dt = dinnerPlatters.objects.all()
            elif category == 'Salads':
                dt = Salad.objects.all()
            
            for data in dt:
                if selection == data.items:
                    if size == 'small':
                        cost = data.small
                    elif size  == 'large':
                        cost = data.large
                    elif size == 'medium':
                        cost = data.rate

            Orders.objects.create(email=request.user.email, category=category, selection=selection, topping='', progress="Payment Pending!", size=size, cost=cost)
            return redirect('track')
    else:
        render(request, "menu/error.html", {"message": "Please Log In First!"})

def placePizzaOrder(request):
    if request.user.is_authenticated:
        email = request.user.email
        sel = request.POST['selection']
        if sel.find('Special') == 0:
            sel = 'Special'
        else:
            pass
        category = request.POST['category']
        topp = int(request.POST['topp'])
        tp = ''

        if topp == 1:
            t1 = request.POST['menuOpt']
            tp = t1
            
        elif topp == 2:
            t1 = request.POST['menuOpt']
            t2 = request.POST['menuOpt2']
            tp = t1+' '+t2
            
        elif topp == 3:
            t1 = request.POST['menuOpt']
            t2 = request.POST['menuOpt2']
            t3 = request.POST['menuOpt3']
            tp = t1+' '+t2+' '+t3
            
        elif topp == 5:
            t1 = request.POST['menuOpt']
            t2 = request.POST['menuOpt2']
            t3 = request.POST['menuOpt3']
            t4 = request.POST['menuOpt4']
            t5 = request.POST['menuOpt5']
            tp = t1+' '+t2+' '+t3+' '+t4+' '+t5
            
            print(tp)

        if category == 'regularPizza':
            dt = regularPizza.objects.get(items=sel)
        elif category == 'sicilianPizza':
            dt = sicilianPizza.objects.get(items=sel)
        
        size = pizzaSize[0]
        pizzaSize.clear()
        if size == 'small':
            cost = dt.small
        elif size == 'large':
            cost = dt.large

        Orders.objects.create(email=email, category=category, selection=sel, topping=tp, progress="Payment Pending!", size=size, cost=cost)
        o = []
        name = request.user.first_name+' '+request.user.last_name
        orders = Orders.objects.all()
        mail = request.user.email
        for order in orders:
            if order.email == mail:
                if order.progress == "Payment Pending!":
                    o.append(order)
        context = {
            "orders": o,
            "mail": mail,
            "username": name 
        }
        cost = 0
        for order in orders:
            if order.email == mail:
                if order.progress == "Payment Pending!":
                    cost = cost+order.cost

        context['totalCost'] = cost
        return render(request, "menu/track.html", context)
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})

def track(request):
    if request.user.is_authenticated:
        o = []
        name = request.user.first_name+' '+request.user.last_name
        orders = Orders.objects.all()
        mail = request.user.email
        for order in orders:
            if order.email == mail:
                if order.progress == "Payment Pending!":
                    o.append(order)
        context = {
            "orders": o,
            "mail": mail,
            "username": name 
        }
        cost = 0
        for order in o:
            if order.email == mail:
                cost = cost+order.cost

        context['totalCost'] = cost
        return render(request, "menu/track.html", context)
    else:
        render(request, "menu/error.html", {"message": "Please Log In First!"})

def delOrder(request):
    if request.user.is_authenticated:
        orderId = request.POST['orderId']
        order = Orders.objects.get(pk=orderId)
        order.delete()
        return redirect('track')
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})

def addCredit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            name = request.user.first_name+' '+request.user.last_name
            context = {
                "username": name, 
                "users": User.objects.all(),
                "credits": Credits.objects.all()
            }
            return render(request, "menu/addBalance.html", context)
        else:
            return render(request, "menu/error.html", {"message": "Forbidden!"})
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})

def updateCredit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            name = request.user.first_name+' '+request.user.last_name
            mail = request.POST['mail']
            credit = Decimal(request.POST['cost'])
            user = User.objects.get(email=mail)
            c = Credits.objects.get(user=user)
            c.credit += credit
            c.save()
            context = {
                "username": name, 
                "users": User.objects.all(),
                "credits": Credits.objects.all(), 
                "message": "Updated Successfully"
            }
            return render(request, "menu/addBalance.html", context)
        else:
            return render(request, "menu/error.html", {"message": "Forbidden!"})
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})

def checkOut(request):
    if request.user.is_authenticated:
        name = request.user.first_name+' '+request.user.last_name
        totalCost = Decimal(request.POST['totalCost'])
        mail = request.user.email
        c = Credits.objects.get(user=request.user)
        balance = c.credit
        if balance > totalCost:
            c.credit = balance-totalCost
            c.save()
            orders = Orders.objects.all()
            for order in orders:
                if order.email == mail:
                    if order.progress == "Delivered":
                        pass
                    else:
                        order.progress = "Payment Recieved!"
                        order.save()
            context = {
                "username": name, 
                "orders": Orders.objects.all(),
                "mail": mail
            }
            return render(request, "menu/progress.html", context)
        else:
            return render(request, "menu/error.html", {"message": "Not enough balance!", "username": name})
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})

def trackFood(request):
    if request.user.is_authenticated:
        name = request.user.first_name+' '+request.user.last_name
        mail = request.user.email
        context = {
                "username": name, 
                "orders": Orders.objects.all(),
                "mail": mail
            }
        return render(request, "menu/progress.html", context) 
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})

def returnBalance(request):
    if request.user.is_authenticated:
        b = Credits.objects.get(user=request.user)
        name = request.user.first_name+' '+request.user.last_name
        context = {
            "username": name,
            "balance": b.credit
        }
        return render(request, "menu/balance.html", context)
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})
    
def showStatus(request):
    if request.user.is_authenticated:
        name = request.user.first_name+' '+request.user.last_name
        context = {
            "username": name,
            "orders": Orders.objects.all()
        }
        return render(request, "menu/status.html", context)
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})

def updateStatus(request):
    if request.user.is_authenticated:
        name = request.user.first_name+' '+request.user.last_name
        status = request.POST['updStat']
        oid = request.POST['orderNumber']
        if status == 'success':
            order = Orders.objects.get(pk=oid)
            order.progress = 'Delivered'
            order.save()
            return redirect('showStatus')
    else:
        return render(request, "menu/error.html", {"message": "Please Log In First!"})