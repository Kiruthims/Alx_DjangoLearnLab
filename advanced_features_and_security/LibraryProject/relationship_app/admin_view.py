from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Hello Admin, welcome to the admin view.")
