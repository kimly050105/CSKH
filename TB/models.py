from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Bảng Thông báo thực tế
class ThongBao(models.Model):
    tieu_de = models.CharField(max_length=200)
    noi_dung = models.TextField()
    ngay_tao = models.DateTimeField(auto_now_add=True)
    nguoi_gui = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='da_gui')
    nguoi_nhan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ds_thong_bao')
    da_doc = models.BooleanField(default=False)

    def __str__(self):
        return self.tieu_de