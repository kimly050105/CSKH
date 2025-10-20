from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DangKyForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def dangky(request):
    if request.method == 'POST':
        form = DangKyForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('trangchu')
        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu!")

    return render(request, 'TK/dang_nhap.html')


def quenmatkhau(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('mat_khau_moi')
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Mật khẩu đã được cập nhật thành công! Vui lòng đăng nhập lại.")
            return redirect('dangnhap')
        except User.DoesNotExist:
            messages.error(request, "Không tìm thấy tài khoản với email này.")

    return render(request, 'TK/quenmatkhau.html')



# Create your views here.
