from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    elif role == "quan_tri_vien":
        return render(request, "quan_tri_vien_dashboard.html")
    elif role == "giam_doc":
        return render(request, "giam_doc_dashboard.html")
    else:
        return render(request, "dashboard.html")  # fallback nếu không có role

# Các views dưới đây vẫn giữ lại, chỉ thêm login_required

@login_required
def admin_assign_role_view(request):
    return render(request, 'admin_assign_role.html')

@login_required
def admin_manage_users_view(request):
    return render(request, 'admin_manage_users.html')

@login_required
def attendance_mark_view(request):
    return render(request, 'attendance_mark.html')

@login_required
def class_list_view(request):
    return render(request, 'class_list.html')

@login_required
def class_register_view(request):
    return render(request, 'class_register.html')

@login_required
def enter_score_view(request):
    return render(request, 'enter_score.html')

@login_required
def make_payment_view(request):
    return render(request, 'make_payment.html')

@login_required
def registered_classes_view(request):
    return render(request, 'registered_classes.html')

@login_required
def staff_create_class_view(request):
    return render(request, 'staff_create_class.html')

@login_required
def staff_manage_students_view(request):
    return render(request, 'staff_manage_students.html')

@login_required
def view_scores_view(request):
    return render(request, 'view_scores.html')
