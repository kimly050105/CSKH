from django.shortcuts import render, get_object_or_404
from .models import DichVu

# 🌸 Hiển thị danh sách tất cả dịch vụ
def danh_sach_dich_vu(request):
    dich_vus = DichVu.objects.all().order_by('id')  # sắp xếp để dễ nhìn
    return render(request, 'DV/danhsachdichvu.html', {
        'dich_vus': dich_vus
    })


# 🌸 Hiển thị chi tiết từng dịch vụ
def chi_tiet_dich_vu(request, id):
    # Lấy dịch vụ theo ID, nếu không có thì báo lỗi 404
    dich_vu = get_object_or_404(DichVu, pk=id)
    return render(request, 'DV/chitietdichvu.html', {
        'dich_vu': dich_vu
    })
