import shortuuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.utils import IntegrityError

from ..forms import BookForm
from ..models import Books


class BookView(object):
        
    @login_required
    def index(request):        
        _books = Books.objects.all()        
        return render(request, 'books.html', {"books": _books })
        
    
    @login_required
    def add(request):
        template_path = 'forms/book-form.html'
        if request.method == 'POST':
            form = BookForm(request.POST)            
            if form.is_valid():                                                
                obj = form.save(commit=False)                
                obj.user = request.user
                obj.save()
                
                messages.add_message(request, messages.INFO, "Libro guardado exitosamente")
                return redirect("books")                
            else:
                return render(request, template_path, {'form': form})   
            
        form = BookForm()
        form.initial['identifier'] = shortuuid.ShortUUID().random(length=15).upper()        
        return render(request, template_path, {'form': form})
    

    @login_required
    def edit(request, pk):
        template_path = 'forms/book-form.html'        
        try:
            book = get_object_or_404(Books, pk=pk)

            if request.method == 'POST':            
                form = BookForm(request.POST, instance=book)
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.INFO, "Libro actualizado exitosamente")
                    return redirect("books")
                else:
                    return render(request, template_path, {'form': form})        
            else:
                form = BookForm(instance=book)   
                if book.certificate_count() > 0:
                    form.fields['title'].disabled = True
                    form.fields['n_pages'].disabled = True     
                return render(request, template_path, {'form': form, 'book': book})
        except:            
            messages.add_message(request, messages.ERROR, 'No se ha podido actualizar el libro')
            return redirect('books')
    
    
    @login_required
    def delete(request):        
        if request.method == 'POST':
            try:                
                pk = request.POST['bookid']
                book = get_object_or_404(Books, pk=pk)        
                if request.method == 'POST':            
                    book.delete()                            
                    messages.add_message(request, messages.INFO, 'Libro eliminado satisfactoriamente')
                    return redirect('books')                
            except IntegrityError as ex:
                messages.add_message(request, messages.ERROR, 'Libro no eliminado, porque tiene referencias en las actas registradas')
                return redirect('books')
            except Exception:
                messages.add_message(request, messages.ERROR, 'No se ha podido eliminar el Libro')
                return redirect('books')
            
        return redirect('books')