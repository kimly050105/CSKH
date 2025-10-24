from django.urls import path
from .import views
urlpatterns = [
    path('dangky/', views.dangky, name='dangky'),
    path('dangnhap/', views.dangnhap, name='dangnhap'),
    path('quenmatkhau/', views.quenmatkhau, name='quenmatkhau'),
    path('dangxuat/', views.dangxuat, name='dangxuat'),
    path('thongtintaikhoan/', views.thongtintaikhoan, name='thongtintaikhoan'),
    path('thongtinthucung/', views.thongtinthucung, name='thongtinthucung'),
    path('xoa_tai_khoan/', views.xoa_tai_khoan, name='xoa_tai_khoan'),

]
