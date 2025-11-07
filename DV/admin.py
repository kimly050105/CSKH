from django.contrib import admin
from .models import DichVu
class DichVuAdmin(admin.ModelAdmin):
    list_display = ('ten_dich_vu', 'gia')
admin.site.register(DichVu, DichVuAdmin)





# Register your models here.
