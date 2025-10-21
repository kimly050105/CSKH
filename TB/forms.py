from django import forms
from .models import ThongBao

class ThongBaoForm(forms.ModelForm):
    class Meta:
        model = ThongBao
        fields = ['nguoi_nhan', 'tieu_de', 'noi_dung']
        widgets = {
            'tieu_de': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tiêu đề...'}),
            'noi_dung': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Nhập nội dung...'}),
            'nguoi_nhan': forms.Select(attrs={'class': 'form-control'}),
        }
