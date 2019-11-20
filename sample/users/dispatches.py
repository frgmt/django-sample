from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django_mobile import set_flavour


# noinspection PyUnresolvedReferences
class RedirectLoggedInUser(object):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('my_page_default')

        return super(RedirectLoggedInUser, self).dispatch(request, *args, **kwargs)


# noinspection PyUnresolvedReferences
class RedirectAnonymousUser(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RedirectAnonymousUser, self).dispatch(request, *args, **kwargs)


# noinspection PyUnresolvedReferences
class RedirectNonPC(object):
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('preview') and self.request.GET.get('preview') in settings.FLAVOURS:
            set_flavour(self.request.GET.get('preview'), permanent=False)

        if self.request.flavour == settings.DEFAULT_MOBILE_FLAVOUR:
            return redirect('home')

        return super(RedirectNonPC, self).dispatch(request, *args, **kwargs)


# noinspection PyUnresolvedReferences
class RedirectNonSP(object):
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('preview') and self.request.GET.get('preview') in settings.FLAVOURS:
            set_flavour(self.request.GET.get('preview'), permanent=False)

        if self.request.flavour != settings.DEFAULT_MOBILE_FLAVOUR:
            return redirect('home')

        return super(RedirectNonSP, self).dispatch(request, *args, **kwargs)
