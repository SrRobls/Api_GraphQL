from django.shortcuts import render

# Create your views here.

def formulario_usuario(request):
    return render(request, 'User/formulario.html')
