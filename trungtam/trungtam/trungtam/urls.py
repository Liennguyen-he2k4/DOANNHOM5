from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                        # Trang admin
    path('api/', include('core.urls')),                     # API chính
    path('api/auth/', include('rest_framework.urls')),      # API login (token hoặc session)
    
    # 👇 Thêm dòng này để dùng giao diện HTML
    path('', include('frontend.urls')),                     # Frontend giao diện người dùng
]
