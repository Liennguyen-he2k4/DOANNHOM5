from django.db import models
from django.contrib.auth.models import AbstractUser

# -------------------------------
# Vai trò người dùng
# -------------------------------
class User(AbstractUser):
    ADMIN = 'admin'
    GIAO_VU = 'giao_vu'
    GIANG_VIEN = 'giang_vien'
    HOC_VIEN = 'hoc_vien'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (GIAO_VU, 'Giáo vụ'),
        (GIANG_VIEN, 'Giảng viên'),
        (HOC_VIEN, 'Học viên'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


# -------------------------------
# Lớp học
# -------------------------------
class LopHoc(models.Model):
    ten_lop = models.CharField(max_length=100)
    mo_ta = models.TextField(blank=True, null=True)
    giang_vien = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': User.GIANG_VIEN}
    )
    thoi_gian_bat_dau = models.DateField()
    thoi_gian_ket_thuc = models.DateField()

    def __str__(self):
        return self.ten_lop


# -------------------------------
# Đăng ký lớp học
# -------------------------------
class DangKy(models.Model):
    hoc_vien = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.HOC_VIEN}
    )
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    ngay_dang_ky = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hoc_vien', 'lop_hoc')

    def __str__(self):
        return f"{self.hoc_vien.username} đăng ký {self.lop_hoc.ten_lop}"


# -------------------------------
# Điểm danh
# -------------------------------
class DiemDanh(models.Model):
    hoc_vien = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.HOC_VIEN}
    )
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    ngay = models.DateField()
    trang_thai = models.BooleanField(default=False)  # True: Có mặt, False: Vắng

    class Meta:
        unique_together = ('hoc_vien', 'lop_hoc', 'ngay')

    def __str__(self):
        return f"{self.hoc_vien.username} - {self.ngay} - {'Có mặt' if self.trang_thai else 'Vắng'}"


# -------------------------------
# Nhập điểm
# -------------------------------
class Diem(models.Model):
    hoc_vien = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.HOC_VIEN}
    )
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    diem_so = models.FloatField()

    class Meta:
        unique_together = ('hoc_vien', 'lop_hoc')

    def __str__(self):
        return f"{self.hoc_vien.username} - {self.lop_hoc.ten_lop}: {self.diem_so}"


# -------------------------------
# Học phí
# -------------------------------
class HocPhi(models.Model):
    hoc_vien = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.HOC_VIEN}
    )
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    so_tien = models.PositiveIntegerField()
    ngay_thanh_toan = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.hoc_vien.username} - {self.lop_hoc.ten_lop}: {self.so_tien} VNĐ"
