from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from . import models
from . import forms

def add_book(request):
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'bookItemsChanged'}) # Return Respuesta vacia
        else:
            return render(request, 'partial/book-form.html', {'form': form})    

    form = forms.BookForm()
    return render(request, 'partial/book-form.html', {'form': form})


def edit_book(request, pk):
    book = get_object_or_404(models.Books, pk=pk)

    if request.method == 'POST':
        form = forms.BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'partial/book-form.html', {'form': form})        
        
        return HttpResponse(status=204, headers={'HX-Trigger': 'bookItemsChanged'})
    else:
        form = forms.BookForm(instance=book)
        form.fields['title'].disabled = True
        form.fields['n_pages'].disabled = True
        return render(request, 'partial/book-form.html', {'form': form, 'book': book})


def delete_book(request, pk):
    book = get_object_or_404(models.Books, pk=pk)
    if request.method == 'POST':
        book.delete()
        return HttpResponse(status=204, headers={'HX-Trigger': 'bookItemsChanged'})
    else:
        return render(request, 'partial/delete-form.html', {'book': book})


def index(request):
    return render(request, 'index.html', {})


def book_List(request):
    bookList = models.Books.objects.all()
    return render(request, 'partial/book_list.html', {'bookList': bookList})


def books(request):
    return render(request, 'books.html', {})