from django.contrib import admin
from .models import TinNhan

@admin.register(TinNhan)
class TinNhanAdmin(admin.ModelAdmin):
    list_display = ('id_tinnhan', 'nguoi_gui', 'noi_dung', 'thoi_gian_gui', 'id_khachhang', 'id_nhanvien')
    list_filter = ('nguoi_gui', 'thoi_gian_gui')
    search_fields = ('noi_dung',)
    ordering = ('-thoi_gian_gui',)
