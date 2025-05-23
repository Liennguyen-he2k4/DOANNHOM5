from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('director-dashboard/', views.director_dashboard, name='director_dashboard'),
    path('assign-role/', views.admin_assign_role_view, name='assign_role'),
    path('manage-users/', views.admin_manage_users_view, name='manage_users'),
    path('attendance/', views.select_class_for_attendance, name='select_class_for_attendance'),
    path('attendance/<int:class_id>/', views.attendance_mark_view, name='attendance_mark'),
    path('class-list/', views.class_list_view, name='class_list'),
    path('class-register/', views.class_register_view, name='class_register'),
    path('enter-score/', views.select_class_for_score, name='select_class_for_score'),
    path('enter-score/<int:class_id>/', views.enter_score_view, name='enter_score'),
    path('make-payment/', views.make_payment_view, name='make_payment'),
    path('registered-classes/', views.registered_classes_view, name='registered_classes'),
    path('create-class/', views.staff_create_class_view, name='create_class'),
    path('manage-students/', views.staff_manage_students_view, name='manage_students'),
    path('manage-students/<int:class_id>/', views.staff_manage_students_view, name='manage_students'),
    path('view-scores/', views.view_scores_view, name='view_scores'),
]
