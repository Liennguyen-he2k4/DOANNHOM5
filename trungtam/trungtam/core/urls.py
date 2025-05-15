from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserListView,
    LopHocViewSet,
    DangKyListView, DangKyCreateView,
    DiemDanhListView, DiemDanhCreateView,
    DiemListView, DiemCreateView,
    HocPhiListView, HocPhiCreateView,
)

router = DefaultRouter()
router.register(r'lop-hoc', LopHocViewSet, basename='lop-hoc')

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),

    # Lớp học (qua router)
    path('', include(router.urls)),

    # Đăng ký lớp học
    path('dang-ky/', DangKyCreateView.as_view(), name='dang-ky-create'),
    path('dang-ky/danh-sach/', DangKyListView.as_view(), name='dang-ky-list'),

    # Điểm danh
    path('diem-danh/', DiemDanhCreateView.as_view(), name='diem-danh-create'),
    path('diem-danh/danh-sach/', DiemDanhListView.as_view(), name='diem-danh-list'),

    # Nhập điểm
    path('diem/', DiemCreateView.as_view(), name='diem-create'),
    path('diem/danh-sach/', DiemListView.as_view(), name='diem-list'),

    # Học phí
    path('hoc-phi/', HocPhiCreateView.as_view(), name='hoc-phi-create'),
    path('hoc-phi/danh-sach/', HocPhiListView.as_view(), name='hoc-phi-list'),
]
