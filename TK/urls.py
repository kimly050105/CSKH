from django.urls import path
from .import views
urlpatterns = [
    path('dangky/', views.dangky, name='dangky'),
    path('dangnhap/', views.dangnhap, name='dangnhap'),
    path('quenmatkhau/', views.quenmatkhau, name='quenmatkhau'),
]