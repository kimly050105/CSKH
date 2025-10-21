from django import forms
from .models import LichHen

class DatLichForm(forms.ModelForm):
    class Meta:
        model = LichHen
        fields = [
            'khach_hang', 'thu_cung', 'so_dien_thoai', 'can_nang',
            'dich_vu', 'nhan_vien', 'thoi_gian', 'ghi_chu'
        ]

        widgets = {
            'thoi_gian': forms.DateTimeInput(  # ô chọn ngày + giờ
                attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Chọn ngày và giờ hẹn'}
            ),
            'so_dien_thoai': forms.TextInput(  # nhập số điện thoại khách
                attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}
            ),
            'can_nang': forms.TextInput(  # nhập cân nặng thú cưng
                attrs={'class': 'form-control', 'placeholder': 'VD: 2 kg'}
            ),
            'ghi_chu': forms.Textarea(  # ghi chú nhiều dòng
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Ghi chú thêm...'}
            ),
            'khach_hang': forms.Select(attrs={'class': 'form-select'}),  # dropdown chọn khách hàng
            'thu_cung': forms.Select(attrs={'class': 'form-select'}),    # dropdown chọn thú cưng
            'dich_vu': forms.Select(attrs={'class': 'form-select'}),     # dropdown chọn dịch vụ
            'nhan_vien': forms.Select(attrs={'class': 'form-select'}),   # dropdown chọn nhân viên
        }
