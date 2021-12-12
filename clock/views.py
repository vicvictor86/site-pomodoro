from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect, render

from clock.models import Config_Perfil

# Create your views here.
def index(request):
    return render(request, 'index.html')

def confirm_configurations(request, user_id):
    """Modifica as configurações do relógio de acordo com o usuário logado"""
    if request.method == "POST":     
        client = Config_Perfil.objects.get(client_id=user_id)
        client.time_pomodoro = request.POST['time_pomodoro']
        client.time_short_break = request.POST['time_short_break']
        client.time_long_break = request.POST['time_long_break']
        client.quantity_long_break = request.POST['quantity_long_break']
        client.type_sound = request.POST['type_sound']
        client.save()
    return redirect('index')

def perfil(request):
    return render(request, 'users/perfil.html')

def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if empty(name):
            return redirect('create_user')
        if empty(email):
            return redirect('create_user')
        if empty(password) or empty(password2):
            return redirect('create_user')
        if not equal_passwords(password, password2):
            return redirect('create_user')
        if User.objects.filter(email=email).exists():
            return redirect('create_user')
        if User.objects.filter(username=name).exists():
            return redirect('create_user')
            
        user = User.objects.create_user(username=name, email=email, password=password)
        client = Config_Perfil.objects.create(client_id=user.id)
        user.save()
        client.save()
        auth.login(request, user)
        return redirect('index')
        
    return render(request, 'users/create-user.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password_user']
        if empty(email) or empty(password):
            #messages.error(request, 'Os campos email e password não podem ficar em branco')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            name = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=name, password=password)
            if user is not None:
                auth.login(request, user)
                #messages.success(request, 'Login realizado com sucesso')
                return redirect('index')
            else:
                #messages.error(request, 'Usuário ou senha incorreto, por favor tente novamente')
                return redirect('login')
        #else:
            #messages.error(request, 'Usuário inexistente')
    return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def change_information(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)

        new_name = request.POST['username']
        if not information_user_equal_information_form(user.username, new_name) and User.objects.filter(username=new_name).exists():
            return redirect('perfil')
        user.username = new_name

        new_email = request.POST['email']
        if not information_user_equal_information_form(user.email, new_email) and User.objects.filter(email=new_email).exists():
            return redirect('perfil')
        user.email = new_email

        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        if not empty(new_password) and equal_passwords(new_password, confirm_new_password):
            user.set_password(new_password)
            
        user.save()
        return redirect('index')

def empty(field):
    return not field.strip()

def information_user_equal_information_form(information_user, information_form):
    return information_user == information_form

def equal_passwords(password, password2):
    return password == password2