from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
tasks = []



def index(request):
    temp_tasks = request.session.get('temp_tasks', [])

    if request.method == 'POST':
        task_name = request.POST.get('taskInput')
        task_status = request.POST.get('taskStatus', 'Pending')
        new_task = {'name': task_name, 'status': task_status}
        temp_tasks.append(new_task)  # Default to 'Pending'
        request.session['temp_tasks'] = temp_tasks
        return redirect('home')  # Adjust the redirect as needed

    return render(request, 'index.html', {'tasks': temp_tasks, 'user_authenticated': False})

@csrf_exempt
def update_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')
        task = Task.objects.get(id=task_id)
        task.status = status
        task.save()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        task = Task.objects.get(id=task_id)
        task.delete()
        return JsonResponse({'status': 'success'})

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Change this to match the name in your form
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('todo_list')  # Redirect to a success page.
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # Check if passwords match
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Check if email is already taken
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already taken.")
            return render(request, 'signup.html')

        # Create new user
        user = User.objects.create_user(username=email, password=password)
        user.first_name = full_name
        user.save()
        
        messages.success(request, "Registration successful. You can log in now.")
        return redirect('login')  # Redirect to login page

    return render(request, 'signup.html')

@login_required
def todo_list(request):
    if request.method == 'POST':
        task_input = request.POST.get('taskInput')
        task_status = request.POST.get('taskStatus')
        task = Task.objects.create(user=request.user, name=task_input, status=task_status)
        messages.success(request, 'Task added successfully!')
    
    tasks = Task.objects.filter(user=request.user)  # Fetch tasks related to the logged-in user
    return render(request, 'todo_list.html', {'tasks': tasks})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()
        return redirect('todo_list')  # Redirect to your task list or home page

    return render(request, 'update_task.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('todo_list')  # Redirect to your task list or home page

    return render(request, 'delete_task.html', {'task': task})




def logout_view(request):
    logout(request)
    return redirect('login')


@login_required  # Ensure user is logged in
def task_list(request):
    if request.method == 'POST':
        task_name = request.POST.get('taskInput')
        task_status = request.POST.get('taskStatus')
        Task.objects.create(name=task_name, status=task_status, user=request.user)  # Associate with logged-in user
        return redirect('task_list')  # Redirect to the task list after adding

    tasks = Task.objects.filter(user=request.user)  # Get tasks for the logged-in user
    return render(request, 'todo_list.html', {'tasks': tasks})