from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from ..forms import BookForm
from ..models import Baptisms, Communions, Books


class BookView(object):
    
    @staticmethod
    def empty_response(headers={}):
        return HttpResponse(status=204, headers=headers)
    

    def index(request):        
        return render(request, 'books.html', {})
    

    @login_required
    def count(request):        
        count = len(Books.objects.all())
        return HttpResponse(count)


    @login_required
    def books(request):    
        template_path = 'partial/book/book-list.html'
        _books = Books.objects.all()    
        return render(request, template_path, {'bookList': _books})
    
    @login_required
    def add(request):
        template_path = 'partial/book/book-form.html'
        headers={'HX-Trigger': 'bookItemsChanged'}
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                
                return BookView.empty_response(headers=headers)
            else:
                return render(request, template_path, {'form': form})   
            
        form = BookForm()
        return render(request, template_path, {'form': form})
    

    @login_required
    def edit(request, pk):
        template_path = 'partial/book/book-form.html'
        headers={'HX-Trigger': 'bookItemsChanged'}
        try:
            book = get_object_or_404(Books, pk=pk)

            if request.method == 'POST':
                form = BookForm(request.POST, instance=book)
                if form.is_valid():
                    form.save()
                else:
                    return render(request, template_path, {'form': form})        
                
                return BookView.empty_response(headers=headers)            
            else:
                form = BookForm(instance=book)
                form.fields['title'].disabled = True
                form.fields['n_pages'].disabled = True
                return render(request, template_path, {'form': form, 'book': book})
        except Exception as ex:
            return BookView.empty_response(headers=headers)   
        

    @login_required
    def delete(request, pk):
        template_path = 'partial/book/delete-form.html'
        headers={'HX-Trigger': 'bookItemsChanged'}
        try:    
            context = {}
            
            book = get_object_or_404(Books, pk=pk)        
            context['book'] = book

            count_certificates = 0
            if book.title == Books.TitleChoices.BAUTISMOS:
                count_certificates = Baptisms.objects.filter(book=book).count()        
            elif book.title == Books.TitleChoices.COMUNIONES:
                count_certificates = Communions.objects.filter(book=book).count()        


            if count_certificates > 0:                        
                    context['has_certificates'] = True


            if request.method == 'POST':            
                book.delete()                            
                return BookView.empty_response(headers=headers)                
            else:
                
                return render(request, template_path, context)
        except:
            return BookView.empty_response(headers=headers)