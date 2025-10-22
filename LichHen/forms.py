from django import forms
from .models import LichHen
from DV.models import DichVu
from TK.models import ThuCung  # ✅ import model thú cưng


class LichHenForm(forms.ModelForm):
    dich_vu = forms.ModelMultipleChoiceField(
        queryset=DichVu.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Dịch vụ",
        required=True  # ✅ bắt buộc chọn ít nhất 1 dịch vụ
    )

    thoi_gian = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Thời gian hẹn",
        required=True  # ✅ bắt buộc nhập thời gian
    )

    # Chọn 1 hoặc nhiều thú cưng thuộc khách hàng hiện tại
    thu_cung = forms.ModelMultipleChoiceField(
        queryset=ThuCung.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Thú cưng",
        required=True  # ✅ bắt buộc nhập thời gian
    )

    class Meta:
        model = LichHen
        fields = ['thu_cung', 'dich_vu', 'thoi_gian', 'ghi_chu']
        labels = {
            'thu_cung': 'Chọn thú cưng',
            'ghi_chu': 'Ghi chú thêm'
        }

    def __init__(self, *args, **kwargs):
        # ✅ Lấy ra giá trị 'khach_hang' được truyền từ view (nếu có)
        #   pop() ở đây sẽ đồng thời "lấy ra" và "xóa" tham số này khỏi kwargs,
        #   để tránh Django ném lỗi “unexpected keyword argument”.
        khach_hang = kwargs.pop('khach_hang', None)

        # ✅ Gọi hàm __init__ gốc của lớp cha (ModelForm)
        #   để Django khởi tạo bình thường tất cả các field trong form.
        super().__init__(*args, **kwargs)

        # ✅ Nếu có khách hàng được truyền vào (không phải None),
        #   thì ta lọc danh sách thú cưng chỉ thuộc khách hàng đó.
        if khach_hang:
            self.fields['thu_cung'].queryset = ThuCung.objects.filter(khach_hang=khach_hang)

