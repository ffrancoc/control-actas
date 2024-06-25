from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from ..forms import CommunionForm
from ..models import Communions, Books


class CommunionView(object):
    
    @staticmethod
    def empty_response(headers={}):
        return HttpResponse(status=204, headers=headers)
    

    def index(request):        
        return render(request, 'communions.html', {})
    

    @login_required
    def count_by_book(request, pk):
        book = get_object_or_404(Books, pk=pk)
        communions = Communions.objects.filter(book=book).count()

        response = f'{communions}/{book.n_pages} Actas'    
        return HttpResponse(response)
    
    
    @login_required
    def count(request):        
        count = len(Communions.objects.all())
        return HttpResponse(count)
    

    @login_required
    def communions(request):
        template_path = 'partial/communion/communion-list.html'
        _communions = Communions.objects.all()
        return render(request, template_path, {'communionList': _communions})
    

    @login_required
    def add(request):
        template_path = 'partial/communion/communion-form.html'
        headers={'HX-Trigger': 'communionItemsChanged'}

        if request.method == 'POST':
            form = CommunionForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()

                return CommunionView.empty_response(headers=headers)
            else:
                print(form.errors)
                return render(request, template_path, {'form': form})   
        
        form = CommunionForm()
        return render(request, template_path, {'form': form})