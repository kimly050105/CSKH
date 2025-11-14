from django.db import models
from django.contrib.auth.models import User
from TK.models import KhachHang, NhanVien

class TinNhan(models.Model):
    id_tinnhan = models.AutoField(primary_key=True)
    id_khachhang = models.ForeignKey(KhachHang, on_delete=models.CASCADE, null=True, blank=True, related_name='tinnhan_khachhang')
    id_nhanvien = models.ForeignKey(NhanVien, on_delete=models.CASCADE, null=True, blank=True, related_name='tinnhan_nhanvien')
    id_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tinnhan_admin')
    session_key = models.CharField(max_length=64, null=True, blank=True)

    NGUOI_GUI_CHOICES = [
        ('khachhang', 'Khách hàng'),
        ('khach_vang_lai', 'Khách vãng lai'),
        ('nhanvien', 'Nhân viên'),
        ('admin', 'Quản trị viên'),
        ('bot', 'Hệ thống tự động'),
    ]
    nguoi_gui = models.CharField(max_length=20, choices=NGUOI_GUI_CHOICES)
    noi_dung = models.TextField()
    thoi_gian_gui = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"[{self.nguoi_gui}] {self.noi_dung[:30]}"
