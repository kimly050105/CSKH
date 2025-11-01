from django.contrib import admin
from .models import (KhachHang, NhanVien, ThuCung)
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from TK.models import NhanVien


class NhanVienAdmin(admin.ModelAdmin):
    list_display = ('ho_ten', 'chuc_vu', 'email', 'so_dien_thoai','dia_chi', 'ngay_vao_lam')
    list_filter =('chuc_vu','ngay_vao_lam')
    search_fields = ('ho_ten', 'so_dien_thoai')
    ordering = ('ngay_vao_lam',)
class KhachHangAdmin(admin.ModelAdmin):
   list_display = ('ho_ten', 'so_dien_thoai', 'dia_chi','email', 'gioi_tinh', 'ngay_sinh', 'ngay_tham_gia')
   search_fields = ( 'ho_ten', 'so_dien_thoai' )
   ordering = ('ngay_tham_gia',)

class ThuCungAdmin(admin.ModelAdmin):
   list_display = ('ten_thucung', 'loai', 'tuoi', 'can_nang', 'ghi_chu','khach_hang')
   list_filter = ('loai', 'khach_hang')
   search_fields = ('ten_thucung', 'khach_hang')


# Kế thừa UserAdmin mặc định để tùy chỉnh hành vi khi lưu
class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        # Gọi phương thức gốc để lưu user
        super().save_model(request, obj, form, change)

        # Khi user được lưu hoặc cập nhật:
        if obj.is_staff:
            # Nếu là nhân viên => tạo hoặc cập nhật NhanVien tương ứng
            NhanVien.objects.update_or_create(
                user=obj,
                defaults={
                    'ho_ten': obj.get_full_name() or obj.username,
                    'email': obj.email,
                    'chuc_vu': '',
                    'so_dien_thoai': '',
                    'dia_chi': '',
                    'ngay_vao_lam': timezone.now().date(),
                }
            )
        else:
            # Nếu bỏ quyền staff => xóa bản ghi NhanVien
            NhanVien.objects.filter(user=obj).delete()

# Gỡ bỏ UserAdmin mặc định của Django
admin.site.unregister(User)
# Đăng ký lại với phiên bản tùy chỉnh
admin.site.register(User, CustomUserAdmin)
admin.site.register(KhachHang, KhachHangAdmin)
admin.site.register(NhanVien, NhanVienAdmin)
admin.site.register(ThuCung, ThuCungAdmin)
