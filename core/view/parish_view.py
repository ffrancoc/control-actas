import shortuuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ParishForm
from ..models import Parishs


class ParishView(object):
        
    @login_required
    def index(request):        
        _parishs = Parishs.objects.all()        
        return render(request, 'parishs.html', {"parishs": _parishs })
        
    
    @login_required
    def add(request):
        template_path = 'forms/parish-form.html'
        if request.method == 'POST':
            form = ParishForm(request.POST)            
            if form.is_valid():
                form.save()                                
                
                messages.add_message(request, messages.INFO, "Parroquia creada exitosamente")
                return redirect("parishs")                
            else:
                return render(request, template_path, {'form': form})   
            
        form = ParishForm()        
        return render(request, template_path, {'form': form})
    

    @login_required
    def edit(request, pk):
        template_path = 'forms/parish-form.html'        
        try:
            parish = get_object_or_404(Parishs, pk=pk)

            if request.method == 'POST':            
                form = ParishForm(request.POST, instance=parish)
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.INFO, "Parroquia actualizada exitosamente")
                    return redirect("parishs")
                else:
                    return render(request, template_path, {'form': form})        
            else:
                form = ParishForm(instance=parish)        
                return render(request, template_path, {'form': form, 'parish': parish})
        except Exception as ex:            
            messages.add_message(request, messages.ERROR, 'No se ha podido actualizar la parroquia')
            return redirect('parishs')
    
    
    @login_required
    def delete(request):        
        if request.method == 'POST':
            try:                
                pk = request.POST['parishid']
                parish = get_object_or_404(Parishs, pk=pk)        
                if request.method == 'POST':            
                    parish.delete()                            
                    messages.add_message(request, messages.INFO, 'La parroquia se ha eliminado satisfactoriamente')
                    return redirect('parishs')                
            except:
                messages.add_message(request, messages.ERROR, 'No se ha podido eliminar la parroquia')
                return redirect('parishs')
            
        return redirect('parishs')