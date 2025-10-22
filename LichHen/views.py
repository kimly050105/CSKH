from django.shortcuts import render, redirect, get_object_or_404
from .models import LichHen,DV_LichHen
from .forms import LichHenForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 🧾 Hiển thị lịch hẹn sắp tới + nút thêm/sửa/xóa
def lich_hen_sap_toi(request):
    lich_hens = LichHen.objects.filter(trang_thai='sap_toi').order_by('thoi_gian')
    return render(request, 'lichhen/lich_hen_sap_toi.html', {'lich_hens': lich_hens})

# ➕ Thêm lịch hẹn mới
@login_required
def tao_lich_hen(request):
    khach_hang = request.user.khachhang  # ✅ Lấy khách hàng hiện tại

    if request.method == 'POST':
        form = LichHenForm(request.POST, khach_hang=khach_hang)

        if form.is_valid():
            # ✅ Lưu lịch hẹn vào DB
            lich_hen = form.save(commit=False)
            lich_hen.khach_hang = khach_hang
            lich_hen.trang_thai = 'sap_toi'
            lich_hen.save()

            # ✅ Lưu các dịch vụ đã chọn
            for dv in form.cleaned_data['dich_vu']:
                DV_LichHen.objects.create(lich_hen=lich_hen, dich_vu=dv)

            # ✅ Thông báo thành công
            messages.success(request, "🎉 Lịch hẹn của bạn đã được tạo thành công!")
            return redirect('lich_hen_sap_toi')  # 👉 chuyển sang trang lịch hẹn sắp tới
        else:
            # ✅ Nếu form thiếu dữ liệu -> thông báo lỗi
            messages.error(request, "⚠️ Vui lòng điền đầy đủ thông tin trước khi lưu!")
    else:
        form = LichHenForm(khach_hang=khach_hang)

    return render(request, 'lichhen/tao_lich_hen.html', {'form': form})



# ✏️ Sửa lịch hẹn
def sua_lich_hen(request, id):
    lich_hen = get_object_or_404(LichHen, id=id)
    if request.method == 'POST':
        form = LichHenForm(request.POST, instance=lich_hen)
        if form.is_valid():
            form.save()
            return redirect('lich_hen_sap_toi')
    else:
        form = LichHenForm(instance=lich_hen)
    return render(request, 'lichhen/sua_lich_hen.html', {'form': form})

# 🗑️ Xóa lịch hẹn
def xoa_lich_hen(request, id):
    lich_hen = get_object_or_404(LichHen, id=id)
    if request.method == 'POST':
        lich_hen.delete()
        return redirect('lich_hen_sap_toi')
    return render(request, 'lichhen/xoa_lich_hen.html', {'lich_hen': lich_hen})
# 📘 Xem lịch sử lịch hẹn (hoàn thành)
def lich_su_lich_hen(request):
    lich_hens = LichHen.objects.filter(trang_thai='hoan_thanh').order_by('-thoi_gian')
    return render(request, 'lichhen/lich_su_lich_hen.html', {'lich_hens': lich_hens})


# ❌ Xem lịch hẹn đã hủy
def lich_da_huy(request):
    lich_hens = LichHen.objects.filter(trang_thai='huy').order_by('-thoi_gian')
    return render(request, 'lichhen/lich_da_huy.html', {'lich_hens': lich_hens})
# Create your views here.
