from django.db import models
from django.utils import timezone
from TK.models import KhachHang, ThuCung, NhanVien, DichVu

class LichHen(models.Model):
    TRANG_THAI_CHOICES = [
        ('sap_toi', 'Sắp tới'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Đã hủy'),
    ]

    khach_hang = models.ForeignKey(
        KhachHang, on_delete=models.CASCADE, related_name='lich_hen',
        verbose_name="Khách hàng"
    )
    thu_cung = models.ForeignKey(
        ThuCung, on_delete=models.CASCADE, related_name='lich_hen',
        verbose_name="Thú cưng"
    )
    dich_vu = models.ForeignKey(
        DichVu, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='lich_hen', verbose_name="Dịch vụ"
    )
    nhan_vien = models.ForeignKey(
        NhanVien, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='lich_hen', verbose_name="Nhân viên phụ trách"
    )

    # 🔹 Thông tin bổ sung cho bảng hiển thị
    so_dien_thoai = models.CharField(max_length=15, blank=True, null=True)
    can_nang = models.CharField(max_length=20, blank=True, null=True)
    ghi_chu = models.TextField(blank=True, null=True)

    # 🔹 Dành riêng cho trang "Lịch sử lịch hẹn"
    danh_gia = models.CharField(max_length=255, blank=True, null=True)
    khieu_nai = models.TextField(blank=True, null=True)

    thoi_gian = models.DateTimeField(verbose_name="Thời gian hẹn")
    trang_thai = models.CharField(
        max_length=20, choices=TRANG_THAI_CHOICES, default='sap_toi'
    )
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.thu_cung.ten_thucung} - {self.khach_hang.user.username} ({self.trang_thai})"
from django.db import models

# Create your models here.
