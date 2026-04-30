from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['content']
        widgets = {
            'content':forms. TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a new task',
            }),
        }

class UpdateTodoForm(forms.ModelForm):  
    class Meta:
        model = Task
        fields = '__all__'  