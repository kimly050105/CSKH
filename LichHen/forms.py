from django import forms
from .models import LichHen

class LichHenForm(forms.ModelForm):
    class Meta:
        model = LichHen
        fields = ['khach_hang', 'thu_cung', 'nhan_vien', 'thoi_gian', 'dich_vu', 'can_nang', 'ghi_chu', 'trang_thai']
        widgets = {
            'thoi_gian': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'ghi_chu': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'dich_vu': forms.TextInput(attrs={'class': 'form-control'}),
            'can_nang': forms.TextInput(attrs={'class': 'form-control'}),
        }
