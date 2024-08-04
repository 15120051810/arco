from rest_framework.permissions import BasePermission

from users.models import Api


class APIPermission(BasePermission):
    """
    自定义接口权限
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        path = request.path
        apis = Api.objects.filter(routers__roles__role_users=request.user).values_list('abs_path', flat=True)
        apis = set(apis)
        apis = {*apis}
        for api in apis:
            if api in path:
                return True
        else:
            return False
