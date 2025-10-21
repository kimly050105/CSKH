from .models import ThongBao

def thong_bao_moi(request):
    thong_baos_moi = []
    if request.user.is_authenticated:
        thong_baos_moi = ThongBao.objects.filter(
            nguoi_nhan=request.user, da_doc=False
        ).order_by('-ngay_tao')[:5]
    return {'thong_baos_moi': thong_baos_moi}

