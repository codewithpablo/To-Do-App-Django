from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tasks(models.Model):
    titulo = models.CharField(max_length=500)
    descripcion = models.TextField(max_length=10000)
    creado = models.DateTimeField(auto_now_add=True)
    fecha_completado = models.DateTimeField(null=True)
    completado  = models.BooleanField(default=False)
    importante = models.BooleanField(default=False)
    usuario  = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
    
    def __str__(self):
        return f"{self.titulo.upper()}: fue  asignada para @{self.usuario}. Se estima que sea completada para antes del {self.fecha_completado.strftime('%d/%m/%Y a las %H:%M hs')}"