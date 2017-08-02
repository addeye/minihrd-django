from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from karyawan.models import Karyawan
from kehadiran.models import Kehadiran, Izin
from kehadiran.forms import IzinForm
# Create your views here.

@login_required(login_url=settings.LOGIN_URL)
def daftar_hadir(request):
    daftar_hadir = None

    if request.method == 'POST':
        bulan = request.POST['bulan']
        tahun = request.POST['tahun']
        daftar_hadir = Kehadiran.objects.filter(waktu__year=tahun, waktu__month=bulan, karyawan__id=request.session['karyawan_id'])

    return render(request, 'new/daftar_hadir.html', {'daftar_hadir':daftar_hadir})

@login_required(login_url=settings.LOGIN_URL)
def pengajuan_izin(request):
    if request.method == 'POST':
        form_data = request.POST
        form = IzinForm(form_data)
        if form.is_valid():
            izin = Izin(
                    karyawan = Karyawan.objects.get(id=request.session['karyawan_id']),
                    jenis_kehadiran = request.POST['jenis_kehadiran'],
                    waktu_mulai = request.POST['waktu_mulai'],
                    waktu_berhenti = request.POST['waktu_berhenti'],
                    alasan = request.POST['alasan'],
                    disetujui = False,
                )
            izin.save()
            return redirect('/')
    else:
        form = IzinForm()

    return render(request, 'new/tambah_izin.html', {'form':form})

@login_required(login_url=settings.LOGIN_URL)
def daftar_izin(request):
    daftar_izin = Izin.objects.filter(karyawan__id=request.session['karyawan_id'])
    return render(request, 'new/daftar_izin.html', {'daftar_izin':daftar_izin})

@login_required(login_url=settings.LOGIN_URL)
def tampil_grafik(request, bulan, tahun):
    temp_chart_data = []
    daftar_hadir = Kehadiran.objects.filter(waktu__year=tahun, waktu__month=bulan, karyawan__id=request.session('karyawan_id'))

    temp_chart_data.append({"x":"hadir", "a":daftar_hadir.filter(jenis_kehadiran='hadir').count()})
    temp_chart_data.append({"x":"izin", "a":daftar_hadir.filter(jenis_kehadiran='izin').count()})
    temp_chart_data.append({"x":"alpa", "a":daftar_hadir.filter(jenis_kehadiran='alpa').count()})
    temp_chart_data.append({"x":"cuti", "a":daftar_hadir.filter(jenis_kehadiran='cuti').count()})
    
    chart_data = json.dumps({"data":temp_chart_data})

    return render(request, 'new/tampil_grafik.html',{'chart_data':chart_data,'bulan':bulan,'tahun':tahun})