from datetime import date
from datetime import datetime
from django.utils import timezone
from difflib import context_diff
from venv import logger
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.http import HttpResponse
from django.urls import reverse
from .models import Employee, menus,hmenus,CustomUser,AddToCart,Payment
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BillingInformation
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import razorpay
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
User=get_user_model()

def index(request):
    return render(request,'index.html')

from django.shortcuts import render
from .models import menus  # Import your "menus" model
def menu(request):
    # Fetch all menu items from the database
    all_menu_items = menus.objects.all()
    # Display the first 9 menu items
    menu_items = all_menu_items[:9]
    return render(request, 'menu.html', {'menu_items': menu_items})

def about(request):
    return render(request,'about.html')

def login_page(request):
    return render(request, 'LoginVal.html')

# def booking_confirm(request):
#     Your view logic here
#     return render(request, 'booking_confirm.html')


def menumore(request):
    Menus=menus.objects.all()
    return render(request,'menumore.html',{'Menus': Menus})




# def loginn(request):
#     if request.method=="POST":
#         email=request.POST['email']
#         password=request.POST['password']
#         user=authenticate(email=email,password=password)
#         if user is not None:
#             login(request,user)
#             return HttpResponse("Login successful") 
            
#         else:
#             messages.info(request,"Invalid login")
#             return redirect('login')
#     else:
#         return render(request, 'LoginVal.html')

# def userlogin(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email)  # Print the email for debugging
#         print(password)  # Print the password for debugging

#         if email and password:
#             user = authenticate(request, email=email, password=password)
#             print("Authenticated user:", user)  # Print the user for debugging
#             if user is not None:
#                 login(request, user)
#                 print("User authenticated:", user.email, user.role)
#                 return HttpResponse("Login successful") 
#                 return redirect('http://127.0.0.1:8000/')
#             else:
#                 error_message = "Invalid login credentials."
#                 return render(request, 'LoginVal.html', {'error_message': error_message})
#         else:
#             error_message = "Please fill out all fields."
#             return render(request, 'LoginVal.html', {'error_message': error_message})

def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)  # Print the email for debugging
        print(password)  # Print the password for debugging

        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superadmin:
                # Superuser is logged in, redirect to 'admin_index'
                return redirect('admin_index')
            elif user.role == CustomUser.EMPLOYEE:
                return redirect('emp_index')   
            else:
                return redirect('/')     
        else:
            messages.error(request, "Invalid Login")
            return redirect('login-submit')
    else:
        return render(request, 'LoginVal.html')
        
       #.............     
        # if email and password:
        #     user = authenticate(request, email=email, password=password)
        #     print("Authenticated user:", user)  # Print the user for debugging
        #     if user is not None:
        #         login(request, user)
        #         print("User authenticated:", user.email, user.role)
        #         return redirect('http://127.0.0.1:8000/')
        #     else:
        #         error_message = "Invalid login credentials."
        #         return render(request, 'LoginVal.html', {'error_message': error_message})
        # else:
        #     error_message = "Please fill out all fields."
        #     return render(request, 'LoginVal.html', {'error_message': error_message})

    # If the request method is not POST (GET request)
    #...............



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)

        if username and email and phone and password:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'RegVal.html', {'error_message': error_message})
            else:
                # Create a new user instance
                user = User(name=username, email=email, phone=phone)
                user.set_password(password)  # Set the password securely
                user.save()
                return redirect('login')  
            
    return render(request, 'RegVal.html')

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render

@csrf_protect
def login_submit(request):
    # Your login logic goes here
    # For example, validate the user's credentials and log them in

    if request.method == 'POST':
        # Handle form submission
        # Example: Check user credentials, create sessions, etc.

        # If login is successful, you can redirect the user to a different page
        return render(request, 'index.html')  # Replace 'success.html' with your success page

    # If it's a GET request, render the login page
    return render(request, 'login.html')  # Replace 'login.html' with your login page

# def reg(request):
#     if request.method=="POST":
#         fname=request.POST['fname']
#         lname=request.POST['lname']
#         username=request.POST['username']
#         email=request.POST['email']
#         password=request.POST['password']
#         confirm_password=request.POST['confirmPassword']

#         if password==confirm_password:
#             if User.objects.filter(username=username).exists():
#                 return render(request, 'RegVal.html', {'username_exits': True})
#             # elif User.objects.filter(email=email).exists():
#             #     messages.info(request,'Email already exists')
#             #     return redirect('reg')
#             else:
#                 user=User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password)
#                 user.save()
#                 messages.success(request,'Registration successful. You can now log in.')
#                 return redirect('loginn')
#         else:
#             messages.error(request,'Password confirmation does not match')
#             return redirect('reg')
#     else:
#         return render(request,'RegVal.html')
#     return render(request, 'RegVal.html')

def loggout(request):
    print('Logged Out')
    auth.logout(request)
    return redirect('/')




# def create_menu(request):
#     if request.method == 'POST':
#         form = MenuForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return redirect('/')# Redirect to a success page or perform any other action
#     else:
#         form = MenuForm()
    
#     return render(request, 'add-menu.html', {'form': form})
# def menumore(request):
#     Menus=menus.objects.all()
#     return render(request,'menumore.html',{'Menus': Menus})
def menuMore(request):
    Hmenus=hmenus.objects.all()
    return render(request,'menumore2.html',{'Hmenus': Hmenus})

# addtable
# def add_table(request):
#     if request.method == 'POST':
#         # Get the data from the request
#         tab_id = request.POST.get('tab_id')
#         desc = request.POST.get('desc')

#         # Create a new record in the 'tables' model
#         tables.objects.create(tab_id=tab_id, desc=desc)

#         # Add a success message
#         messages.success(request, 'Data added successfully!')

#         # Redirect to the same page to display the success message
#         return redirect('add_table')

#     return render(request, 'add_table.html')

# # reservation
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TableBooking
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django.contrib.auth import get_user_model  # Import the get_user_model function
from django.db.models import Q
from django.shortcuts import render, redirect
import uuid

from django.db import transaction

from django.utils import timezone
from django.http import HttpResponse

from django.utils import timezone
from django.http import HttpResponse
from django.utils.dateparse import parse_date, parse_time

# def add_reservation(request):
#     expired()
#     error_message = ""
#     user = request.user

#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#         date_str = request.POST.get("reservation_date")
#         table_name = request.POST.get("table_name")
#         start_time_str = request.POST.get("start_time")
#         end_time_str = request.POST.get("end_time")

#         # Convert date, start_time, and end_time strings to datetime.date and datetime.time objects
#         date = parse_date(date_str)
#         start_time = parse_time(start_time_str)
#         end_time = parse_time(end_time_str)

#         # Create datetime objects from date and time components
#         start_datetime = timezone.make_aware(timezone.datetime.combine(date, start_time))
#         end_datetime = timezone.make_aware(timezone.datetime.combine(date, end_time))

#         existing_booking = TableBooking.objects.filter(
#             date=date,
#             table_name=table_name,
#             start_time__lt=end_datetime,
#             end_time__gt=start_datetime,
#         ).first()

#         if existing_booking:
#             error_message = "The table is already booked. Please select another table or time or date"
#         else:
#             post = TableBooking(
#                 name=user,
#                 email=user,
#                 phone=user,
#                 date=date,
#                 start_time=start_time,
#                 end_time=end_time,
#                 table_name=table_name,
#                 status=False
#             )
#             post.save()
#             error_message = "Reservation saved successfully"

#     return render(request, "book.html", {"error_message": error_message})

from django.db import transaction  # Import transaction module
from django.shortcuts import render, redirect
from .models import TableBooking
@login_required
def add_reservation(request):
    error_message = ""
    user = request.user
    t_price = 0

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        date_str = request.POST.get("reservation_date")
        table_name = request.POST.get("table_name")
        start_time_str = request.POST.get("start_time")
        end_time_str = request.POST.get("end_time")

        date = parse_date(date_str)
        start_time = parse_time(start_time_str)
        end_time = parse_time(end_time_str)

        start_datetime = timezone.make_aware(timezone.datetime.combine(date, start_time))
        end_datetime = timezone.make_aware(timezone.datetime.combine(date, end_time))

        existing_booking = TableBooking.objects.filter(
            date=date,
            table_name=table_name,
            start_time__lt=end_datetime,
            end_time__gt=start_datetime,
        ).first()

        if existing_booking:
            error_message = "The table is already booked. Please select another table or time or date"
        else:
            selected_menu_items = request.POST.getlist("menu_items")
            selected_menu_items_info = []

            for menu_item_id in selected_menu_items:
                menu_item = menus.objects.get(id=menu_item_id)
                quantity = int(request.POST.get(f"menu_item_quantity_{menu_item.id}", 1))
                price = menu_item.price

                item_total_price = price * quantity
                t_price += item_total_price

                item_info = f"{menu_item.name} - {quantity}"
                selected_menu_items_info.append(item_info)

            selected_items = ", ".join(selected_menu_items_info)

            # Create a new TableBooking instance with t_price saved to the total_price field
            post = TableBooking(
                name=user,
                email=user,
                phone=user,
                date=date,
                start_time=start_time,
                end_time=end_time,
                table_name=table_name,
                status=False,
                selected_items=selected_items,
                total_price=t_price + 200,  # Save t_price to the total_price field
            )

            with transaction.atomic():
                post.save()  # Save the instance within a transaction

            error_message = "Reservation saved successfully"
            print("Total Price:", t_price)

            # Redirect to the booking summary page with the ID of the saved booking
            return redirect('booking_confirm', booking_id=post.id)

    menu_items = menus.objects.filter(active=True)

    return render(request, "book.html", {
        "error_message": error_message,
        "menu_items": menu_items,
    })


def expired():
    # Check for expired bookings and make slots available
    now = datetime.now()
    expired_bookings = TableBooking.objects.filter(Q(end_time__lt=now) & Q(del_status=False))
    
    for booking in expired_bookings:
        booking.del_status = True 
        booking.save()
        # Delete the expired booking
        # booking.delete()



from django.shortcuts import render, get_object_or_404
from .models import TableBooking
@login_required
def booking_confirm(request, booking_id):
    # Use get_object_or_404 to handle cases where the booking doesn't exist
    booking = get_object_or_404(TableBooking, id=booking_id)
    return render(request, 'booking_confirm.html', {'booking': booking})


from django.shortcuts import render
from .models import TableBooking  # Import your model
@login_required
def booking_list(request):
    if request.user.is_authenticated:
        # Retrieve all bookings for the logged-in user or filter as needed
        bookings = TableBooking.objects.filter(name=request.user)

    return render(request, 'booking_list.html', {'bookings': bookings})


# from django.http import JsonResponse

# def get_total_persons(request):
#     selected_date = request.GET.get('date')
#     selected_time_slot = request.GET.get('time_slot')

#     total_persons = Reservation.objects.filter(reservation_date=selected_date, time_slot=selected_time_slot).aggregate(total_persons=Sum('num_of_persons'))['total_persons'] or 0

#     return JsonResponse({'totalPersons': total_persons})


# def book_table(request):
#     if request.method == 'POST':
#         form = YourForm(request.POST)
#         if form.is_valid():
#             # Create a new Reservation object and save it to the database
#             reservation = form.save()
#             # Redirect to the booking confirmation page
#             return redirect('booking_confirm')
#     else:
#         form = YourForm()  # Create a new instance of your form
    
#     return render(request, 'book.html', {'form': form})


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404
# from .models import menus, Reservation



# # views.py
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import get_object_or_404
# from home.models import Reservation


# def cancel_reservation(request, reservation_id):
#     booking = get_object_or_404(Reservation, reservation_id=reservation_id)
    
#     if request.method == "POST" and booking.is_active:
#         # Update the is_active status to False
#         booking.is_active = False
#         booking.save()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page
    
#     return render(request, 'booking_confirm.html', {'booking': booking})



# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Reservation,TimeSlot

# from django.shortcuts import get_object_or_404, render, redirect
# from .models import Reservation, TimeSlot  # Import your models

# def edit_reservation(request, reservation_id):
#     booking = get_object_or_404(Reservation, reservation_id=reservation_id)
#     table_numbers = tables.objects.values_list('tab_id', flat=True)

#     # Fetch all available time slots from the database
#     all_time_slots = TimeSlot.objects.values_list('slot_time', flat=True)
#     # Set the initial_time_slot to the currently booked time slot
#     initial_time_slot = booking.time_slot

#     if request.method == 'POST':
#         # Handle form submission for updating reservation details
#         booking.name = request.POST['name']
#         booking.phone = request.POST['phone']
#         booking.email = request.POST['email']
#         booking.num_of_persons = request.POST['num_of_persons']
#         booking.table_id = tables.objects.get(tab_id=request.POST['table_id'])
#         booking.reservation_date = request.POST['reservation_date']

#         # Update the time slot with the selected value from the form
#         booking.time_slot = request.POST['time_slot']
#         booking.save()

#         # Redirect back to the booking confirmation page or any other desired page
#         return redirect('booking_confirm')

#     return render(request, 'edit_reservation.html', {'booking': booking, 'table_numbers': table_numbers, 'all_time_slots': all_time_slots, 'initial_time_slot': initial_time_slot})

# def res_list(request):
#     today = date.today()
#     res_lists = Reservation.objects.filter(is_active=True, reservation_date__gte=today)
#     return render(request,'admin_dashboard/tbl_booking_list.html',{'res_lists':res_lists})

# from django.shortcuts import render
# from datetime import date, timedelta
# from .models import Reservation  # Import your Reservation model
# def previous_reservations(request):
#     today = date.today()
#     one_day_ago = today - timedelta(days=1)  # Get yesterday's date
#     first_reservation = Reservation.objects.filter(reservation_date__lt=one_day_ago).order_by('reservation_date')
#     return render(request, 'admin_dashboard/previous_reservations.html', {'previous_reservations': first_reservation})

# from django.shortcuts import redirect
# from .models import Reservation
# def approve_reservation(request, reservation_id):
#     # Retrieve the reservation from the database
#     reservation = Reservation.objects.get(reservation_id=reservation_id)

#     # Update the status to 'approved'
#     reservation.status = 'approved'
#     reservation.save()
#     return redirect('res_list')  # Change 'success_page' to your actual URL name

def admin_login(request):
    return render(request,'LoginVal.html')
def admin_index(request):
    return render(request,'admin_dashboard/index.html')
def ad_MenuAdd(request):
    return render(request,'admin_dashboard/product-add.html')
def ad_MenuList(request):
    return render(request,'admin_dashboard/product-list.html')


from django.shortcuts import render, redirect
from .models import menus
from django.http import HttpResponse

def add_menu(request):
    if request.method == 'POST':
        # Get the form data from the request
        Mname = request.POST['Mname']
        Mprice = request.POST['Mprice']
        Mdesc = request.POST['Mdesc']
        Mimg = request.FILES['Mimg'] if 'Mimg' in request.FILES else None
        Mcategory = request.POST['Mcategory']
        Msubcategory = request.POST['Msubcategory']
        Msubsubcategory = request.POST['Msubsubcategory']


        # Create a new menu item
        menu_item = menus(
            name=Mname,
            desc=Mdesc,
            price=Mprice,
            img=Mimg,
            category=Mcategory,
            submenu=Msubcategory,
            sub_submenu=Msubsubcategory
        )
        
        # Save the menu item to the database
        menu_item.save()
        return redirect('menu_list')  # Redirect to a success page or any other desired page

    return render(request, 'admin_dashboard/product-add.html')

from django.shortcuts import render
from .models import menus

def products_by_category(request, category_name):
    # Filter products by the provided category name
    products = menus.objects.filter(category=category_name)

    context = {
        'category_name': category_name,
        'products': products,
    }

    return render(request, 'products_by_category.html', context)

from django.shortcuts import render
from .models import menus
from django.db.models import Q

def filtered_menus(request, category=None, submenu=None, sub_submenu=None):
    # Create a base query
    filtered_menus = menus.objects.all()

    # Build the filter condition based on selected choices
    filter_condition = Q()

    if category:
        filter_condition &= Q(category=category)

    if submenu:
        filter_condition &= Q(submenu=submenu)

    if sub_submenu:
        filter_condition &= Q(sub_submenu=sub_submenu)

    filtered_menus = filtered_menus.filter(filter_condition)

    context = {
        'filtered_menus': filtered_menus,
    }

    return render(request, 'filtered_menus.html', context)



from django.shortcuts import render
from .models import menus  # Import your Menu model

def menu_list(request):
    menu_items = menus.objects.all()  # Retrieve all menu items from the database
    return render(request, 'admin_dashboard/product-list.html', {'menu_items': menu_items})

from django.shortcuts import render
from .models import CustomUser

def user_list(request):
    user_lists = CustomUser.objects.filter(role='1')
    user_count=CustomUser.objects.filter(is_admin='0', role='1').count()
    active_user_count = CustomUser.objects.filter(is_active='1', is_admin='0',role='1').count()
    print(user_lists)
    return render(request, 'admin_dashboard/user-list.html', {'user_lists': user_lists, 'user_count': user_count,'active_user_count': active_user_count})

from django.shortcuts import render, get_object_or_404, redirect
from .models import menus
def menu_edit(request, menu_id):
    menu_items= get_object_or_404(menus, id=menu_id)
    if request.method == 'POST':
        Mname = request.POST.get('Mname')
        Mcategory = request.POST.get('Mcategory')
        Msubcategory = request.POST.get('Msubcategory')
        Msubsubcategory = request.POST.get('Msubsubcategory')
        Mdesc = request.POST.get('Mdesc')
        Mprice = request.POST.get('Mprice')
        Mimg = request.FILES.get('Mimg')

        menu_items.name= Mname
        menu_items.category=Mcategory
        menu_items.submenu=Msubcategory
        menu_items.sub_submenu=Msubsubcategory
        menu_items.desc=Mdesc
        menu_items.price=Mprice
        menu_items.img=Mimg
        
        menu_items.save()
        return redirect('menu_list')
    return render(request, 'admin_dashboard/menu_edit.html', {'menu_items': menu_items})

from django.shortcuts import render, redirect, get_object_or_404
from .models import menus

def delete_menu_item(request, menu_id):
    # Get the menu item to be deleted
    menu_item = get_object_or_404(menus, id=menu_id)

    # Set the "active" status to False
    menu_item.active = False
    menu_item.save()

    # Redirect to the menu list page or update the menu_items queryset accordingly
    return redirect('menu_list')

# views.py

from django.http import JsonResponse
from .models import menus

# def cart(request):
#     if request.method == 'POST':
#         item_name = request.POST.get('item_name')
#         item_price = request.POST.get('item_price')
        
#         # Check if the item already exists in the cart
#         existing_item = menus.objects.filter(name=item_name).first()

#         if existing_item:
#             # If item exists, update its quantity and total price
#             existing_item.quantity += 1
#             existing_item.total_price = existing_item.quantity * existing_item.price
#             existing_item.save()
#         else:
#             # If item doesn't exist, create a new cart item
#             new_item = menus(
#                 name=item_name,
#                 price=item_price,
#                 quantity=1,  # Set the initial quantity to 1
#                 total_price=item_price,  # Set the initial total price
#             )
#             new_item.save()

#         return JsonResponse({'message': 'Item added to cart successfully'})

#     return JsonResponse({'message': 'Invalid request'}, status=400)

def cart(request):
    return render(request,'cart.html')

@login_required(login_url='http://127.0.0.1:8000/')
def add_to_cart(request, menu_id):
    menu = get_object_or_404(menus, id=menu_id)
    user = request.user

    check=AddToCart.objects.filter(menu_id=menu_id,user_id=user.id).exists()
    if check:
        cart_item=AddToCart.objects.get(menu_id=menu_id,user_id=user.id)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cartItem=AddToCart(
            menu_id=menu_id,
            user_id=user.id,
            quantity=1
        )
        cartItem.save()

    return redirect('menu')

# @login_required(login_url='http://127.0.0.1:8000/')
# def cart(request):
#     # Retrieve cart items
#     cart_items = AddToCart.objects.filter(user=request.user, status=1)

#     if request.method == 'POST':
#         # Process the payment and get payment_id (you should implement this logic)
#         payment_id = process_payment(request)  # Implement this function

#         if payment_id:
#             # Update the order with payment ID and change status to "Successful."
#             for item in cart_items:
#                 item.status = 0
#                 item.save()

#             # Set the total_price to 0
#             total_price = 0
#         else:
#             # Handle the case where payment processing failed
#             total_price = sum(item.menu.price * item.quantity for item in cart_items)
#     else:
#         # Calculate the total price for the cart items
#         total_price = sum(item.menu.price * item.quantity for item in cart_items)

#     total_items = sum(item.quantity for item in cart_items)

#     max_quantity = 10
#     quantity_range = range(1, max_quantity + 1)

#     for item in cart_items:
#         item.product_total = item.menu.price * item.quantity

#     context = {
#         'cart_items': cart_items,
#         'total_items': total_items,
#         'total_price': total_price,
#         'quantity_range': quantity_range,
#     }
#     return render(request, 'cart.html', context)

@login_required(login_url='http://127.0.0.1:8000/')
def cart(request):
    cart_items = AddToCart.objects.filter(user=request.user)
    at_least_one_item_with_status_1 = any(item.status == 1 for item in cart_items)
    total_price = sum(item.menu.price * item.quantity for item in cart_items if item.status)
    total_items = sum(item.quantity for item in cart_items)

    max_quantity = 10
    quantity_range = range(1, max_quantity + 1)

    for item in cart_items:
        item.product_total = item.menu.price * item.quantity

    context = {
        'cart_items':cart_items,
        'total_items':total_items,
        'total_price':total_price,
        'quantity_range': quantity_range, 
        'at_least_one_item_with_status_1': at_least_one_item_with_status_1,
    }
    return render(request,'cart.html',context)


from django.shortcuts import redirect
from .models import AddToCart

def remove_from_cart(request, item_id):
    try:
        item = AddToCart.objects.get(id=item_id, user=request.user)
        item.delete()
    except AddToCart.DoesNotExist:
        pass  # Handle item not found as needed
    return redirect('cart')

# views.py
from django.http import JsonResponse

def update_cart_item_quantity(request, item_id, new_quantity):
    cart_item = get_object_or_404(AddToCart, id=item_id)
    cart_item.quantity = new_quantity
    cart_item.save()
    return JsonResponse({'success': True})



@login_required
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

    user = request.user
    cart_items = AddToCart.objects.filter(user=user)
    total_price = sum(item.menu.price * item.quantity for item in cart_items if item.status)

    # Get the latest BillingInformation object for the user
    try:
        billing_info = BillingInformation.objects.filter(user=user).latest('id')
    except BillingInformation.DoesNotExist:
        billing_info = None

    if request.method == 'POST':
        address = request.POST.get('address')
        town = request.POST.get('town')
        zip_code = request.POST.get('zip')

        if address is not None and address.strip() != '':
            # Create a new BillingInformation instance for each order
            billing_info = BillingInformation(user=user, address=address, town=town, zip_code=zip_code)
            billing_info.amount = total_price
            billing_info.save()

            # Clear the products in the cart and add them to billing_info.menu
            product_ids = [item.menu.id for item in cart_items]
            products_to_add = menus.objects.filter(id__in=product_ids)

            if billing_info is not None:
                billing_info.menu.set(products_to_add)  # Set the related products in billing_info.menu

            return redirect('billing_payment', billing_id=billing_info.id)  # Redirect to a success page
        else:
            error_message = "Address is required. Please provide a valid address."
            context = {
                'cart_items': cart_items,
                'total_price': total_price,
                'error_message': error_message,
                'billing_info': billing_info,
            }
            return render(request, 'delAddress.html', context)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'billing_info': billing_info,
    }

    return render(request, 'delAddress.html', context)

# def payment(request, billing_id):
#     billing = BillingInformation.objects.get(pk=billing_id)
#     user = request.user

#     # For Razorpay integration
#     currency = 'INR'
#     amount = billing.amount 
#     amount_in_paise = int(amount * 100)

#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(
#         amount=amount_in_paise,
#         currency=currency,
#         payment_capture='0'  # Capture payment manually after verifying it
#     ))

#     # Order ID of the newly created order
#     razorpay_order_id = razorpay_order['id']
#     callback_url = reverse('paymenthandler', args=[billing_id])

#     # Create a Payment record
#     payment = Payment.objects.create(
#         user=request.user,
#         razorpay_order_id=razorpay_order_id,
#         amount=billing.amount,
#         currency=currency,
#         payment_status=Payment.PaymentStatusChoices.PENDING,
#     )
#     payment.billing_info.add(billing)

#     # Prepare the context data
#     context = {
#         'user': request.user,
#         'billing': billing,
#         'razorpay_order_id': razorpay_order_id,
#         'razorpay_merchant_key': settings.RAZOR_KEY_ID,
#         'razorpay_amount': amount,
#         'currency': currency,
#         'amount': billing.amount,
#         'callback_url': callback_url,
#     }

#     return render(request, 'confirm_payment.html', context)

def billing_payment(request, billing_id):
    billing = BillingInformation.objects.get(pk=billing_id)

    currency = 'INR'
    amount = billing.amount
    amount_in_paise = int(amount * 100)

    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('billing_paymenthandler', args=[billing_id])

    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        amount=billing.amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        billing_info=billing
    )

    

    context = {
        'user': request.user,
        'billing': billing,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'amount': billing.amount,
        'callback_url': callback_url,
    }

    return render(request, 'confirm_payment.html', context)

def table_booking_payment(request, booking_id):
    booking = TableBooking.objects.get(pk=booking_id)

    currency = 'INR'
    amount = booking.total_price  # Adjust this as needed
    amount_in_paise = int(amount * 100)

    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    razorpay_order_id = razorpay_order['id']
    callback_url_booking = reverse('table_booking_paymenthandler', args=[booking_id])


    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        table_booking=booking
    )

    

    context = {
        'user': request.user,
        'booking': booking,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'amount': amount,
        'callback_url': callback_url_booking,
    }

    return render(request, 'booking_payment.html', context)

@csrf_exempt
def paymenthandler(request, booking_id=None, billing_id=None):
    print(billing_id)
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        user = request.user
        cart_items = AddToCart.objects.filter(user=user)

        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        amount = int(payment.amount * 100)
        payment.payment_id = payment_id
        payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
        payment.save()
        # Handle billing payment success, e.g., mark billing as paid

        if billing_id is not None:
            billing = BillingInformation.objects.get(id=billing_id)
            billing.status = True
            cart_items.delete()
            billing.save()
        elif booking_id is not None:
            booking = TableBooking.objects.get(id=booking_id)
            booking.status = True
        
        return redirect('/')  # Adjust the URL as needed

    return HttpResponseBadRequest()


# @csrf_exempt
# def paymenthandler(request, billing_id):
#     # Only accept POST requests.
#     if request.method == "POST":
#         # Get the required parameters from the POST request.
#         payment_id = request.POST.get('razorpay_payment_id', '')
#         razorpay_order_id = request.POST.get('razorpay_order_id', '')
#         signature = request.POST.get('razorpay_signature', '')
#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature
#         }
#         # Verify the payment signature.
#         result = razorpay_client.utility.verify_payment_signature(params_dict)
#         user = request.user
#         cart_items = AddToCart.objects.filter(user=user)
#         payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
#         amount = int(payment.amount * 100)  # Convert Decimal to paise

#         # Capture the payment.
#         razorpay_client.payment.capture(payment_id, amount)
#         payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

#         # Update the order with payment ID and change status to "Successful."
#         payment.payment_id = payment_id
#         payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
#         payment.save()

#         # Mark the cart items as inactive (status = 0)
#         cart_items.delete()

#         # Render the success page on successful capture of payment.
#         user_id = user.id
#         return redirect(reverse('order_summary', args=[user_id]))

#     else:
#         billing = BillingInformation.objects.get(id=billing_id)
#         billing.status = False
#         billing.save()
#         # If other than POST request is made.
#         return HttpResponseBadRequest()

from django.shortcuts import render
from .models import AddToCart

def display_cart_items(request):
    cart_items = AddToCart.objects.filter(user=request.user)
    total_price = sum(item.menu.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    
    return render(request, 'checkout.html', context)

from django.shortcuts import render
from .models import BillingInformation, Payment

def order_list(request):
    # Retrieve the data you need from the models
    billing_info = BillingInformation.objects.all()
    payments = Payment.objects.all()

    context = {
        'billing_info': billing_info,
        'payments': payments,
    }

    return render(request, 'admin_dashboard/orders.html', context)

from django.shortcuts import render
from .models import Payment

def payment_counts(request):
    successful_payments = Payment.objects.filter(payment_status='successful').count()
    pending_payments = Payment.objects.filter(payment_status='pending').count()
    failed_payments = Payment.objects.filter(payment_status='failed').count()

    context = {
        'successful_payments': successful_payments,
        'pending_payments': pending_payments,
        'failed_payments': failed_payments,
    }

    return render(request, 'orders.html', context)

# # cart/views.py
# from django.shortcuts import render, redirect
# from .models import AddToCart

# def add_to_cart(request, menu_id):
#     # Assuming menu_id is passed as an argument to specify the menu item to add
#     if request.method == 'POST':
#         # Get the user (you might need to implement user authentication)
#         user = request.user  # Assuming you have user authentication set up

#         # Get the menu item based on menu_id
#         menu_item = menus.objects.get(id=menu_id)

#         # Create a cart entry for the user and menu item
#         AddToCart.objects.create(user=user, menu=menu_item)

#         return redirect('cart')  # Redirect to the cart page after adding an item

def view_cart(request):
    # Retrieve cart items for the logged-in user
    user_cart_items = AddToCart.objects.filter(user=request.user)

    return render(request, 'cart.html', {'cart_items': user_cart_items})

from django.shortcuts import render
from .models import AddToCart, Payment


from django.shortcuts import render
from .models import BillingInformation, Payment

def order_summary(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Get the latest billing information for the user
    billing_info = BillingInformation.objects.filter(user=user).order_by('-id').first()

    # Get the latest payment associated with the user
    latest_payment = Payment.objects.filter(user=user).order_by('-timestamp').first()

    # Get all menu items associated with the latest billing information
    purchased_items = billing_info.menu.all() if billing_info else []

    context = {
        'user': user,
        'billing_info': billing_info,
        'latest_payment': latest_payment,
        'purchased_items': purchased_items,
    }

    return render(request, 'orderSummary.html', context)

def emp_index(request):
    emp_count=CustomUser.objects.filter(role='2').count()
    return render(request,'employee/index.html',{'emp_count':emp_count})

def emp_add(request):
    return render(request,'admin_dashboard/emp-add.html')

def emp_booking_lists(request):
        # Retrieve all bookings for the logged-in user or filter as needed
    bookings = TableBooking.objects.all() # Retrieve all booking details and related payments
    return render(request, 'employee/booking-list.html', {'bookings': bookings})

def ad_booking_lists(request):
        # Retrieve all bookings for the logged-in user or filter as needed
    bookings = TableBooking.objects.all() # Retrieve all booking details and related payments
    return render(request, 'admin_dashboard/tbl_booking_list.html', {'bookings': bookings})


def emp_list(request):
    emp_lists = Employee.objects.all()  # Retrieve all menu items from the database
    return render(request,'admin_dashboard/emp-list.html',{'emp_lists':emp_lists})

from django.shortcuts import render
from .models import LeaveApplication

def empLeave_list(request):
    leave_applications = LeaveApplication.objects.all()
    return render(request, 'admin_dashboard/empLeave_list.html', {'leave_applications': leave_applications})


def employee_count(request):
    # Count the number of employees with role=2
    emp_count = CustomUser.objects.filter(role='2').count()
    active_emp=CustomUser.objects.filter(role='2',is_active='1').count()
    print("Employee Count:", employee_count)
    print("Active Employee Count:", active_emp)
    return render(request, 'admin_dashboard/emp-list.html', {'emp_count': emp_count,'active_emp':active_emp,})

def emp_profile(request):
    emp_list= Employee.objects.all()
    user = request.user
    return render(request,'employee/emp-profile.html',{'emp_list':emp_list,'user': user})

from django.shortcuts import render, redirect
from .models import Employee,CustomUser


def save_employee_details(request):
    if request.method == "POST":
        # Get the form data from the POST request
        position = request.POST.get('position')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        id_proof_number = request.POST.get('idProof')
        education = request.POST.get('education')
        qualification = request.POST.get('qualification')
        emergency_name = request.POST.get('emergencyName')
        emergency_contact_number = request.POST.get('emergencyContact')
        image = request.FILES.get('photo')  # Get the uploaded image

        # Get the user associated with the request
        user = request.user

        # Check if an Employee record already exists for the user
        try:
            employee = Employee.objects.get(user=user)
            # If it exists, update the fields
            employee.position = position
            employee.years_of_experience = experience
            employee.address = address
            employee.id_proof_number = id_proof_number
            employee.education = education
            employee.qualification = qualification
            employee.emergency_name = emergency_name
            employee.emergency_contact_number = emergency_contact_number
            if image:
                employee.image = image  # Update the image if provided
            employee.save()
        except Employee.DoesNotExist:
            # If it doesn't exist, create a new Employee instance
            employee = Employee(
                user=user,
                position=position,
                years_of_experience=experience,
                address=address,
                id_proof_number=id_proof_number,
                education=education,
                qualification=qualification,
                emergency_name=emergency_name,
                emergency_contact_number=emergency_contact_number,
                image=image
            )
            employee.save()

        return redirect('employee_profile')  # Redirect to the desired URL after saving

    # Render the form on the page
    return render(request, 'emp_profile.html')


def emp_menu(request):
    return render(request,'employee/emp_menu.html')

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.conf import settings

def emp_registration(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        position=request.POST.get('position')
        years_of_experience=request.POST.get('years_of_experience')
    
        role=CustomUser.EMPLOYEE
        if CustomUser.objects.filter(email=email,role=CustomUser.EMPLOYEE).exists():
            return render(request,'employee/index.html')
        else:
            user=CustomUser.objects.create_user(name=name,email=email,phone=phone,password=password)
            user.role = CustomUser.EMPLOYEE
            user.save()
            empRegister = Employee(user=user,position=position,years_of_experience=years_of_experience)
            empRegister.save()

            # Send a welcome email to the newly registered employee
            subject = 'Employee Login Details'
            message = f'Registered as an employee. Your username: {email}, Password: {password}'
            from_email = settings.EMAIL_HOST_USER  # Your email address
            recipient_list = [user.email]  # Employee's email address

            send_mail(subject, message, from_email, recipient_list)

            return redirect('emp_list')
    else:
        return render(request,'employee/emp-add.html')

from django.shortcuts import render
from .models import Employee

def employee_profile(request):
    # Query all Employee model objects
    employees = Employee.objects.all()

    context = {
        'employees': employees,
    }

    return render(request, 'employee/profile.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee,CustomUser
def emp_edit(request, emp_id):
    emp_lists= get_object_or_404(Employee, id=emp_id)
    # custom_user = emp_lists.user
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        position = request.POST.get('position')
        years_of_experience = request.POST.get('years_of_experience')

        emp_lists.user.name = name
        emp_lists.user.email = email
        emp_lists.user.phone = phone
        emp_lists.user.save()

        emp_lists.position=position
        emp_lists.years_of_experience=years_of_experience
        emp_lists.save()

        return redirect('emp_list')
    
    return render(request, 'admin_dashboard/emp_edit.html', {'emp_lists': emp_lists})

def delete_emp(request, emp_id):
    # Get the menu item to be deleted
    emp = get_object_or_404(Employee, id=emp_id)

    # Set the "active" status to False
    emp.active = False
    emp.save()

    emp.user.is_active = False
    emp.user.save()

    # Redirect to the menu list page or update the menu_items queryset accordingly
    return redirect('emp_list')

def change_pswrd(request):
    return render(request,'employee/change_pswrd.html')

from django.shortcuts import render, redirect
from .models import LeaveApplication

def apply_leave(request):
    if request.method == 'POST':
        # Get the currently authenticated user
        logged_in_user = request.user

        # Get the form data from the POST request (you can use a form if needed)
        date = request.POST.get('leaveDate')
        duration = request.POST.get('leaveDuration')
        reason = request.POST.get('leaveReason')

        # Create a new LeaveApplication instance with the user's information
        leave_application = LeaveApplication(
            user=logged_in_user,
            date=date,
            duration=duration,
            reason=reason,
            status='pending'  # You can set an initial status
        )

        # Save the LeaveApplication instance
        leave_application.save()

        # Redirect or perform other actions as needed
        return redirect('apply_leave')  # Replace 'success_page' with your success page URL

    return render(request, 'employee/emp_leave.html')  # Render your leave application form template


from django.shortcuts import render
from .models import LeaveApplication

def leave_list(request):
    if request.user.is_authenticated:
        # Filter the leave applications for the currently logged-in user
        leave_applications = LeaveApplication.objects.filter(user=request.user)
    else:
        # If the user is not logged in, provide an empty queryset
        leave_applications = LeaveApplication.objects.none()
    
    return render(request, 'employee/leave_list.html', {'leave_applications': leave_applications})

from django.shortcuts import redirect, get_object_or_404
from .models import LeaveApplication

def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)
    leave.status = 'approved'
    leave.save()
    return redirect('empLeave_list')  # Redirect to the leave list page or another appropriate page


from django.shortcuts import render
from .models import BillingInformation, Payment
from datetime import date

def orderlist_emp(request):
    current_date = date.today()

    # Filter data to include only records created today
    billings_info = BillingInformation.objects.filter(payment__timestamp__date=current_date).distinct()
    payments = Payment.objects.filter(timestamp__date=current_date)


    context = {
        'billings_info': billings_info,
        'payments': payments,
    }

    return render(request, 'employee/orders-emp.html', context)


from datetime import date, timedelta
def history_orders(request):
    yesterday = date.today() - timedelta(days=1)

    # Filter data to include records up to yesterday
    billings_info = BillingInformation.objects.filter(payment__timestamp__date__lte=yesterday).distinct()
    payments = Payment.objects.filter(timestamp__date__lte=yesterday)
    
    context = {
        'billings_info': billings_info,
        'payments': payments,
    }

    return render(request, 'employee/history_orders.html', context)


from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import PredictedImage
import os
import tensorflow as tf
import numpy as np
from PIL import Image
from django.conf import settings

# Load the saved model
loaded_model = tf.keras.models.load_model("models\your_model (1).h5")

# Function to preprocess and predict an image with a threshold
def predict_food(image_path, model, threshold=0.3):
    # Load and preprocess the image
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Resize to the model's input shape
    img = img.convert("RGB")  # Convert to RGB (3 channels)

    img = np.array(img) / 255.0  # Normalize the image (assuming you trained the model with normalized data)
    img = np.expand_dims(img, axis=0)  # Add a batch dimension

    # Make predictions
    predictions = model.predict(img)
    class_idx = np.argmax(predictions)
    confidence = predictions[0][class_idx]

    # Check if confidence is above the threshold
    if confidence >= threshold:
        return class_idx, confidence
    else:
        return None, None  # No class found if confidence is below the threshold
import re



# def predict_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the uploaded image
#             instance = form.save()
#             image_path = os.path.join(settings.MEDIA_ROOT, instance.image.name)

#             # Perform prediction
#             predicted_class_idx, confidence = predict_food(image_path, loaded_model, threshold=0.5)

#             if predicted_class_idx is not None:
#                 # Assuming you have a class mapping from your training data
#                 class_names = {0: 'Beefroast', 1: 'Biryani', 2: 'Falafel', 3: 'Mandi', 4: 'Naan', 5: 'Shawarma', 6: 'burger',
#                                7: 'butter_naan', 8: 'chapati', 9: 'chicken_noodles', 10: 'chillychicken', 11: 'chole_bhature', 12: 'dal',
#                                13: 'dal_makhani', 14: 'dhokla', 15: 'dosa', 16: 'fishcurry', 17: 'fried_rice', 18: 'gobimanchurian', 19: 'idli',
#                                20: 'jalebi', 21: 'kaathi_rolls', 22: 'kadai_paneer', 23: 'kebab', 24: 'kulfi', 25: 'masala_dosa', 26: 'momos', 
#                                27: 'paani_puri', 28: 'pakode', 29: 'pav_bhaji', 30: 'pizza', 31: 'porotta', 32: 'samosa', 33: 'tea'}
#                 predicted_class_name = class_names.get(predicted_class_idx, "Unknown Class")
#                 instance.predicted_class = predicted_class_name
#                 instance.confidence = confidence
#                 instance.save()

#                 # Print the prediction result to the terminal
#                 print(f"Predicted class: {predicted_class_name}")
#                 print(f"Confidence: {confidence:.2f}")

#             return redirect('predict_image')

#     else:
#         form = ImageUploadForm()

#     return render(request, 'upload.html', {'form': form})
def clean_text(text):
    # Convert to lowercase and remove special characters
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s _]', '', text).lower()
    return cleaned_text
    
def predict_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            instance = form.save()
            image_path = os.path.join(settings.MEDIA_ROOT, instance.image.name)

            # Perform prediction
            predicted_class_idx, confidence = predict_food(image_path, loaded_model, threshold=0.5)

            if predicted_class_idx is not None:
                # Class mapping
                class_names = {
                    0: 'Beef Roast', 1: 'Biryani', 2: 'Falafel', 3: 'Mandi', 4: 'Naan',
                    5: 'Shawarma', 6: 'burger', 7: 'Butter Naan', 8: 'Chapati',
                    9: 'Chicken Noodles', 10: 'Chilly Chicken', 11: 'Chole Bhature', 12: 'dal',
                    13: 'Dal Makhani', 14: 'dhokla', 15: 'Dosa', 16: 'Fish Curry',
                    17: 'fried_rice', 18: 'Gobi Manchurian', 19: 'Idli', 20: 'jalebi',
                    21: 'Kaathi Rolls', 22: 'Kadai Paneer', 23: 'Kebab', 24: 'kulfi',
                    25: 'masala_dosa', 26: 'momos', 27: 'Paani Puri', 28: 'pakode',
                    29: 'Paav Bhaji', 30: 'pizza', 31: 'porotta', 32: 'samosa', 33: 'tea'
                }

                predicted_class_name = class_names.get(predicted_class_idx, "Unknown Class")
                cleaned_predicted_class_name = clean_text(predicted_class_name)
                instance.predicted_class = predicted_class_name
                instance.confidence = confidence
                instance.save()

                # Print the prediction result to the terminal
                print(f"Predicted class: {cleaned_predicted_class_name}")
                print(f"Confidence: {confidence:.2f}")


                # Find menus matching the cleaned class name
                matched_menus = menus.objects.filter(name__icontains=cleaned_predicted_class_name)

                if matched_menus:
                    # Display matched menus with details
                    return render(request, 'pred_menu.html', {'matched_menus': matched_menus})
                else:
                    # If no matched menus, return to pred_menu.html with a message
                    return render(request, 'pred_menu.html', {'message': 'This food is not available in our menu.'})

            # If the prediction is "Unknown Class," return to pred_menu.html with a message
            return render(request, 'pred_menu.html', {'message': 'Not available in our menu.'})

    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})

from .models import menus
def pred_menu(request):
    pred_menus = menus.objects.all()
    return render(request, 'pred_menu.html',{'pred_menus': pred_menus})
