from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core import serializers
import shortuuid

from ..forms import PersonForm
from ..models import Persons


class PersonView(object):

        
    @login_required
    def index(request):        
        _persons = Persons.objects.all()        
        return render(request, 'persons.html', {"persons": _persons })
        
    
    @login_required
    def person(request, pk):        
        _person = get_object_or_404(Persons, pk=pk)                
        if not _person:
            return redirect('persons')
        
        data = serializers.serialize('json', [_person])        
        return HttpResponse(data, content_type="application/json")

    
    @login_required
    def add(request):
        template_path = 'forms/person-form.html'
        if request.method == 'POST':
            form = PersonForm(request.POST)            
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                
                messages.add_message(request, messages.INFO, "Persona guardado exitosamente")
                return redirect("persons")                
            else:
                return render(request, template_path, {'form': form})   
            
        form = PersonForm()        
        form.initial['identifier'] = shortuuid.ShortUUID().random(length=15).upper()        
        return render(request, template_path, {'form': form})
    

    @login_required
    def edit(request, pk):
        template_path = 'forms/person-form.html'        
        try:
            person = get_object_or_404(Persons, pk=pk)

            if request.method == 'POST':            
                form = PersonForm(request.POST, instance=person)
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.INFO, "Persona actualizada exitosamente")
                    return redirect("persons")
                else:
                    return render(request, template_path, {'form': form})        
            else:
                form = PersonForm(instance=person)        
                return render(request, template_path, {'form': form, 'person': person})
        except Exception as ex:            
            messages.add_message(request, messages.ERROR, 'No se ha podido actualizar la persona')
            return redirect('persons')
    
    
    @login_required
    def delete(request):        
        if request.method == 'POST':
            try:                
                pk = request.POST['personid']
                book = get_object_or_404(Persons, pk=pk)        
                if request.method == 'POST':            
                    book.delete()                            
                    messages.add_message(request, messages.INFO, 'Persona eliminada satisfactoriamente')
                    return redirect('persons')                
            except:
                messages.add_message(request, messages.ERROR, 'No se ha podido eliminar la Persona')
                return redirect('persons')
            
        return redirect('persons')