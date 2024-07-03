from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from ..forms import UserNewForm


class UserView(object):

    
    @login_required
    def index(request):        
        _users = User.objects.exclude(id=request.user.id).all()
        userlen = len(_users) + 1
        return render(request, 'users.html', {"users": _users, "userlen": userlen})

    @login_required
    def add(request):
        template_path = 'partial/user/user-form.html'

        if request.method == 'POST':
            form = UserNewForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, "Usuario guardado exitosamente")
                return redirect(to="users")
            else:       
                print("Formulario no es valido")     
                return render(request, template_path, {'form': form})    

        form = UserNewForm()
        return render(request, template_path, {'form': form})


