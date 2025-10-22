
from django.shortcuts import render, redirect, get_object_or_404
from .models import LichHen
from .forms import LichHenForm

# 🧾 Hiển thị lịch hẹn sắp tới + nút thêm/sửa/xóa
def lich_hen_sap_toi(request):
    lich_hens = LichHen.objects.filter(trang_thai='sap_toi').order_by('thoi_gian')
    return render(request, 'lichhen/lich_hen_sap_toi.html', {'lich_hens': lich_hens})

# ➕ Thêm lịch hẹn mới
def them_lich_hen(request):
    if request.method == 'POST':
        form = LichHenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lich_hen_sap_toi')
    else:
        form = LichHenForm()
    return render(request, 'lichhen/them_lich_hen.html', {'form': form})

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
