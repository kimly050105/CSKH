from django.shortcuts import render, get_object_or_404
from .models import DichVu
def danh_sach_dich_vu(request):
    dich_vus = DichVu.objects.all()
    return render(request, 'DV/danhsachdichvu.html', {'dich_vus': dich_vus})
def chi_tiet_dich_vu(request, dich_vu_id):
    dich_vu = get_object_or_404(DichVu, id=dich_vu_id)
    return render(request, 'DV/chitietdichvu.html', {'dich_vu': dich_vu})

# Create your views here.
