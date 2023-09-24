from difflib import context_diff
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages,auth
from django.http import HttpResponse
from .models import Employee, menus,hmenus,tables,Reservation,CustomUser,AddToCart
from .forms import  YourForm
from django.contrib.auth import get_user_model


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
#     # Your view logic here
#     return render(request, 'booking_confirm.html')

def payment(request):
    return render(request,'payment.html')

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
            if user.role == CustomUser.EMPLOYEE:
                return redirect('emp_index')
            else:
                return redirect('')  # Redirect to the custom dashboard for non-admin users
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



def add_table(request):
    if request.method == 'POST':
        # Get the data from the request
        tab_id = request.POST.get('tab_id')
        desc = request.POST.get('desc')

        # Create a new record in the 'tables' model
        tables.objects.create(tab_id=tab_id, desc=desc)

        # Add a success message
        messages.success(request, 'Data added successfully!')

        # Redirect to the same page to display the success message
        return redirect('add_table')

    return render(request, 'add_table.html')

# reservation
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation
from .models import tables  # Import the 'tables' model
import uuid
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django.contrib.auth import get_user_model  # Import the get_user_model function


from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation, tables
import uuid

from django.db import transaction

def add_reservation(request):
    table_numbers = tables.objects.values_list('tab_id', flat=True)
    selected_table = None  # Initialize selected_table outside the if statement

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        reservation_date = request.POST.get('reservation_date')
        num_of_persons = request.POST.get('num_of_persons')
        table_id = request.POST.get('table_id')
        time_slot = request.POST.get('time_slot')  # Assuming you have added the time_slot field

        with transaction.atomic():
            # Use select_for_update to lock the selected table row
            selected_table = tables.objects.select_for_update().get(tab_id=table_id)

            existing_reservation = Reservation.objects.filter(
                table_id=table_id,
                reservation_date=reservation_date,
                time_slot=time_slot  # Check for the same time slot as well
            ).first()

            if existing_reservation:
                messages.error(request, 'Table already reserved for the selected date and time slot.')
            else:
                reservation = Reservation(
                    reservation_id=str(uuid.uuid4()),
                    name=name,
                    email=email,
                    phone=phone,
                    reservation_date=reservation_date,
                    num_of_persons=num_of_persons,
                    table_id=selected_table,
                    time_slot=time_slot  # Save the selected time slot
                )
                reservation.save()
                messages.success(request, 'Reservation added successfully!')
                return redirect('booking_confirm')

    user = request.user
    user_data = {
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
    }

    initial_time_slot = None
    return render(request, 'book.html', {'table_numbers': table_numbers, 'user_data': user_data, 'initial_time_slot': initial_time_slot})



def book_table(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            # Create a new Reservation object and save it to the database
            reservation = form.save()
            # Redirect to the booking confirmation page
            return redirect('booking_confirm')
    else:
        form = YourForm()  # Create a new instance of your form
    
    return render(request, 'book.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import menus, Reservation

@login_required
def booking_confirm(request, menu_id=None):
    if menu_id is not None:
        # Retrieve the menu item based on the menu_id parameter
        menu_item = get_object_or_404(menus, id=menu_id)

        # Pass the menu item to the 'booking_confirm' HTML template
        context = {'menu_item': menu_item}
    else:
        # Retrieve all bookings of the logged-in user
        bookings = Reservation.objects.filter(email=request.user.email)
        context = {'bookings': bookings}

    return render(request, 'booking_confirm.html', context)

# views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from home.models import Reservation

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

def cancel_reservation(request, reservation_id):
    booking = get_object_or_404(Reservation, reservation_id=reservation_id)
    
    if request.method == "POST" and booking.is_active:
        # Update the is_active status to False
        booking.is_active = False
        booking.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect back to the previous page
    
    return render(request, 'booking_confirm.html', {'booking': booking})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation,TimeSlot

def edit_reservation(request, reservation_id):
    booking = get_object_or_404(Reservation, reservation_id=reservation_id)
    table_numbers = tables.objects.values_list('tab_id', flat=True)

    # Fetch all available time slots from the database
    all_time_slots = TimeSlot.objects.values_list('slot_time', flat=True)
     # Set the initial_time_slot to the currently booked time slot
    initial_time_slot = booking.time_slot

    if request.method == 'POST':
        # Handle form submission for updating reservation details
        booking.name = request.POST['name']
        booking.phone = request.POST['phone']
        booking.email = request.POST['email']
        booking.num_of_persons = request.POST['num_of_persons']
        booking.table_id = tables.objects.get(tab_id=request.POST['table_id'])
        booking.reservation_date = request.POST['reservation_date']
        
        # Update the time slot by querying the TimeSlot model
        booking.time_slot = TimeSlot.objects.get(slot_time=request.POST['time_slot'])
        booking.save()

        # Redirect back to the booking confirmation page or any other desired page
        return redirect('booking_confirm')

    return render(request, 'edit_reservation.html', {'booking': booking, 'table_numbers': table_numbers, 'all_time_slots': all_time_slots, 'initial_time_slot': initial_time_slot})

def res_list(request):
    res_lists = Reservation.objects.all()  # Retrieve all menu items from the database
    return render(request,'admin_dashboard/tbl_booking_list.html',{'res_lists':res_lists})


def admin_login(request):
    return render(request,'admin_dashboard/admin_login.html')
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

def filtered_menus(request, category=None, submenu=None, sub_submenu=None):
    # Filter menus based on the selected choices
    filtered_menus = menus.objects.all()

    if category:
        filtered_menus = filtered_menus.filter(category=category)

    if submenu:
        filtered_menus = filtered_menus.filter(submenu=submenu)

    if sub_submenu:
        filtered_menus = filtered_menus.filter(sub_submenu=sub_submenu)

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
    user_count=CustomUser.objects.filter(is_admin='0').count()
    active_user_count = CustomUser.objects.filter(is_active='1', is_admin='0').count()
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

@login_required(login_url='http://127.0.0.1:8000/')
def cart(request):
    cart_items = AddToCart.objects.filter(user=request.user)
    total_price = sum(item.menu.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    for item in cart_items:
        item.product_total = item.menu.price * item.quantity

    context = {
        'cart_items':cart_items,
        'total_items':total_items,
        'total_price':total_price,
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

def update_cart_item_quantity(request, item_id):
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity', 1)  # Get the new quantity from the POST data
        try:
            cart_item = AddToCart.objects.get(id=item_id)
            cart_item.quantity = new_quantity
            cart_item.save()
            return JsonResponse({'success': True})
        except AddToCart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


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


def emp_index(request):
    emp_count=CustomUser.objects.filter(role='2').count()
    return render(request,'employee/index.html',{'emp_count':emp_count})

def emp_add(request):
    return render(request,'admin_dashboard/emp-add.html')


def emp_list(request):
    emp_lists = Employee.objects.all()  # Retrieve all menu items from the database
    return render(request,'admin_dashboard/emp-list.html',{'emp_lists':emp_lists})
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
def emp_leave(request):
    return render(request,'employee/emp_leave.html')


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
