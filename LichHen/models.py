from django.db import models
from django.utils import timezone
from TK.models import KhachHang, ThuCung, NhanVien
from DV.models import DichVu
from django.core.validators import RegexValidator


class LichHen(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Số điện thoại phải gồm đúng 10 chữ số."
    )
    TRANG_THAI_CHOICES = [
        ('sap_toi', 'Sắp tới'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Đã hủy'),
    ]

    khach_hang = models.ForeignKey(
        KhachHang,
        on_delete=models.CASCADE,
        help_text="Khách hàng đặt lịch hẹn."
    )
    thu_cung = models.ForeignKey(
        ThuCung,
        on_delete=models.CASCADE,
        help_text="Thú cưng được chăm sóc."
    )
    nhan_vien = models.ForeignKey(
        NhanVien,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Nhân viên phụ trách dịch vụ."
    )
    so_dien_thoai = models.CharField(
        max_length=10,
        validators=[phone_validator],
        blank=False,  # ❌ không được để trống
        null=False,  # ❌ không được null
        verbose_name="Số điện thoại"
    )
    thoi_gian = models.DateTimeField(help_text="Thời gian thực hiện dịch vụ.")
    ghi_chu = models.TextField(blank=True, help_text="Ghi chú đặc biệt của khách hàng.")
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='sap_toi')
    ly_do_huy = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.khach_hang.ho_ten} - {self.thu_cung.ten_thucung}"
class DV_LichHen(models.Model):
    lich_hen = models.ForeignKey(LichHen, on_delete=models.CASCADE)
    dich_vu = models.ForeignKey('DV.DichVu', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.dich_vu.ten_dich_vu} trong {self.lich_hen}"