from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from ..forms import BaptismForm
from ..models import Baptisms, Books
from django.core import serializers
import json


class BaptismView(object):

    @staticmethod
    def empty_response(headers={}):
        return HttpResponse(status=204, headers=headers)
    

    def index(request):        
        return render(request, 'baptisms.html', {})
    
    @login_required
    def baptism_by_pk(request):
        pk = request.GET.get('baptism', 0)
        pk = pk if pk != '' else 0
    
        baptism = Baptisms.objects.filter(pk=pk)


        
        if len(baptism) > 0:
            data = '<div>'
            data += f'<p id="v_firstname" hidden>{baptism[0].firstname}</p>'
            data += f'<p id="v_lastname" hidden>{baptism[0].lastname}</p>'
            data += f'<p id="v_birthplace" hidden>{baptism[0].birthplace}</p>'
            data += f'<p id="v_birthday" hidden>{baptism[0].birthday}</p>'
            data += f'<input type="text" name="gender" id="v_gender" value="{baptism[0].gender}" hidden readonly>'
            data += f'<p id="v_father_info" hidden>{baptism[0].father_info}</p>'
            data += f'<p id="v_mother_info" hidden>{baptism[0].mother_info}</p>'
            data += f'<p id="v_baptism_parish" hidden>{baptism[0].baptism_parish}</p>'
            data += f'<p id="v_baptism_date" hidden>{baptism[0].baptism_date}</p>'
            data += '</div>'
            baptism = data
        else:
            baptism = {}
        
        
        return HttpResponse(baptism)


    @login_required
    def count_by_book(request, pk):
        book = get_object_or_404(Books, pk=pk)
        baptisms = Baptisms.objects.filter(book=book).count()

        response = f'{baptisms}/{book.n_pages} Actas'    
        return HttpResponse(response)


    @login_required
    def count(request):        
        count = len(Baptisms.objects.all())
        return HttpResponse(count)
    
    
    @login_required
    def baptisms(request):
        template_path = 'partial/baptism/baptism-list.html'
        _baptisms = Baptisms.objects.all()        
        return render(request, template_path, {'baptismList': _baptisms})


    @login_required
    def preview(request, pk):
        template_path = 'partial/baptism/preview-form.html'
        try:    
            baptism = get_object_or_404(Baptisms, pk=pk)                
            return render(request, template_path, {'baptism': baptism})
        except:
            return BaptismView.empty_response()
        
    
    @login_required
    def add(request):
        template_path = 'partial/baptism/baptism-form.html'
        headers={'HX-Trigger': 'baptismItemsChanged'}

        if request.method == 'POST':        
            form = BaptismForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()

                return BaptismView.empty_response(headers=headers)
            else:
                return render(request, template_path, {'form': form})    

        form = BaptismForm()
        return render(request, template_path, {'form': form})
    
        
    @login_required
    def edit(request, pk):
        template_path = 'partial/baptism/baptism-form.html'
        headers={'HX-Trigger': 'baptismItemsChanged'}

        try:
            baptism = get_object_or_404(Baptisms, pk=pk)

            if request.method == 'POST':
                form = BaptismForm(request.POST, instance=baptism)
                if form.is_valid():
                    form.save()
                else:
                    return render(request, template_path, {'form': form})        
                
                return BaptismView.empty_response(headers=headers)
            else:
                form = BaptismForm(instance=baptism)            
                return render(request, template_path, {'form': form, 'baptism': baptism})
        except Exception as ex:
            return BaptismView.empty_response(headers=headers)
        

    @login_required
    def delete(request, pk):
        template_path = 'partial/baptism/delete-form.html'
        headers={'HX-Trigger': 'baptismItemsChanged'}

        try:    
            baptism = get_object_or_404(Baptisms, pk=pk)        
            if request.method == 'POST':            
                baptism.delete()                            
                return BaptismView.empty_response(headers=headers)
            else:
                return render(request, template_path, {'baptism': baptism})
        except:
            return BaptismView.empty_response(headers=headers)