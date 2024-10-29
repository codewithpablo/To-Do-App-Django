from django.forms import ModelForm
from .models import Tasks
from django import forms

class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Tasks
        fields = ["titulo", "descripcion", "fecha_completado", "importante"]