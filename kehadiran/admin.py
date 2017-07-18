from django.contrib import admin
from kehadiran.models import Kehadiran

# Register your models here.
class KehadiranAdmin (admin.ModelAdmin):
    list_display = ['karyawan', 'jenis_kehadiran', 'waktu']
    list_filter = ('jenis_kehadiran',)
    search_fields = []
    list_per_page = 25

admin.site.register(Kehadiran, KehadiranAdmin)