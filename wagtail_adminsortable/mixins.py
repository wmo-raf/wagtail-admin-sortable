import json

from django.db import transaction
from django.http import JsonResponse
from .utils import is_ajax


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView
    """
    
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if is_ajax(self.request):
            return JsonResponse(form.errors, status=400)
        else:
            return response
    
    def form_valid(self, form):
        super(AjaxableResponseMixin, self).form_valid(form)
        if is_ajax(self.request):
            objects = json.loads(self.request.POST.get('objects', '[]'))
            data = {
                'message': 'success'
            }
            
            with transaction.atomic():
                try:
                    for obj in objects:
                        self.model.objects.filter(pk=obj.pop('pk')).update(**obj)
                except Exception as e:
                    str(e)
            return JsonResponse(data)
        
        return JsonResponse({'message': 'Invalid Data'}, status=400)
