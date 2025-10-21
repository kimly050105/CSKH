from django.contrib.auth.models import User
from django.db import models

class KhachHang(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    ho_ten = models.CharField(max_length=100, blank=True)
    so_dien_thoai = models.CharField(max_length=15)
    dia_chi = models.CharField(max_length=255)
    gioi_tinh = models.CharField(max_length=1, choices=[('M', 'Nam'), ('F', 'Nữ')])
    ngay_sinh = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    ngay_tham_gia = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username



class NhanVien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    chuc_vu = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=15)
    dia_chi = models.CharField(max_length=255)
    ngay_vao_lam = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.chuc_vu}"


class QuanTriVien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    quyen_han = models.CharField(max_length=100, default="Toàn quyền")
    ngay_tao_quyen = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Admin: {self.user.username}"


class ThuCung(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    ten_thucung = models.CharField(max_length=100)
    loai = models.CharField(max_length=100)
    tuoi = models.IntegerField()
    ghi_chu = models.TextField(blank=True)

    def __str__(self):
        return f"{self.ten_thucung} ({self.loai})"
