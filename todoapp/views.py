from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Task
from .forms import TaskForm, UpdateTodoForm


def home(request):
    if request.user.is_authenticated:
        return redirect('todo-index')
    return render(request, 'todo/home.html')


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
            return redirect('todo-index')
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


@login_required
def update(request, pk):
    todo = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == 'POST':
        form = UpdateTodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo-index')
    else:
        form = UpdateTodoForm(instance=todo)

    context = {
        'form': form,
        'todo': todo,
    }
    return render(request, 'todo/update.html', context)


@login_required
def delete(request, pk):
    todo = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo-index')
    return render(request, 'todo/delete.html', {'todo': todo})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo-index')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('todo-index')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def reminders_api(request):
    """
    Returns incomplete tasks that need a reminder (6+ minutes since last reminded).
    Also updates last_reminded_at for returned tasks so the clock resets.
    """
    tasks_needing_reminder = [
        task for task in Task.objects.filter(user=request.user, complete=False)
        if task.needs_reminder()
    ]

    data = []
    for task in tasks_needing_reminder:
        data.append({
            'id': task.id,
            'content': task.content,
            'due_date': str(task.due_date) if task.due_date else None,
            'due_time': str(task.due_time) if task.due_time else None,
        })
        # Update last_reminded_at so the 6-min window resets
        task.last_reminded_at = timezone.now()
        task.save(update_fields=['last_reminded_at'])

    return JsonResponse({'reminders': data})


# ── PWA Views ────────────────────────────────────────────────────────────────

def manifest(request):
    """Serve the Web App Manifest with correct content-type."""
    content = render_to_string('pwa/manifest.json', request=request)
    return HttpResponse(content, content_type='application/manifest+json')


def service_worker(request):
    """Serve the service worker JS from root scope."""
    content = render_to_string('pwa/sw.js', request=request)
    return HttpResponse(content, content_type='application/javascript')


def offline(request):
    """Offline fallback page shown by the service worker."""
    return render(request, 'pwa/offline.html')
