from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.messages import get_messages


from .models import LichHen, DV_LichHen
from .forms import LichHenForm
from TK.models import KhachHang, ThuCung


# 🧾 Hiển thị lịch hẹn sắp tới + nút thêm/sửa/xóa
@login_required(login_url='/dangnhap/')
def lich_hen_sap_toi(request):
    # ✅ Tìm chính xác KhachHang theo user đang đăng nhập
    khach_hang = KhachHang.objects.filter(user=request.user).first()

    # ⚠️ Nếu không tìm thấy khách hàng tương ứng, tránh lỗi None
    if not khach_hang:
        messages.error(request, "Tài khoản này chưa có thông tin khách hàng.")
        return render(request, 'lichhen/lich_hen_sap_toi.html', {'lich_hens': []})

    # ✅ Lọc tất cả lịch hẹn thuộc khách hàng đó, trạng thái 'sắp tới'
    lich_hens = LichHen.objects.filter(
        khach_hang_id=khach_hang.id,
        trang_thai='sap_toi'
    ).select_related('thu_cung', 'khach_hang').order_by('thoi_gian')

    return render(request, 'lichhen/lich_hen_sap_toi.html', {'lich_hens': lich_hens})


# ➕ Thêm lịch hẹn mới
@login_required(login_url='/dangnhap/')
def tao_lich_hen(request):
    # ✅ Xóa message cũ mỗi khi mở form
    storage = get_messages(request)
    storage.used = True

    user = request.user
    try:
        khach_hang = KhachHang.objects.get(user=user)
    except KhachHang.DoesNotExist:
        messages.error(request, "Tài khoản này chưa có thông tin khách hàng.")
        return redirect('home')

    if request.method == 'POST':
        form = LichHenForm(request.POST, khach_hang=khach_hang)
        if form.is_valid():
            thu_cung = form.cleaned_data.get('thu_cung')
            ten_moi = form.cleaned_data.get('ten_thu_cung_moi')

            # 🐶 Nếu người dùng thêm thú cưng mới
            if not thu_cung and ten_moi:
                thu_cung = ThuCung.objects.create(
                    khach_hang=khach_hang,
                    ten_thucung=ten_moi,
                    loai=form.cleaned_data.get('loai'),
                    tuoi=form.cleaned_data.get('tuoi'),
                    can_nang=form.cleaned_data.get('can_nang')
                )

            if not thu_cung:
                messages.error(request, "Vui lòng chọn hoặc thêm thú cưng hợp lệ.")
                return render(request, 'lichhen/tao_lich_hen.html', {'form': form})

            # ✅ Lưu lịch hẹn
            lich_hen = form.save(commit=False)
            lich_hen.khach_hang = khach_hang
            lich_hen.thu_cung = thu_cung
            lich_hen.trang_thai = 'sap_toi'
            lich_hen.so_dien_thoai = form.cleaned_data.get('so_dien_thoai')
            lich_hen.save()

            # ✅ Thêm nhiều dịch vụ
            dich_vu_list = form.cleaned_data.get('dich_vu', [])
            for dv in dich_vu_list:
                DV_LichHen.objects.create(lich_hen=lich_hen, dich_vu=dv)

            messages.success(request, "Thêm lịch hẹn thành công!")
            return redirect('lich_hen_sap_toi')
        else:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin hợp lệ.")
    else:
        so_dien_thoai_mac_dinh = getattr(khach_hang, 'so_dien_thoai', '')
        form = LichHenForm(khach_hang=khach_hang, initial={'so_dien_thoai': so_dien_thoai_mac_dinh})

    return render(request, 'lichhen/tao_lich_hen.html', {'form': form})
# 📘 API trả về thông tin thú cưng (AJAX)
def thong_tin_thu_cung(request, pk):
    try:
        thu_cung = ThuCung.objects.get(pk=pk)
        data = {
            'loai': thu_cung.loai,
            'tuoi': thu_cung.tuoi,
            'can_nang': thu_cung.can_nang,
        }
        return JsonResponse(data)
    except ThuCung.DoesNotExist:
        return JsonResponse({'error': 'Không tìm thấy thú cưng.'}, status=404)


# ✏️ Sửa lịch hẹn
@login_required(login_url='/dangnhap/')
def sua_lich_hen(request, id):
    lich_hen = get_object_or_404(LichHen, id=id)
    if request.method == 'POST':
        form = LichHenForm(request.POST, instance=lich_hen)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật lịch hẹn thành công!")
            return redirect('lich_hen_sap_toi')
    else:
        form = LichHenForm(instance=lich_hen)
    return render(request, 'lichhen/sua_lich_hen.html', {'form': form})


# 🗑️ Xóa lịch hẹn
@login_required(login_url='/dangnhap/')
def xoa_lich_hen(request, id):
    lich_hen = get_object_or_404(LichHen, id=id)
    if request.method == 'POST':
        lich_hen.delete()
        messages.success(request, "Đã xóa lịch hẹn thành công.")
        return redirect('lich_hen_sap_toi')
    return render(request, 'lichhen/xoa_lich_hen.html', {'lich_hen': lich_hen})


# 📘 Xem lịch sử lịch hẹn (hoàn thành)
@login_required(login_url='/dangnhap/')
def lich_su_lich_hen(request):
    khach_hang = KhachHang.objects.filter(user=request.user).first()
    lich_hens = LichHen.objects.filter(
        khach_hang=khach_hang,
        trang_thai='hoan_thanh'
    ).order_by('-thoi_gian')
    return render(request, 'lichhen/lich_su_lich_hen.html', {'lich_hens': lich_hens})


# ❌ Xem lịch hẹn đã hủy
@login_required(login_url='/dangnhap/')
def lich_da_huy(request):
    khach_hang = KhachHang.objects.filter(user=request.user).first()
    lich_hens = LichHen.objects.filter(
        khach_hang=khach_hang,
        trang_thai='huy'
    ).order_by('-thoi_gian')
    return render(request, 'lichhen/lich_da_huy.html', {'lich_hens': lich_hens})
