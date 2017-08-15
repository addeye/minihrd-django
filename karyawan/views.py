# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect

from karyawan.models import Karyawan

# Create your views here.
# 
@login_required(login_url=settings.LOGIN_URL)
def profil(request):
	karyawan = Karyawan.objects.get(id=request.session['karyawan_id'])
	return render(request, 'profil.html', {"karyawan":karyawan})

@login_required(login_url=settings.LOGIN_URL)
def ganti_foto(request):
    karyawan = Karyawan.objects.get(id=request.session['karyawan_id'])
    if karyawan.foto != '':
    	image_path = os.path.join(settings.MEDIA_ROOT, str(karyawan.foto))
    	try:
    		os.unlink(image_path)
    	except Exception as e:
    		raise
    	else:
    		pass
    	finally:
    		pass
    karyawan.foto = request.FILES['files']
    karyawan.save()


    return redirect('/')
