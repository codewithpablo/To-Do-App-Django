from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms  import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Tasks
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
   return render(request, "home.html")

@login_required
def tasks(request):
    if request.method == "GET":
        form = TaskForm()
        all_tasks = Tasks.objects.filter(usuario=request.user)
        return render(request, "tasks.html", {"form": form, "all_tasks": all_tasks})
    else: 
        try:
            form = TaskForm(request.POST)
            new_task  = form.save(commit=False)
            new_task.usuario = request.user
            new_task.save()
            all_tasks = Tasks.objects.filter(usuario=request.user)
            form = TaskForm()
            return redirect("tasks")
        except ValueError: 
            all_tasks = Tasks.objects.all()
            return render(request, "tasks.html", {"form": form, "all_tasks": all_tasks, "error": "Los datos ingresados no son validos!"})
            
def sign_up(request):
    
    #Cuando ingresamos a la pagina para poder registrarnos
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "sign-up.html", {"form": form})
    
    #Cuando hacemos click en el boton de enviar los datos
    else: 
        
        #Si las contraseñas coinciden
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                form = UserCreationForm()
                return render(request, "sign-up.html", {"form": form, "error": "Ya existe un cuenta registrada con ese nombre de usuario!"})
        else:
            form = UserCreationForm()
            return render(request, "sign-up.html", {"form": form, "error": "Las contraseñas ingresadas no coinciden!"})

def log_in(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, "log-in.html", {"form": form})
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None: 
            form = AuthenticationForm()
            return render(request, "log-in.html", {"form": form, "error": "El nombre de usuario no se encuentra registrado en nuestra base de datos!"})
        else: 
            login(request, user)
            return redirect("tasks")

@login_required
def log_out(request):
    logout(request)
    return redirect("home")

@login_required
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Tasks, pk=task_id)# Es un forma de mandar  un respuesta cliente sin que el servidor se caiga completamente
        # task  = Tasks.objects.get(id=task_id) Esto no poruqe tumba el servidor
        task.delete()
    return redirect("tasks")

@login_required
def update_task(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Tasks, pk=task_id, usuario=request.user)
        form  = TaskForm(instance=task)
        return render(request, "task-detail.html", {"form": form})
    else:
        try:
            task = get_object_or_404(Tasks, pk=task_id, usuario=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError: 
            return render(request, "task-detail.html", {"form": form, "error": "Se ha producido un error al intentar actualizar la tarea!"})

@login_required
def mark_as_complete(request, task_id):
    if request.method == "POST":
        task  = get_object_or_404(Tasks, pk=task_id, usuario=request.user)
        print(f"Antes de actualizar: completado = {task.completado}")  # Debug
        task.completado = not task.completado
        task.save()
        print(f"Después de actualizar: completado = {task.completado}")  # Debug
        return redirect("tasks")
    