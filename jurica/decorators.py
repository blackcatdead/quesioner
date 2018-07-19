from django.shortcuts import redirect
from jurica.models import Responden
from django.core.exceptions import PermissionDenied
def tesdeco(func):
    def decorated(request, *args, **kwargs):
        # print (request.session['id_user'])
        if 'id_responden' not in request.session:
        	return redirect('masuk/?init=0')
        else:
        	return func(request, *args, **kwargs)
	# decorated.__doc__ = func.__doc__
	# decorated.__name__ = func.__name__
    return decorated

def decoadmin(func):
    def decorated(request, *args, **kwargs):
        # print (request.session['id_user'])
        if 'admin' not in request.session:
            return redirect('masukadmin')
        else:
            return func(request, *args, **kwargs)
    # decorated.__doc__ = func.__doc__
    # decorated.__name__ = func.__name__
    return decorated


def ifselesai(func):
    def decorated2(request, *args, **kwargs):
        # print (request.session['id_user'])
        r= Responden.objects.get(id_responden=request.session['id_responden'])
        if r.status ==2 or r.status ==3:
        	return redirect('selesai')
        else:
        	return func(request, *args, **kwargs)
    return decorated2

def ifblmselesai(func):
    def decorated3(request, *args, **kwargs):
        # print (request.session['id_user'])
        r= Responden.objects.get(id_responden=request.session['id_responden'])
        if r.status ==1:
        	return redirect('pertanyaan')
        else:
        	return func(request, *args, **kwargs)
    return decorated3

def ifsudahmulai(func):
    def decorated4(request, *args, **kwargs):
        # print (request.session['id_user'])
        r= Responden.objects.get(id_responden=request.session['id_responden'])
        if r.stage ==0:
            return redirect('/')
        else:
            return func(request, *args, **kwargs)
    return decorated4
    