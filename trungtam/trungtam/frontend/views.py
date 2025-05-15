from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import LopHoc, DangKy, Diem, DiemDanh, User, HocPhi
from django.utils import timezone
from django.db.models import Sum
from datetime import date, datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import IntegrityError

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    role = getattr(request.user, "role", None)

    if role == "hoc_vien":
        return render(request, "hoc_vien_dashboard.html")
    elif role == "giang_vien":
        return render(request, "giang_vien_dashboard.html")
    elif role == "giao_vu":
        return render(request, "giao_vu_dashboard.html")
    elif role == "admin":
        return redirect("admin_dashboard")
    elif role == "giam_doc":
        return render(request, "giam_doc_dashboard.html")
    else:
        return render(request, "dashboard.html")  # fallback nếu không có role

# Các views dưới đây vẫn giữ lại, chỉ thêm login_required
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, "Bạn không có quyền truy cập trang quản trị viên.")
        return redirect('dashboard')

    stats = {
        'total_classes': LopHoc.objects.count(),
        'total_users': User.objects.count(),
        'admin_users': User.objects.filter(role='admin').count(),
        'staff_users': User.objects.filter(role='giao_vu').count(),
        'teacher_users': User.objects.filter(role='giang_vien').count(),
        'student_users': User.objects.filter(role='hoc_vien').count(),
        'director_users': User.objects.filter(role='giam_doc').count(),
    }

    return render(request, 'quan_tri_vien_dashboard.html', {
        'stats': stats
    })

@login_required
def admin_assign_role_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Bạn không có quyền phân quyền người dùng.")
        return redirect('dashboard')

    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role = request.POST.get('role')

        # Danh sách vai trò hợp lệ
        valid_roles = ['hoc_vien', 'giang_vien', 'giao_vu', 'admin', 'giam_doc']

        try:
            user = get_object_or_404(User, id=user_id)
            if role not in valid_roles:
                messages.error(request, "Vai trò không hợp lệ.")
            else:
                user.role = role
                user.save()
                messages.success(request, f"Đã cập nhật vai trò của {user.username} thành {role}.")
            return redirect('assign_role')
        except Exception as e:
            messages.error(request, f"Lỗi khi cập nhật vai trò: {str(e)}")

    return render(request, 'admin_assign_role.html', {
        'users': users
    })

@login_required
def admin_manage_users_view(request):
    if request.user.role != 'admin':
        messages.error(request, "Bạn không có quyền quản lý người dùng.")
        return redirect('dashboard')

    users = User.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        if action == 'delete':
            try:
                user = get_object_or_404(User, id=user_id)
                if user == request.user:
                    messages.error(request, "Bạn không thể xóa chính mình.")
                elif user.role == 'admin' and User.objects.filter(role='admin').count() == 1:
                    messages.error(request, "Không thể xóa quản trị viên cuối cùng.")
                else:
                    username = user.username
                    user.delete()
                    messages.success(request, f"Đã xóa người dùng {username} thành công.")
                return redirect('manage_users')
            except Exception as e:
                messages.error(request, f"Lỗi khi xóa người dùng: {str(e)}")

    return render(request, 'admin_manage_users.html', {
        'users': users
    })

@login_required
def select_class_for_attendance(request):
    # Lấy các lớp do giảng viên hiện tại dạy
    classes = LopHoc.objects.filter(giang_vien=request.user)
    return render(request, 'select_class_for_attendance.html', {'classes': classes})

@login_required
def attendance_mark_view(request, class_id):
    classroom = get_object_or_404(LopHoc, id=class_id)

    # Kiểm tra quyền
    if classroom.giang_vien != request.user:
        messages.error(request, "Bạn không có quyền điểm danh lớp học này.")
        return redirect('select_class_for_attendance')

    # Lấy danh sách học viên đã đăng ký
    students = User.objects.filter(
        role=User.HOC_VIEN,
        dangky__lop_hoc=classroom
    ).distinct()

    # Lấy trạng thái điểm danh hôm nay
    today = date.today()
    attendance_records = DiemDanh.objects.filter(
        lop_hoc=classroom,
        ngay=today
    ).select_related('hoc_vien')

    # Tạo dictionary để lưu trạng thái điểm danh
    attendance_status = {record.hoc_vien.id: record.trang_thai for record in attendance_records}

    if request.method == 'POST':
        print("POST data:", request.POST)  # Ghi log dữ liệu POST
        for student in students:
            is_present = f'present_{student.id}' in request.POST
            print(f"Cập nhật điểm danh cho {student.username}: {is_present}")  # Ghi log
            try:
                DiemDanh.objects.update_or_create(
                    hoc_vien=student,
                    lop_hoc=classroom,
                    ngay=today,
                    defaults={'trang_thai': is_present}
                )
            except Exception as e:
                print(f"Lỗi cơ sở dữ liệu cho {student.username}: {e}")  # Ghi log lỗi
                messages.error(request, f"Lỗi khi lưu điểm danh cho {student.username}: {str(e)}")
        messages.success(request, "Đã lưu điểm danh thành công!")
        return redirect('attendance_mark', class_id=class_id)

    return render(request, 'attendance_mark.html', {
        'classroom': classroom,
        'students': students,
        'attendance_status': attendance_status,
        'today': today,
    })

@login_required
def class_list_view(request):
    classes = LopHoc.objects.select_related('giang_vien').all()
    return render(request, 'class_list.html', {'classes': classes})

@login_required
def class_register_view(request):
    available_classes = LopHoc.objects.all()
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        lop = LopHoc.objects.get(id=class_id)
        DangKy.objects.create(hoc_vien=request.user, lop_hoc=lop)
        return redirect('registered_classes')  # Đường dẫn tùy bạn đặt

    return render(request, 'class_register.html', {'available_classes': available_classes})

@login_required
def select_class_for_score(request):
    classes = LopHoc.objects.filter(giang_vien=request.user)
    return render(request, 'select_class_for_score.html', {'classes': classes})

@login_required
def enter_score_view(request, class_id):
    classroom = get_object_or_404(LopHoc, id=class_id)

    # Kiểm tra quyền
    if classroom.giang_vien != request.user:
        messages.error(request, "Bạn không có quyền nhập điểm cho lớp học này.")
        return redirect('select_class_for_score')

    # Lấy danh sách học viên đã đăng ký
    students = User.objects.filter(
        role=User.HOC_VIEN,
        dangky__lop_hoc=classroom
    ).distinct()

    # Lấy điểm hiện tại
    scores = Diem.objects.filter(lop_hoc=classroom).select_related('hoc_vien')
    student_scores = [
        {
            'student': student,
            'score': next((s.diem_so for s in scores if s.hoc_vien == student), None)
        }
        for student in students
    ]

    if request.method == 'POST':
        print("POST data:", request.POST)  # Ghi log dữ liệu POST
        for student in students:
            score_key = f'score_{student.id}'
            if score_key in request.POST:
                try:
                    score_value = float(request.POST[score_key])
                    if not 0 <= score_value <= 100:
                        raise ValueError("Điểm phải từ 0 đến 10.")
                    print(f"Cập nhật điểm cho {student.username}: {score_value}")  # Ghi log
                    Diem.objects.update_or_create(
                        hoc_vien=student,
                        lop_hoc=classroom,
                        defaults={'diem_so': score_value}
                    )
                except ValueError as e:
                    print(f"Lỗi điểm cho {student.username}: {e}")  # Ghi log lỗi
                    messages.error(request, f"Điểm của {student.username} không hợp lệ: {str(e)}")
                    continue
                except Exception as e:
                    print(f"Lỗi cơ sở dữ liệu cho {student.username}: {e}")  # Ghi log lỗi
                    messages.error(request, f"Lỗi khi lưu điểm cho {student.username}: {str(e)}")
        messages.success(request, "Đã lưu điểm thành công!")
        return redirect('enter_score', class_id=class_id)

    return render(request, 'enter_score.html', {
        'classroom': classroom,
        'student_scores': student_scores,
    })

@login_required
def make_payment_view(request):
    if request.method == 'POST':
        fee_id = request.POST.get('fee_id')
        try:
            fee = HocPhi.objects.get(id=fee_id, hoc_vien=request.user)
            fee.ngay_thanh_toan = timezone.now()
            fee.save()
        except HocPhi.DoesNotExist:
            pass
        return redirect('make_payment')

    fees = HocPhi.objects.filter(hoc_vien=request.user)
    return render(request, 'make_payment.html', {'fees': fees})
@login_required
def registered_classes_view(request):
    user = request.user
    registrations = DangKy.objects.filter(hoc_vien=user)
    return render(request, 'registered_classes.html', {
        'registrations': registrations
    })

@login_required
def staff_create_class_view(request):
    # Kiểm tra quyền giáo vụ
    if request.user.role != 'giao_vu':
        messages.error(request, "Bạn không có quyền tạo lớp học.")
        return redirect('dashboard')

    # Lấy danh sách giảng viên
    teachers = User.objects.filter(role='giang_vien')

    if request.method == 'POST':
        print("POST data:", request.POST)  # Ghi log dữ liệu POST
        ten_lop = request.POST.get('ten_lop')
        mo_ta = request.POST.get('mo_ta')  # Lấy mô tả
        giang_vien_id = request.POST.get('giang_vien_id')
        thoi_gian_bat_dau = request.POST.get('thoi_gian_bat_dau')
        thoi_gian_ket_thuc = request.POST.get('thoi_gian_ket_thuc')

        try:
            # Kiểm tra ngày hợp lệ
            start_date = datetime.strptime(thoi_gian_bat_dau, '%Y-%m-%d').date()
            end_date = datetime.strptime(thoi_gian_ket_thuc, '%Y-%m-%d').date()
            if end_date < start_date:
                messages.error(request, "Ngày kết thúc phải sau ngày bắt đầu.")
                return render(request, 'staff_create_class.html', {'teachers': teachers})

            giang_vien = User.objects.get(id=giang_vien_id, role='giang_vien')
            print(f"Tạo lớp: ten_lop={ten_lop}, mo_ta={mo_ta}, giang_vien={giang_vien.username}, start={thoi_gian_bat_dau}, end={thoi_gian_ket_thuc}")  # Ghi log
            LopHoc.objects.create(
                ten_lop=ten_lop,
                mo_ta=mo_ta or None,  # Lưu None nếu mo_ta rỗng
                giang_vien=giang_vien,
                thoi_gian_bat_dau=thoi_gian_bat_dau,
                thoi_gian_ket_thuc=thoi_gian_ket_thuc
            )
            messages.success(request, f"Lớp học '{ten_lop}' đã được tạo thành công!")
            return redirect('create_class')
        except User.DoesNotExist:
            print("Lỗi: Giảng viên không hợp lệ, giang_vien_id=", giang_vien_id)  # Ghi log
            messages.error(request, "Giảng viên không hợp lệ.")
        except ValueError as e:
            print(f"Lỗi định dạng ngày: {e}")  # Ghi log
            messages.error(request, "Định dạng ngày không hợp lệ. Vui lòng chọn ngày đúng định dạng.")
        except IntegrityError as e:
            print(f"Lỗi trùng khóa chính: {e}")  # Ghi log
            messages.error(request, "Lỗi: Không thể tạo lớp do trùng khóa chính. Vui lòng thử lại hoặc liên hệ quản trị viên.")
        except Exception as e:
            print(f"Lỗi khác khi tạo lớp: {e}")  # Ghi log
            messages.error(request, f"Lỗi khi tạo lớp: {str(e)}")

    return render(request, 'staff_create_class.html', {
        'teachers': teachers
    })

@login_required
def staff_manage_students_view(request, class_id=None):
    # Kiểm tra quyền giáo vụ
    if request.user.role != 'giao_vu':
        messages.error(request, "Bạn không có quyền quản lý học viên.")
        return redirect('dashboard')

    # Lấy danh sách tất cả lớp học
    classes = LopHoc.objects.all()

    # Xử lý class_id từ URL hoặc GET
    selected_class_id = class_id or request.GET.get('class_id')
    classroom = None
    students = []
    classroom_students = []

    if selected_class_id:
        try:
            classroom = get_object_or_404(LopHoc, id=selected_class_id)
            # Lấy học viên đã đăng ký lớp
            classroom_students = User.objects.filter(
                role='hoc_vien',
                dangky__lop_hoc=classroom
            ).distinct()
            # Lấy học viên chưa đăng ký lớp
            students = User.objects.filter(
                role='hoc_vien'
            ).exclude(
                dangky__lop_hoc=classroom
            ).distinct()
        except LopHoc.DoesNotExist:
            messages.error(request, "Lớp học không tồn tại.")
            return redirect('manage_students')

    if request.method == 'POST':
        action = request.POST.get('action')
        class_id = request.POST.get('class_id')
        student_id = request.POST.get('student_id')

        try:
            classroom = get_object_or_404(LopHoc, id=class_id)
            student = get_object_or_404(User, id=student_id, role='hoc_vien')

            if action == 'add':
                DangKy.objects.create(hoc_vien=student, lop_hoc=classroom)
                messages.success(request, f"Đã thêm học viên {student.username} vào lớp {classroom.ten_lop}.")
            elif action == 'remove':
                DangKy.objects.filter(hoc_vien=student, lop_hoc=classroom).delete()
                messages.success(request, f"Đã xóa học viên {student.username} khỏi lớp {classroom.ten_lop}.")
            else:
                messages.error(request, "Hành động không hợp lệ.")
            return redirect('manage_students', class_id=class_id)
        except Exception as e:
            messages.error(request, f"Lỗi: {str(e)}")

    return render(request, 'staff_manage_students.html', {
        'classes': classes,
        'classroom': classroom,
        'students': students,
        'classroom_students': classroom_students,
        'selected_class_id': selected_class_id
    })

@login_required
def view_scores_view(request):
    scores = Diem.objects.filter(hoc_vien=request.user)
    return render(request, 'view_scores.html', {'scores': scores})

@login_required
def director_dashboard(request):
    if request.user.role != User.GIAM_DOC:
        return render(request, 'unauthorized.html')  # tuỳ bạn xử lý nếu không phải giám đốc

    stats = {
        'total_classes': LopHoc.objects.count(),
        'total_students': User.objects.filter(role=User.HOC_VIEN).count(),
        'total_teachers': User.objects.filter(role=User.GIANG_VIEN).count(),
        'total_revenue': HocPhi.objects.aggregate(total=Sum('so_tien'))['total'] or 0
    }

    return render(request, 'director_dashboard.html', {'stats': stats})
