from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Gán mặc định vai trò cho user nếu chưa có
@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created and not instance.role:
        instance.role = User.HOC_VIEN  # Hoặc vai trò mặc định khác nếu muốn
        instance.save()
