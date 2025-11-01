from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DangKyForm, KhachHangForm, ThuCungForm
from .models import KhachHang, ThuCung
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def dangky(request):
    if request.method == 'POST':
        form = DangKyForm(request.POST)
        if form.is_valid():
            user = form.save()  # Tạo tài khoản user
            user.is_active=True
            # Gán vào nhóm Khách hàng
            khach_group, _ = Group.objects.get_or_create(name='Khách hàng')
            user.groups.add(khach_group)
            ho_ten = form.cleaned_data.get('ho_ten', user.username)
            # 👉 Tự động tạo bản ghi KhachHang
            KhachHang.objects.create(user=user, ho_ten=ho_ten, email=user.email,)
                # hoặc nếu form có field họ_tên thì thay user.username bằng form.cleaned_data['ho_ten']
            messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
            return redirect('dangnhap')
        else:
            messages.error(request, "Đăng ký thất bại, vui lòng kiểm tra lại.")
    else:
        form = DangKyForm()
    return render(request, 'TK/dang_ky.html', {'form': form})

def dangnhap(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')
            else:
               return redirect('home')
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu!")

    return render(request, 'TK/dang_nhap.html')


def quenmatkhau(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Mật khẩu đã được cập nhật thành công! Vui lòng đăng nhập lại.")
            return redirect('dangnhap')
        except User.DoesNotExist:
            messages.error(request, "Không tìm thấy tài khoản với email này.")

    return render(request, 'TK/quenmatkhau.html')

def dangxuat(request):
    logout(request)
    return redirect('home')

@login_required
def thongtintaikhoan(request):
    khach, created = KhachHang.objects.get_or_create(user=request.user)

    if not khach.ho_ten:
        khach.ho_ten = request.user.username
        khach.save()

    # 🔹 Nếu khách mới tạo hoặc chưa có email, tự gán email từ tài khoản user
    if not khach.email:
        khach.email = request.user.email
        khach.save()

    if request.method == 'POST':
        form = KhachHangForm(request.POST, instance=khach)
        if form.is_valid():
            kh = form.save(commit=False)
            # Nếu người dùng sửa email → cập nhật cả User.email luôn
            request.user.email = kh.email
            request.user.save()
            kh.save()
            messages.success(request, "Thông tin đã được cập nhật thành công!")
            return redirect('thongtintaikhoan')
    else:
        form = KhachHangForm(instance=khach)

    return render(request, 'TK/thongtintaikhoan.html', {
        'form': form,
        'user': request.user,
    })

@login_required
def xoa_tai_khoan(request):
    if request.method == 'POST':
        ly_do = request.POST.get('ly_do')
        user = request.user
        user.delete()
        messages.success(request, "Tài khoản của bạn đã được xóa thành công!")
        return redirect('dangxuat')  # đăng xuất sau khi khóa

    return render(request, 'TK/xoa_tai_khoan.html', {'user': request.user})
