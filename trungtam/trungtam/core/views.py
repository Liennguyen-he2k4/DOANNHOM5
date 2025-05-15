from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, LopHoc, DangKy, DiemDanh, Diem, HocPhi
from .serializers import (
    UserSerializer,
    LopHocSerializer,
    DangKySerializer, DangKyCreateSerializer,
    DiemDanhSerializer, DiemDanhCreateSerializer,
    DiemSerializer, DiemCreateSerializer,
    HocPhiSerializer, HocPhiCreateSerializer
)

# -------------------------------
# User View (Danh sách hoặc chi tiết user)
# -------------------------------

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------------
# Lớp học
# -------------------------------

class LopHocViewSet(viewsets.ModelViewSet):
    queryset = LopHoc.objects.all()
    serializer_class = LopHocSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Giảng viên tạo lớp học
        serializer.save(giang_vien=self.request.user)


# -------------------------------
# Đăng ký lớp học
# -------------------------------

class DangKyListView(generics.ListAPIView):
    serializer_class = DangKySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DangKy.objects.filter(hoc_vien=self.request.user)

class DangKyCreateView(generics.CreateAPIView):
    serializer_class = DangKyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(hoc_vien=self.request.user)


# -------------------------------
# Điểm danh
# -------------------------------

class DiemDanhListView(generics.ListAPIView):
    serializer_class = DiemDanhSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'hoc_vien':
            return DiemDanh.objects.filter(hoc_vien=user)
        elif user.role == 'giang_vien':
            return DiemDanh.objects.filter(lop_hoc__giang_vien=user)
        return DiemDanh.objects.none()

class DiemDanhCreateView(generics.CreateAPIView):
    serializer_class = DiemDanhCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------------
# Nhập điểm
# -------------------------------

class DiemListView(generics.ListAPIView):
    serializer_class = DiemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'hoc_vien':
            return Diem.objects.filter(hoc_vien=user)
        elif user.role == 'giang_vien':
            return Diem.objects.filter(lop_hoc__giang_vien=user)
        return Diem.objects.none()

class DiemCreateView(generics.CreateAPIView):
    serializer_class = DiemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------------
# Học phí
# -------------------------------

class HocPhiListView(generics.ListAPIView):
    serializer_class = HocPhiSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'hoc_vien':
            return HocPhi.objects.filter(hoc_vien=user)
        elif user.role in ['admin', 'giao_vu']:
            return HocPhi.objects.all()
        return HocPhi.objects.none()

class HocPhiCreateView(generics.CreateAPIView):
    serializer_class = HocPhiCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(hoc_vien=self.request.user)
