# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages

from karyawan.models import Akun, Karyawan

# Create your views here.

def login_view(request):
	if request.POST:
		user = authenticate(username=request.POST['username'], password=request.POST['password'])

		if user is not None:
			if user.is_active:
				try:
					akun = Akun.objects.get(akun=user.id)
					login(request, user)

					request.session['karyawan_id'] = akun.karyawan_id
					request.session['jenis_akun'] = akun.jenis_akun
					request.session['username'] = request.POST['username']
				except:
					message.add_message(request, message.INFO,'Akun ini belum terhubung dengan data karyawan, silahkan hubungi administrator')
				return redirect('/')					
			else:
				message.add_message(request,message.INFO,'User belum terverifikasi')
		else:
			message.add_message(request, message.INFO, 'Username atau password anda salah')

	return render(request, 'new/login.html')

def logout_view(request):
	logout(request)
	return redirect('/login/')	