from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

#custom mixin
class OroganizorRequiredMixin(AccessMixin):
    """Verify that the current user is authenticcated and organizor."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizor :#.user is the instance of our current user (User)
            return redirect('leads:list')#to the lead page
        return super().dispatch(request, *args, **kwargs)
