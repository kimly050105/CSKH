from django.contrib import admin
from .models import (KhachHang, NhanVien, QuanTriVien, ThuCung, DichVu, LichHen, ChiTietLichHen,
                     KhieuNaiPhanHoi, TichDiem, ThongBao, KhachHangThongBao)

admin.site.register(KhachHang)
admin.site.register(NhanVien)
admin.site.register(QuanTriVien)
admin.site.register(ThuCung)
admin.site.register(DichVu)
admin.site.register(LichHen)
admin.site.register(ChiTietLichHen)
admin.site.register(KhachHangThongBao)
admin.site.register(KhieuNaiPhanHoi)
admin.site.register(TichDiem)
admin.site.register(ThongBao)




# Register your models here.
