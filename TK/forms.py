from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import KhachHang

class DangKyForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được sử dụng.")
        return email

class KhachHangForm(forms.ModelForm):
    class Meta:
        model = KhachHang
        fields = ['ho_ten', 'gioi_tinh', 'so_dien_thoai', 'ngay_sinh', 'dia_chi', 'email']
        widgets = {
            'ngay_sinh': forms.DateInput(attrs={'type': 'date'}),
        }

