import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import BaptismForm
from ..models import Baptisms, Books, TitleChoices


class BaptismView(object):

    @login_required
    def index(request):        
        _baptisms = Baptisms.objects.all()                
        return render(request, 'baptisms.html', {"baptisms": _baptisms })
        
    
    @login_required
    def baptism(request, pk):        
        _baptism = get_object_or_404(Baptisms, pk=pk)                                
        if not _baptism:
            return redirect('persons')
        
        data = serializers.serialize('json', [_baptism])        
        return HttpResponse(data, content_type="application/json")

    
    @login_required
    def add(request):
        template_path = 'forms/baptism-form.html'
        if request.method == 'POST':                        
            
            form = BaptismForm(request.POST)            
            if form.is_valid():                
                obj = form.save(commit=False)
                
                
                book = get_object_or_404(Books, pk=obj.book.pk)
                if (book.certificate_count() + 1) <= book.n_pages:                
                    obj.user = request.user
                    obj.save()                    
                    messages.add_message(request, messages.INFO, "Acta guardada exitosamente")
                    return redirect("baptisms")                
                else:
                    messages.add_message(request, messages.ERROR, "No se puede guardar el acta, porque el libro ya no tiene espacios")
                    return redirect("baptisms")                
            else:
                return render(request, template_path, {'form': form})   
            
        form = BaptismForm()                     
        books = Books.objects.filter(title=TitleChoices.BAUTISMOS).all()          
        data = list(filter(lambda b:  b.certificate_count() + 1 <= b.n_pages, books))        
        books = Books.objects.filter(id__in=list(map(lambda b: b.pk, data)))
        
        form.fields['book'].queryset = books
        return render(request, template_path, {'form': form})
    

    @login_required
    def edit(request, pk):
        template_path = 'forms/baptism-form.html'        
        try:
            baptism = get_object_or_404(Baptisms, pk=pk)
            
            if request.method == 'POST':            
                form = BaptismForm(request.POST, instance=baptism)
                                                
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.INFO, "Acta actualizada exitosamente")
                    return redirect("baptisms")
                else:
                    return render(request, template_path, {'form': form})        
            else:                
                form = BaptismForm(instance=baptism)    
                
                # books = Books.objects.filter(title=TitleChoices.BAUTISMOS).all()          
                # data = list(filter(lambda b:  b.certificate_count() <= b.n_pages, books))        
                # books = Books.objects.filter(id__in=list(map(lambda b: b.pk, data)))                    
                # form.fields['book'].queryset = books
                
                return render(request, template_path, {'form': form, 'baptism': baptism})
        except:            
            messages.add_message(request, messages.ERROR, 'No se ha podido actualizar el acta.')
            return redirect('baptisms')
    
    
    @login_required
    def delete(request):        
        if request.method == 'POST':
            try:                
                pk = request.POST['baptismid']
                baptism = get_object_or_404(Baptisms, pk=pk)                        
                if request.method == 'POST':            
                    baptism.delete()                            
                    messages.add_message(request, messages.INFO, 'Acta eliminada satisfactoriamente')
                    return redirect('baptisms')                
                
            except Exception as ex:                
                messages.add_message(request, messages.ERROR, 'No se ha podido eliminar el acta')
                return redirect('baptisms')
            
        return redirect('baptisms')