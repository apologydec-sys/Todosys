from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['content', 'due_date', 'due_time']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a new task',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'due_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
        }

class UpdateTodoForm(forms.ModelForm):  
    class Meta:
        model = Task
        fields = ['content', 'due_date', 'due_time', 'complete']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Update task',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'due_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
        }  