from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, UpdateTodoForm

# Create your views here.
@login_required
def index(request):
    todos = Task.objects.filter(user=request.user)
    count_todos = todos.count()
    
    completed_todos = todos.filter(complete=True)
    count_completed_todos = completed_todos.count()
    
    count_uncompleted_todos = count_todos - count_completed_todos
    
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
    
    context = {
        'todos': todos,
        'form': form,
        'count_todos': count_todos,
        'count_completed_todos': count_completed_todos,
        'count_uncompleted_todos': count_uncompleted_todos, 
    }
    return render(request, 'todo/index.html', context)



def update(request, pk):
    todo = Task.objects.get(id=pk, user=request.user)
    
    if request.method == 'POST':
        form = UpdateTodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    else:
        form = UpdateTodoForm(instance=todo)
    
    
    context = { 
        'form': form
    }
    return render(request, 'todo/update.html', context)




def delete(request, pk):
    todo = Task.objects.get(id=pk, user=request.user)
    if request.method=="POST":
        todo.delete()
        return redirect('/')
    return render(request, 'todo/delete.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')