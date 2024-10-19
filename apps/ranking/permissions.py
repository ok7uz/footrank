from django.core.exceptions import PermissionDenied


class StaffRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
