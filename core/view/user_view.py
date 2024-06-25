from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from ..forms import UserNewForm, UserUpdateForm
from django.http import HttpResponse

class UserView(object):

    @staticmethod
    def empty_response(headers={}):
        return HttpResponse(status=204, headers=headers)
    

    def index(request):        
        return render(request, 'users.html', {})
    

    @login_required
    def count(request):        
        count = len(User.objects.all())
        return HttpResponse(count)
    

    @login_required
    def users(request):    
        template_path = 'partial/user/user-list.html'
        loggedin_user = request.user
        _users = User.objects.all()          
        
        return render(request, template_path, {'userList': _users, 'loggedInUser': loggedin_user})


    @login_required
    def preview(request, pk):
        template_path = 'partial/user/preview-form.html'
        try:    
            user = get_object_or_404(User, pk=pk)       
            context = {'user': user}         

            return render(request, template_path, context)
        except:
            return UserView.empty_response()


    @login_required
    def add(request):
        template_path = 'partial/user/user-form.html'
        headers={'HX-Trigger': 'userItemsChanged'}

        if request.method == 'POST':
            form = UserNewForm(request.POST)
            if form.is_valid():
                form.save()
                return UserView.empty_response(headers=headers)
            else:
                return render(request, template_path, {'form': form})    

        form = UserNewForm()
        return render(request, template_path, {'form': form, 'user': None})



    @login_required
    def edit(request, pk):
        template_path = 'partial/user/user-form.html'
        headers={'HX-Trigger': 'userItemsChanged'}
        try:
            user = get_object_or_404(User, pk=pk)

            if request.method == 'POST':            
                form = UserUpdateForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                else:
                    return render(request, template_path, {'form': form})        
                
                return UserView.empty_response(headers=headers)            
            else:
                form = UserUpdateForm(instance=user)        
                return render(request, template_path, {'form': form, 'user': user})
        except Exception as ex:
            return UserView.empty_response(headers=headers)  


    @login_required
    def delete(request, pk):
        template_path = 'partial/user/delete-form.html'
        headers={'HX-Trigger': 'userItemsChanged'}
        try:                
            user = get_object_or_404(User, pk=pk)        
            if request.method == 'POST':            
                user.delete()                            
                return UserView.empty_response(headers=headers)
            else:
                return render(request, template_path, {'user': user})
        except:
            return UserView.empty_response(headers=headers)


    @login_required
    def edit_password(request, pk):
        template_path = 'partial/user/password-form.html'
        headers={}
        try:
            user = get_object_or_404(User, pk=pk)
            if request.method == 'POST':
                form = PasswordChangeForm(request.POST, user=user)
                if form.is_valid():
                    form.save()
                else:                
                    return render(request, template_path, {'form': form})        
                
                return UserView.empty_response(headers=headers)            
            else:
                form = PasswordChangeForm(user=user)        
                return render(request, template_path, {'form': form})
        except Exception as ex:        
            return UserView.empty_response(headers=headers)    