from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, "home.html")

@login_required(login_url="/login")
def index(request):
    
    all_tasks=Task.objects.all()
    context={'tasks':all_tasks}
    return render(request, "index.html", context)


@login_required(login_url="/login")
def addTask(request):
    
    if request.method=="POST":
         data=request.POST
         
         task_title=data.get('task_title')
         task_description=data.get('task_description')
         task_deadline=data.get('task_deadline')
         
         print(task_title)
         print(task_description)
         print(task_deadline)
         
         
         Task.objects.create(
            task_title=task_title,
            task_description=task_description,
            task_deadline=task_deadline
         )
         
         return redirect('index')
 
    return render(request, "addTask.html")




@login_required(login_url="/login")
def deleteTask(request,id):
    delete_task=Tasks.objects.get(id=id)
    delete_task.delete()
    
    return redirect('index')
    
    

@login_required(login_url="/login")
def updateTask(request,id):
    
    print(id)
    update_task=Tasks.objects.get(id=id)
    print(update_task.task_title)
    print(update_task.task_description)
    print(update_task.task_deadline)
    
    if request.method=="POST":
        data=request.POST
        task_title=data.get('task_title')
        task_description=data.get('task_description')
        task_deadline=data.get('task_deadline')
        
        update_task.task_title=task_title
        update_task.task_description=task_description
        
        if task_deadline:
            update_task.task_deadline=task_deadline
        
        
        
        update_task.save()
        
        
        return redirect('/index/')
    
    context={'task':update_task}

    return render(request, "updateTask.html",context)



def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login')
        
        # Log the user in
        login(request, user)
        return redirect('/index')
    
    
    print(request.user.is_authenticated)
    return render(request, "login.html")
    
    
    



def register_page(request):
    
    if request.method=="POST":
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        
        user=User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, "Username already Exists")
            return redirect('/register')
        
        user=User.objects.create(
            username=username,
            email=email,
            password=password
        )
        
        user.set_password(password)
        user.save()
        
        messages.info(request, "Account Created Successfully")
        
        return redirect('/register/')
        
        
        
    return render(request, "register.html")





def logout_page(request):
    logout(request)
    return redirect('/login')
    
    






    