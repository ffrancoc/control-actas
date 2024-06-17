from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Value
from . import models
from . import forms

RETURN_EMPTY_STATUS_RESPONSE = 204

def empty_response(headers={}):
    return HttpResponse(status=RETURN_EMPTY_STATUS_RESPONSE, headers=headers)


def preview_baptism(request, pk):
    try:    
        baptism = get_object_or_404(models.Baptisms, pk=pk)                
        return render(request, 'partial/preview-baptism.html', {'baptism': baptism})
    except:
        return empty_response()



def add_book(request):
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            form.save()
            headers={'HX-Trigger': 'bookItemsChanged'}
            return empty_response(headers=headers)
        else:
            return render(request, 'partial/book-form.html', {'form': form})    

    form = forms.BookForm()
    return render(request, 'partial/book-form.html', {'form': form})


def add_baptism(request):
    if request.method == 'POST':        
        form = forms.BaptismForm(request.POST)
        if form.is_valid():
            form.save()
            headers={'HX-Trigger': 'baptismItemsChanged'}
            return empty_response(headers=headers)
        else:
            print(form.errors)
            return render(request, 'partial/baptism-form.html', {'form': form})    

    form = forms.BaptismForm()
    return render(request, 'partial/baptism-form.html', {'form': form})


def edit_book(request, pk):
    headers={'HX-Trigger': 'bookItemsChanged'}
    try:
        book = get_object_or_404(models.Books, pk=pk)

        if request.method == 'POST':
            form = forms.BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
            else:
                return render(request, 'partial/book-form.html', {'form': form})        
            
            return empty_response(headers=headers)            
        else:
            form = forms.BookForm(instance=book)
            form.fields['title'].disabled = True
            form.fields['n_pages'].disabled = True
            return render(request, 'partial/book-form.html', {'form': form, 'book': book})
    except Exception as ex:
        return empty_response(headers=headers)     
    

def edit_baptism(request, pk):
    headers={'HX-Trigger': 'baptismItemsChanged'}
    try:
        baptism = get_object_or_404(models.Baptisms, pk=pk)

        if request.method == 'POST':
            form = forms.BaptismForm(request.POST, instance=baptism)
            if form.is_valid():
                form.save()
            else:
                return render(request, 'partial/baptism-form.html', {'form': form})        
            
            return empty_response(headers=headers)
        else:
            form = forms.BaptismForm(instance=baptism)            
            return render(request, 'partial/baptism-form.html', {'form': form, 'baptism': baptism})
    except Exception as ex:
        return empty_response(headers=headers)


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
            
            return render(request, 'partial/delete-book.html', context)
    except:
        return empty_response(headers=headers)



def delete_baptism(request, pk):
    headers={'HX-Trigger': 'baptismItemsChanged'}
    try:    
        baptism = get_object_or_404(models.Baptisms, pk=pk)        
        if request.method == 'POST':            
            baptism.delete()                            
            return HttpResponse(status=RETURN_EMPTY_STATUS_RESPONSE, headers=headers)
        else:
            return render(request, 'partial/delete-baptism.html', {'baptism': baptism})
    except:
        return empty_response(headers=headers)


def index(request):
    return render(request, 'index.html', {})


def books(request):
    return render(request, 'books.html', {})

def book_list(request):    
    booklist = models.Books.objects.all()    
    return render(request, 'partial/book_list.html', {'bookList': booklist})


def baptisms(request):        
    return render(request, 'baptisms.html', {})

def baptisms_list(request):
    baptismlist = models.Baptisms.objects.all()        
    return render(request, 'partial/baptism_list.html', {'baptismList': baptismlist})


def baptisms_count(request, pk):
    book = get_object_or_404(models.Books, pk=pk)
    baptisms = models.Baptisms.objects.filter(book=book).count()

    response = f'{baptisms}/{book.n_pages} Actas'    
    return HttpResponse(response)