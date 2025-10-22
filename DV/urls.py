from django.urls import path
from . import views

urlpatterns = [
    path('', views.danh_sach_dich_vu, name='danh_sach_dich_vu'),         # Trang danh sách
    path('<int:dich_vu_id>/', views.chi_tiet_dich_vu, name='chi_tiet_dich_vu'),  # Trang chi tiết
]
