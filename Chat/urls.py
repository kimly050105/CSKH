from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('send/', views.send_message, name='send_message'),
    path('history/', views.get_history, name='get_history'),
# # 💼 Trang quản lý CSKH
    path('quanly/', views.danh_sach_hoi_thoai, name='danh_sach_hoi_thoai'),
    path('quanly/<int:khachhang_id>/', views.chi_tiet_hoi_thoai, name='chi_tiet_hoi_thoai'),
    path('quanly/gui/<int:khachhang_id>/', views.nhanvien_gui_tin, name='nhanvien_gui_tin'),

]

