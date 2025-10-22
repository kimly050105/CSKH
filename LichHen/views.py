from django.shortcuts import render, redirect, get_object_or_404
from .models import LichHen,DV_LichHen
from .forms import LichHenForm
from django.contrib.auth.decorators import login_required

# 🧾 Hiển thị lịch hẹn sắp tới + nút thêm/sửa/xóa
def lich_hen_sap_toi(request):
    lich_hens = LichHen.objects.filter(trang_thai='sap_toi').order_by('thoi_gian')
    return render(request, 'lichhen/lich_hen_sap_toi.html', {'lich_hens': lich_hens})

# ➕ Thêm lịch hẹn mới
@login_required
def tao_lich_hen(request):
    # ✅ Lấy thông tin khách hàng hiện tại (dựa trên tài khoản đăng nhập)
    khach_hang = request.user.khachhang

    if request.method == 'POST':
        # ✅ Truyền tham số 'khach_hang' vào form để lọc thú cưng
        form = LichHenForm(request.POST, khach_hang=khach_hang)

        # ✅ Kiểm tra dữ liệu form hợp lệ
        if form.is_valid():
            # 🧩 Tạo đối tượng Lịch hẹn nhưng chưa lưu (commit=False)
            lich_hen = form.save(commit=False)
            lich_hen.khach_hang = khach_hang  # gán khách hàng hiện tại
            lich_hen.trang_thai = 'sap_toi'   # trạng thái mặc định
            lich_hen.save()  # Lưu vào DB

            # 🧾 Lưu các dịch vụ được chọn vào bảng trung gian DV_LichHen
            for dv in form.cleaned_data['dich_vu']:
                DV_LichHen.objects.create(
                    lich_hen=lich_hen,   # khóa ngoại đến lịch hẹn
                    dich_vu=dv,          # khóa ngoại đến dịch vụ
                )

            # ✅ Sau khi tạo thành công, chuyển về trang danh sách lịch hẹn sắp tới
            return redirect('lich_hen_sap_toi')

    else:
        # 🧠 Nếu request là GET (truy cập form lần đầu), khởi tạo form trống
        form = LichHenForm(khach_hang=khach_hang)

    # 🪄 Render giao diện thêm lịch hẹn
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
