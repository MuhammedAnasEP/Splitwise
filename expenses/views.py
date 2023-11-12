from django.shortcuts import render, redirect
from .models import Expense, User
from django.contrib import messages
from django.contrib.auth.models import auth
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect(show_balances)
    
    return redirect(signin)


def signup(request):
    if request.user.is_authenticated:
        return redirect(show_balances)
        
    if request.method == "POST":

        mobile = request.POST['mobile']

        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        
        if password == confirm_password:
            if User.objects.filter(username = name).exists():
                messages.info(request,"name already exisst!")
                return redirect(signup)

            if User.objects.filter(email = email).exists():
                messages.info(request,"Email already exists!")
                return redirect(signup)

            user = User.objects.create_user(username = name, name=name, mobile=mobile, email = email, password = password)
            user.save()
            user = auth.authenticate(username=name, password=password)
        
            if user is not None:
                auth.login(request, user)
                return redirect(home)
            return redirect(home)            
    
        messages.info(request, "Password is not matching!")

    return render(request, "signup.html")

def signin(request):
    if request.user.is_authenticated:
        return redirect(show_balances)
        
    if request.method == "POST":
        user_name = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=user_name, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect(home)
        else:
            messages.info(request, "Invalid Credentials!")
            return redirect(signin)
    else:
        return render(request, "signin.html")

def signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect(home)

def add_expense(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST['paid_by']
            title = request.POST['title']
            amount = request.POST['amount']
            split_type = request.POST['split_type']

            try:
                paid_by = User.objects.get(name=name)
            except:
                messages.info(request, f"The user {name} not registered in this app ask him to join.")
                return redirect(add_expense)

            expense = Expense.objects.create(title=title, amount=amount, paid_by=paid_by, split_type=split_type )


            participants_data = []

            participants = request.POST['participants']

            participants_list = participants.split(',')

            for participant in participants_list:
                participant = participant.lstrip()
                participant = participant.rstrip()
                try:
                    participant_user = User.objects.get(name = participant)
                    expense.participants.add(participant_user)
                    participants_data.append(participant_user)
                except:
                    messages.info(request, f"The participant {participant} not registered in this app ask him to join.")
                    return redirect(add_expense)

            calculate_balances(expense)         

    
        
            for participant in participants_data:
                subject = 'Expense Shared'
                message = f'You have been added to an expense. You owe {participant.balance:.2f} ₹.'
                recipient = participant.email
                send_mail(subject, 
                    message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
                messages.info(request, 'Expense added and shared mail to all participents.')

            return redirect(show_balances)           

        return render(request, 'add_expense.html')
    return redirect(signin)

def show_balances(request):
    if request.user.is_authenticated:
        user = request.user

        user = User.objects.get(id=user.id)

        context = {
            "name":user.name,
            "total_expense":user.balance
        }
        

        return render(request, 'balance.html', context)
    return redirect(signin)


def calculate_balances(expense):

    split_amount = float(expense.amount) / expense.participants.count()
    for participant in expense.participants.all():
        if participant != expense.paid_by:
            balance = float(participant.balance)+split_amount
            participant.balance = balance
            participant.save()      
