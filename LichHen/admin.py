# LichHen/admin.py
from django.contrib import admin
from .models import LichHen

class LichHenAdmin(admin.ModelAdmin):
    list_display = ('khach_hang', 'so_dien_thoai','thu_cung','nhan_vien', 'thoi_gian', 'trang_thai','ghi_chu', 'ly_do_huy' )
    list_filter = ('trang_thai','nhan_vien','thoi_gian')
    search_fields = ('khach_hang__ho_ten','so_dien_thoai','thu_cung__ten_thucung','nhan_vien__ho_ten')
    ordering = ('-thoi_gian',)

admin.site.register(LichHen, LichHenAdmin)


# Register your models here.
