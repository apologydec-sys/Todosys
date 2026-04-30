from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm, UpdateTodoForm

# Create your views here.
def index(request):
    todos = Task.objects.all()
    count_todos = todos.count()
    
    completed_todos = Task.objects.filter(complete=True)
    count_completed_todos = completed_todos.count()
    
    count_uncompleted_todos = count_todos - count_completed_todos
    
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
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
    todo = Task.objects.get(id=pk)
    
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
    todo = Task.objects.get(id=pk)
    if request.method=="POST":
        todo.delete()
        return redirect('/')
    return render(request, 'todo/delete.html')