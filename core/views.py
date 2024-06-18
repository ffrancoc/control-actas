from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from . import models
from . import forms

RETURN_EMPTY_STATUS_RESPONSE = 204

def empty_response(headers={}):
    return HttpResponse(status=RETURN_EMPTY_STATUS_RESPONSE, headers=headers)

@login_required
def logout_session(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'index.html', {})

@login_required
def home(request):
    return render(request, 'home.html', {})

@login_required
# @user_passes_test(lambda u: u.is_superuser)
def users(request):        
    return render(request, 'users.html', {})

@login_required
def books(request):
    return render(request, 'books.html', {})

@login_required
def baptisms(request):        
    return render(request, 'baptisms.html', {})

@login_required
def user_list(request):    
    loggedin_user = request.user
    user_list = User.objects.all()            
    return render(request, 'partial/user/user-list.html', {'userList': user_list, 'loggedInUser': loggedin_user})

@login_required
def book_list(request):    
    book_list = models.Books.objects.all()    
    return render(request, 'partial/book/book-list.html', {'bookList': book_list})

@login_required
def baptisms_list(request):
    baptism_list = models.Baptisms.objects.all()        
    return render(request, 'partial/baptism/baptism-list.html', {'baptismList': baptism_list})

@login_required
def baptisms_count(request, pk):
    book = get_object_or_404(models.Books, pk=pk)
    baptisms = models.Baptisms.objects.filter(book=book).count()

    response = f'{baptisms}/{book.n_pages} Actas'    
    return HttpResponse(response)

@login_required
def edit_password(request, pk):
    headers={}
    try:
        user = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            form = PasswordChangeForm(request.POST, user=user)
            if form.is_valid():
                form.save()
            else:                
                return render(request, 'partial/user/password-form.html', {'form': form})        
            
            return empty_response(headers=headers)            
        else:
            form = PasswordChangeForm(user=user)        
            return render(request, 'partial/user/password-form.html', {'form': form})
    except Exception as ex:        
        return empty_response(headers=headers)    
    

@login_required
def preview_user(request, pk):
    try:    
        user = get_object_or_404(User, pk=pk)                
        return render(request, 'partial/user/preview-form.html', {'user': user})
    except:
        return empty_response()

@login_required
def preview_baptism(request, pk):
    try:    
        baptism = get_object_or_404(models.Baptisms, pk=pk)                
        return render(request, 'partial/baptism/preview-form.html', {'baptism': baptism})
    except:
        return empty_response()

@login_required
def add_user(request):
    if request.method == 'POST':
        form = forms.UserNewForm(request.POST)
        if form.is_valid():
            form.save()
            headers={'HX-Trigger': 'userItemsChanged'}
            return empty_response(headers=headers)
        else:
            return render(request, 'partial/user/user-form.html', {'form': form})    

    form = forms.UserNewForm()
    return render(request, 'partial/user/user-form.html', {'form': form, 'user': None})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            
            headers={'HX-Trigger': 'bookItemsChanged'}
            return empty_response(headers=headers)
        else:
            return render(request, 'partial/book/book-form.html', {'form': form})    

    form = forms.BookForm()
    return render(request, 'partial/book/book-form.html', {'form': form})

@login_required
def add_baptism(request):
    if request.method == 'POST':        
        form = forms.BaptismForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            headers={'HX-Trigger': 'baptismItemsChanged'}
            return empty_response(headers=headers)
        else:
            print(form.errors)
            return render(request, 'partial/baptism/baptism-form.html', {'form': form})    

    form = forms.BaptismForm()
    return render(request, 'partial/baptism/baptism-form.html', {'form': form})


@login_required
def edit_user(request, pk):
    headers={'HX-Trigger': 'userItemsChanged'}
    try:
        user = get_object_or_404(User, pk=pk)

        if request.method == 'POST':            
            form = forms.UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
            else:
                return render(request, 'partial/user/user-form.html', {'form': form})        
            
            return empty_response(headers=headers)            
        else:
            form = forms.UserUpdateForm(instance=user)        
            return render(request, 'partial/user/user-form.html', {'form': form, 'user': user})
    except Exception as ex:
        return empty_response(headers=headers)    

@login_required
def edit_book(request, pk):
    headers={'HX-Trigger': 'bookItemsChanged'}
    try:
        book = get_object_or_404(models.Books, pk=pk)

        if request.method == 'POST':
            form = forms.BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
            else:
                return render(request, 'partial/book/book-form.html', {'form': form})        
            
            return empty_response(headers=headers)            
        else:
            form = forms.BookForm(instance=book)
            form.fields['title'].disabled = True
            form.fields['n_pages'].disabled = True
            return render(request, 'partial/book/book-form.html', {'form': form, 'book': book})
    except Exception as ex:
        return empty_response(headers=headers)     
    
@login_required
def edit_baptism(request, pk):
    headers={'HX-Trigger': 'baptismItemsChanged'}
    try:
        baptism = get_object_or_404(models.Baptisms, pk=pk)

        if request.method == 'POST':
            form = forms.BaptismForm(request.POST, instance=baptism)
            if form.is_valid():
                form.save()
            else:
                return render(request, 'partial/baptism/baptism-form.html', {'form': form})        
            
            return empty_response(headers=headers)
        else:
            form = forms.BaptismForm(instance=baptism)            
            return render(request, 'partial/baptism/baptism-form.html', {'form': form, 'baptism': baptism})
    except Exception as ex:
        return empty_response(headers=headers)


@login_required
def delete_user(request, pk):
    print('Eliminando USUARIO')

    headers={'HX-Trigger': 'userItemsChanged'}
    try:    
        user = get_object_or_404(User, pk=pk)        
        if request.method == 'POST':            
            user.delete()                            
            return HttpResponse(status=RETURN_EMPTY_STATUS_RESPONSE, headers=headers)
        else:
            return render(request, 'partial/user/delete-form.html', {'user': user})
    except:
        return empty_response(headers=headers)



@login_required
def delete_book(request, pk):
    headers={'HX-Trigger': 'bookItemsChanged'}
    try:    
        context = {}
        
        book = get_object_or_404(models.Books, pk=pk)        
        context['book'] = book

        count_certificates = models.Baptisms.objects.filter(book=book).count()        
        if count_certificates > 0:                        
                context['has_certificates'] = True


        if request.method == 'POST':            
            book.delete()                            
            return empty_response(headers=headers)                
        else:
            
            return render(request, 'partial/book/delete-form.html', context)
    except:
        return empty_response(headers=headers)


@login_required
def delete_baptism(request, pk):
    headers={'HX-Trigger': 'baptismItemsChanged'}
    try:    
        baptism = get_object_or_404(models.Baptisms, pk=pk)        
        if request.method == 'POST':            
            baptism.delete()                            
            return HttpResponse(status=RETURN_EMPTY_STATUS_RESPONSE, headers=headers)
        else:
            return render(request, 'partial/baptism/delete-form.html', {'baptism': baptism})
    except:
        return empty_response(headers=headers)

