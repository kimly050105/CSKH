from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .models import TinNhan
from TK.models import KhachHang, NhanVien


# ====================== HIỂN THỊ CHATBOX ======================
def chat_view(request):
    """Hiển thị khung chat của khách hàng"""
    messages = []

    if request.user.is_authenticated:
        khachhang = KhachHang.objects.filter(user=request.user).first()
        if khachhang:
            messages = TinNhan.objects.filter(id_khachhang=khachhang).order_by('thoi_gian_gui')

    return render(request, 'trangchu/chatbox.html', {'messages': messages})



# ====================== GỬI TIN NHẮN ======================
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        content = request.POST.get("message", "").strip()
        print("📩 Nhận POST:", content)
        if not content:
            return JsonResponse({"success": False})

        # ✅ Xác định người gửi
        khachhang = nhanvien = admin = None
        nguoi_gui = "khachhang"

        if request.user.is_authenticated:
            khachhang = KhachHang.objects.filter(user=request.user).first()
            nhanvien = NhanVien.objects.filter(user=request.user).first()

            if request.user.is_superuser or request.user.is_staff:
                nguoi_gui = "admin"
                admin = request.user
            elif nhanvien:
                nguoi_gui = "nhanvien"
            elif khachhang:
                nguoi_gui = "khachhang"
        else:
            nguoi_gui = "khach_vang_lai"

        # ✅ Gắn session ID để phân biệt khách chưa đăng nhập
        session_id = request.session.session_key or request.session.create()
        print("🧩 Session ID:", session_id)

        # ✅ Lưu tin người gửi
        TinNhan.objects.create(
            id_khachhang=khachhang,
            id_nhanvien=nhanvien,
            id_admin=admin,
            nguoi_gui=nguoi_gui,
            noi_dung=content,
            thoi_gian_gui=timezone.now(),
        )

        # ✅ Tạo phản hồi bot
        reply = auto_reply(content)

        TinNhan.objects.create(
            id_khachhang=khachhang,
            nguoi_gui="bot",
            noi_dung=reply,
            thoi_gian_gui=timezone.now(),
        )

        return JsonResponse({"success": True, "reply": reply})

    return JsonResponse({"success": False, "error": "Phương thức không hợp lệ"})



# ====================== HÀM AUTO REPLY ======================
def auto_reply(message):
    """Tạo phản hồi tự động cho một số từ khóa cơ bản"""
    text = message.lower()
    if "nhuộm" in text or "nhuom" in text:
        return "🎨 Dịch vụ nhuộm lông có giá khoảng 300,000 VND. Màu nhuộm an toàn cho bé 💕"
    elif "tắm" in text or "tam" in text:
        return "🛁 Dịch vụ tắm rửa có giá khoảng 150,000 VND. Bao gồm sấy khô và chải lông 🌸"
    elif "cắt" in text or "tia" in text:
        return "🐩 Cắt tỉa lông có giá khoảng 200,000 VND. Dụng cụ an toàn, nhân viên tận tâm 💖"
    elif "tư vấn" in text or "sức khỏe" in text:
        return "💬 Vui lòng để lại câu hỏi của bạn, nhân viên sẽ phản hồi sớm nhất 💕"

    # Nếu không trùng từ khóa nào, chỉ gửi cảm ơn (một lần)
    return "💗Cảm ơn bạn đã liên hệ Punky Spa! Bạn vui lòng chờ một lát để nhân viên hỗ trợ nhé💗"


# ====================== LẤY LỊCH SỬ CHAT ======================
def get_history(request):
    """Trả danh sách tin nhắn của khách hiện tại (dù chưa đăng nhập)"""
    session_id = request.session.session_key or request.session.create()

    khachhang = None
    if request.user.is_authenticated:
        khachhang = KhachHang.objects.filter(user=request.user).first()

    # Nếu có tài khoản thì lọc theo id_khachhang, không thì tạm lấy tất cả tin bot+khách chưa có id
    if khachhang:
        messages = TinNhan.objects.filter(id_khachhang=khachhang).order_by('thoi_gian_gui')
    else:
        messages = TinNhan.objects.filter(id_khachhang__isnull=True).order_by('thoi_gian_gui')

    data = [
        {
            "nguoi_gui": m.nguoi_gui,
            "noi_dung": m.noi_dung,
            "thoi_gian": m.thoi_gian_gui.strftime("%H:%M:%S"),
        }
        for m in messages
    ]
    return JsonResponse({"success": True, "messages": data})



# ======================== QUẢN LÝ HỘI THOẠI ========================
@staff_member_required
def danh_sach_hoi_thoai(request):
    """Danh sách khách hàng có hội thoại"""
    hoi_thoai = (
        TinNhan.objects
        .filter(id_khachhang__isnull=False)
        .values('id_khachhang__id', 'id_khachhang__ho_ten')
        .distinct()
        .order_by('-thoi_gian_gui')
    )
    return render(request, 'chat/hoi_thoai_list.html', {'hoi_thoai': hoi_thoai})


@staff_member_required
def chi_tiet_hoi_thoai(request, khachhang_id):
    """Hiển thị chi tiết hội thoại của 1 khách"""
    khachhang = KhachHang.objects.get(pk=khachhang_id)
    messages = TinNhan.objects.filter(id_khachhang=khachhang).order_by('thoi_gian_gui')
    return render(request, 'chat/hoi_thoai_detail.html', {
        'khachhang': khachhang,
        'messages': messages,
    })


@staff_member_required
def gui_tin_admin(request, khachhang_id):
    """Nhân viên gửi tin nhắn phản hồi khách"""
    if request.method == "POST":
        noi_dung = request.POST.get("noi_dung", "").strip()
        khachhang = KhachHang.objects.get(pk=khachhang_id)
        nhanvien = NhanVien.objects.filter(user=request.user).first()

        if noi_dung:
            TinNhan.objects.create(
                id_khachhang=khachhang,
                id_nhanvien=nhanvien,
                nguoi_gui='nhanvien',
                noi_dung=noi_dung,
                thoi_gian_gui=timezone.now()
            )

    return redirect('chi_tiet_hoi_thoai', khachhang_id=khachhang_id)

@staff_member_required
def nhanvien_gui_tin(request, khachhang_id):
    """Nhân viên hoặc admin gửi tin nhắn trả lời khách"""
    if request.method == "POST":
        khachhang = KhachHang.objects.get(pk=khachhang_id)
        noi_dung = request.POST.get("noi_dung", "").strip()
        nhanvien = NhanVien.objects.filter(user=request.user).first()

        if noi_dung:
            if request.user.is_superuser:
                nguoi_gui = "admin"
            elif nhanvien:
                nguoi_gui = "nhanvien"
            else:
                nguoi_gui = "nhanvien"

            TinNhan.objects.create(
                id_khachhang=khachhang,
                id_nhanvien=nhanvien if nguoi_gui == "nhanvien" else None,
                id_admin=request.user if nguoi_gui == "admin" else None,
                nguoi_gui=nguoi_gui,
                noi_dung=noi_dung,
                thoi_gian_gui=timezone.now()
            )

    return redirect('chi_tiet_hoi_thoai', khachhang_id=khachhang_id)
