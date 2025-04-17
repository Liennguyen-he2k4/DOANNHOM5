from rest_framework import serializers
from .models import User, LopHoc, DangKy, DiemDanh, Diem, HocPhi

# -------------------------------
# User Serializer (dùng cho tất cả roles)
# -------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

# -------------------------------
# Lớp học
# -------------------------------

class LopHocSerializer(serializers.ModelSerializer):
    giang_vien = UserSerializer(read_only=True)

    class Meta:
        model = LopHoc
        fields = ['id', 'ten_lop', 'mo_ta', 'giang_vien', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc']

# -------------------------------
# Đăng ký lớp học
# -------------------------------

class DangKySerializer(serializers.ModelSerializer):
    hoc_vien = UserSerializer(read_only=True)
    lop_hoc = LopHocSerializer(read_only=True)

    class Meta:
        model = DangKy
        fields = ['id', 'hoc_vien', 'lop_hoc', 'ngay_dang_ky']

# Dùng khi POST đăng ký lớp (chỉ cần ID)
class DangKyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DangKy
        fields = ['hoc_vien', 'lop_hoc']

# -------------------------------
# Điểm danh
# -------------------------------

class DiemDanhSerializer(serializers.ModelSerializer):
    hoc_vien = UserSerializer(read_only=True)
    lop_hoc = LopHocSerializer(read_only=True)

    class Meta:
        model = DiemDanh
        fields = ['id', 'hoc_vien', 'lop_hoc', 'ngay', 'trang_thai']

class DiemDanhCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiemDanh
        fields = ['hoc_vien', 'lop_hoc', 'ngay', 'trang_thai']

# -------------------------------
# Điểm học viên
# -------------------------------

class DiemSerializer(serializers.ModelSerializer):
    hoc_vien = UserSerializer(read_only=True)
    lop_hoc = LopHocSerializer(read_only=True)

    class Meta:
        model = Diem
        fields = ['id', 'hoc_vien', 'lop_hoc', 'diem_so']

class DiemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diem
        fields = ['hoc_vien', 'lop_hoc', 'diem_so']

# -------------------------------
# Học phí
# -------------------------------

class HocPhiSerializer(serializers.ModelSerializer):
    hoc_vien = UserSerializer(read_only=True)
    lop_hoc = LopHocSerializer(read_only=True)

    class Meta:
        model = HocPhi
        fields = ['id', 'hoc_vien', 'lop_hoc', 'so_tien', 'ngay_thanh_toan']

class HocPhiCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HocPhi
        fields = ['hoc_vien', 'lop_hoc', 'so_tien']
