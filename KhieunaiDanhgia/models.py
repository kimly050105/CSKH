from django.db import models
from django.contrib.auth.models import User
from LichHen.models import LichHen

class DanhGia(models.Model):
    lich_hen = models.ForeignKey(LichHen, on_delete=models.CASCADE, related_name='danh_gia_list')
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)
    diem = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Mức độ hài lòng")
    nhan_xet = models.TextField(verbose_name="Nhận xét", blank=True)
    ngay_danh_gia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Đánh giá #{self.id} - {self.nguoi_dung.username}"


class KhieuNai(models.Model):
    lich_hen = models.ForeignKey(LichHen, on_delete=models.CASCADE, related_name='khieu_nai_list')
    nguoi_gui = models.ForeignKey(User, on_delete=models.CASCADE)
    noi_dung = models.TextField(verbose_name="Nội dung khiếu nại")
    minh_chung = models.FileField(upload_to='minhchung/', blank=True, null=True,
                                  verbose_name="Minh chứng (ảnh hoặc video)")
    yeu_cau = models.TextField(verbose_name="Yêu cầu/mong muốn", blank=True)
    phan_hoi = models.TextField(verbose_name="Phản hồi / Ghi chú từ nhân viên", blank=True, null=True)
    trang_thai = models.CharField(
        max_length=30,
        choices=[
            ('Chờ xử lý', 'Chờ xử lý'),
            ('Đang xử lý', 'Đang xử lý'),
            ('Đã phản hồi', 'Đã phản hồi'),
        ],
        default='Chờ xử lý'
    )
    ngay_gui = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Khiếu nại #{self.id} - {self.nguoi_gui.username}"
