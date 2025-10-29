from django.contrib import admin
from .models import KhieuNai, DanhGia

# 🌸 Cấu hình hiển thị cho model Khiếu nại
@admin.register(KhieuNai)
class KhieuNaiAdmin(admin.ModelAdmin):
    # Các cột hiển thị trong danh sách
    list_display = (
        'id',
        'nguoi_gui',
        'get_thu_cung',
        'get_dich_vu',
        'trang_thai',
        'ngay_gui',
    )

    # Bộ lọc bên phải
    list_filter = ('trang_thai', 'ngay_gui')

    # Ô tìm kiếm
    search_fields = (
        'nguoi_gui__username',
        'lich_hen__thu_cung__ten_thucung',
        'noi_dung',
    )

    # Thứ tự hiển thị các trường trong trang chi tiết
    fields = (
        'lich_hen',
        'nguoi_gui',
        'noi_dung',
        'minh_chung',
        'yeu_cau',
        'phan_hoi',
        'trang_thai',
        'ngay_gui',
    )

    # Chỉ cho phép đọc một số trường (khách hàng, lịch hẹn, ngày gửi)
    readonly_fields = ('nguoi_gui', 'lich_hen', 'ngay_gui')

    # ======= Các hàm tuỳ chỉnh để hiển thị dữ liệu liên quan =======
    def get_thu_cung(self, obj):
        return obj.lich_hen.thu_cung.ten_thucung
    get_thu_cung.short_description = "Thú cưng"

    def get_dich_vu(self, obj):
        return ", ".join(
            [dv_lh.dich_vu.ten_dich_vu for dv_lh in obj.lich_hen.dv_lichhen_set.all()]
        ) or "Không có"
    get_dich_vu.short_description = "Dịch vụ"

    # Khi lưu phản hồi, tự cập nhật trạng thái
    def save_model(self, request, obj, form, change):
        if obj.phan_hoi and obj.trang_thai != 'Đã phản hồi':
            obj.trang_thai = 'Đã phản hồi'
        super().save_model(request, obj, form, change)


# 🌸 Cấu hình hiển thị cho model Đánh giá
@admin.register(DanhGia)
class DanhGiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nguoi_dung', 'lich_hen', 'diem', 'ngay_danh_gia')
    list_filter = ('diem',)
    search_fields = ('nguoi_dung__username', 'lich_hen__thu_cung__ten_thucung')
