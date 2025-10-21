from django.contrib.auth.models import User
from django.db import models

class KhachHang(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    so_dien_thoai = models.CharField(max_length=15)
    dia_chi = models.CharField(max_length=255)
    gioi_tinh = models.CharField(max_length=1, choices=[('M', 'Nam'), ('F', 'Nữ')])
    ngay_sinh = models.DateField(null=True, blank=True)
    ngay_tham_gia = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class NhanVien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chuc_vu = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=15)
    dia_chi = models.CharField(max_length=255)
    ngay_vao_lam = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.chuc_vu}"


class QuanTriVien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


class DichVu(models.Model):
    ten_dichvu = models.CharField(max_length=100)
    gia = models.DecimalField(max_digits=12, decimal_places=2)
    mo_ta = models.TextField(blank=True)

    def __str__(self):
        return f"{self.ten_dichvu} - {self.gia} VND"





class ChiTietLichHen(models.Model):
    lich_hen = models.ForeignKey(LichHen, on_delete=models.CASCADE)
    dich_vu = models.ForeignKey(DichVu, on_delete=models.CASCADE)

    def __str__(self):
        return f"Lịch {self.lich_hen.id} - {self.dich_vu.ten_dichvu}"


class KhieuNaiPhanHoi(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    nhan_vien = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True, blank=True)
    noi_dung = models.TextField()
    phan_hoi = models.TextField(blank=True)
    ngay_gui = models.DateTimeField(auto_now_add=True)
    trang_thai = models.CharField(max_length=50, choices=[
        ('Chờ xử lý', 'Chờ xử lý'),
        ('Đang xử lý', 'Đang xử lý'),
        ('Đã phản hồi', 'Đã phản hồi'),
        ('Đã đóng', 'Đã đóng'),
    ], default='Chờ xử lý')

    def __str__(self):
        return f"Khiếu nại #{self.id} - {self.khach_hang.user.username}"


class TichDiem(models.Model):
    khach_hang = models.OneToOneField(KhachHang, on_delete=models.CASCADE)
    tong_diem = models.IntegerField(default=0)
    cap_bac = models.CharField(max_length=50, default="Thành viên mới")

    def __str__(self):
        return f"{self.khach_hang.user.username} - {self.tong_diem} điểm"


class ThongBao(models.Model):
    admin = models.ForeignKey(QuanTriVien, on_delete=models.CASCADE)
    loai = models.CharField(max_length=100)
    tieu_de = models.CharField(max_length=200)
    noi_dung = models.TextField()
    ngay_gui = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tieu_de


class KhachHangThongBao(models.Model):
    khach_hang = models.ForeignKey(KhachHang, on_delete=models.CASCADE)
    thong_bao = models.ForeignKey(ThongBao, on_delete=models.CASCADE)
    trang_thai = models.CharField(max_length=20, choices=[
        ('Đã đọc', 'Đã đọc'),
        ('Chưa đọc', 'Chưa đọc'),
    ], default='Chưa đọc')
    ngay_nhan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.khach_hang.user.username} - {self.thong_bao.tieu_de}"


# Create your models here.
