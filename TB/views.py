from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import ThongBao
from .forms import ThongBaoForm

# Kiểm tra quyền nhân viên
def la_nhan_vien(user):
    return user.is_staff or user.is_superuser

# 1️⃣ Khách hàng xem danh sách thông báo
@login_required
def danh_sach_thong_bao(request):
    thongbaos = ThongBao.objects.filter(nguoi_nhan=request.user).order_by('-ngay_tao')
    return render(request, 'TB/danh_sach_thong_bao.html', {'thongbaos': thongbaos})

# 2️⃣ Chi tiết thông báo
@login_required
def chi_tiet_thong_bao(request, id):
    tb = get_object_or_404(ThongBao, id=id, nguoi_nhan=request.user)
    tb.da_doc = True
    tb.save()
    return render(request, 'TB/chi_tiet.html', {'tb': tb})

# 3️⃣ Nhân viên tạo thông báo
@login_required
@user_passes_test(la_nhan_vien)
def tao_thong_bao(request):
    if request.method == 'POST':
        form = ThongBaoForm(request.POST)
        if form.is_valid():
            tb = form.save(commit=False)
            tb.nguoi_gui = request.user
            tb.save()
            return redirect('danh_sach_thong_bao')
    else:
        form = ThongBaoForm()
    return render(request, 'TB/tao_thong_bao.html', {'form': form})
