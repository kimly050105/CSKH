from django.urls import path
from . import views

urlpatterns = [
    path('', views.danh_sach_thong_bao, name='danh_sach_thong_bao'),
    path('<int:id>/', views.chi_tiet_thong_bao, name='chi_tiet_thong_bao'),
    path('tao/', views.tao_thong_bao, name='tao_thong_bao'),
]
