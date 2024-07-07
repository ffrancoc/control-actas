
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import UserNewForm, UserUpdateForm, PasswordChangeForm


class UserView(object):

    
    @login_required
    def index(request):        
        _users = User.objects.exclude(id=request.user.id).all()
        userlen = len(_users) + 1

        print([Group.objects.filter(user=request.user).all()])

        return render(request, 'users.html', {"users": _users, "userlen": userlen})
    
    @login_required
    def group(request, pk):
        _group = get_object_or_404(Group, pk=pk)
        if not _group:
            return redirect('users')
        
        data = serializers.serialize('json', [_group])        
        return HttpResponse(data, content_type="application/json")
    
    @login_required
    def user(request, pk):        
        _user = get_object_or_404(User, pk=pk)                
        if not _user:
            return redirect('users')
        
        data = serializers.serialize('json', [_user])        
        return HttpResponse(data, content_type="application/json")


    @login_required
    def add(request):
        template_path = 'forms/user-form.html'

        if request.method == 'POST':
            form = UserNewForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, "Usuario guardado exitosamente")
                return redirect("users")
            else:                       
                return render(request, template_path, {'form': form})    

        form = UserNewForm()
        return render(request, template_path, {'form': form})
    

    @login_required
    def edit(request, pk):
        template_path = 'forms/user-form.html'        
        try:
            user = get_object_or_404(User, pk=pk)

            if request.method == 'POST':            
                form = UserUpdateForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.INFO, "Usuario actualizado exitosamente")
                    return redirect("users")
                else:
                    return render(request, template_path, {'form': form})        
            else:
                form = UserUpdateForm(instance=user)        
                return render(request, template_path, {'form': form, 'useredit': user})
        except Exception as ex:            
            messages.add_message(request, messages.ERROR, 'No se ha podido actualizar el usuario')
            return redirect('users')
        
        
    @login_required
    def edit_password(request, pk):
        template_path = 'forms/password-form.html'        
        try:            
            if request.method == 'POST':                            
                user = get_object_or_404(User, pk=pk)
                form = PasswordChangeForm(user=user)                
                                
                print(f"FORM VALID: {form.is_valid}")
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.INFO, "Contraseña actualizada exitosamente")
                    return redirect("users")
                else:
                    print(f"FORM ERROR: {form.errors}")
                    return render(request, template_path, {'form': form, 'useredit': user})        
            else:                                
                user = get_object_or_404(User, pk=pk)
                form = PasswordChangeForm(user=user)        
                return render(request, template_path, {'form': form, 'useredit': user})
        except Exception as ex:
            print(f"ERROR: {ex}")
            messages.add_message(request, messages.ERROR, 'No se ha podido actualizar la contraseña del usuario')
            return redirect('users')


    @login_required
    def delete(request):        
        if request.method == 'POST':
            try:                
                pk = request.POST['userid']
                user = get_object_or_404(User, pk=pk)        
                if request.method == 'POST':            
                    user.delete()                            
                    messages.add_message(request, messages.INFO, 'Usuario eliminado satisfactoriamente')
                    return redirect('users')                
            except:
                messages.add_message(request, messages.ERROR, 'No se ha podido eliminar al usuario')
                return redirect('users')
            
        return redirect('users')


