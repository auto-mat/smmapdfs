from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .models import PdfSandwichType
from . import email
from . import tasks


def _make_pdfsandwich_(modeladmin, request, queryset, continuation=None):
    for obj in queryset:
        content_type = ContentType.objects.get_for_model(obj)
        if settings.SMMAPDFS_CELERY:
            f = tasks.make_pdfsandwich.delay
        else:
            f = tasks.make_pdfsandwich
        f(
            content_type.app_label, content_type.model, obj.pk, continuation,
        )


def make_pdfsandwich(modeladmin, request, queryset):
    _make_pdfsandwich_(modeladmin, request, queryset)


make_pdfsandwich.short_description = _("Make PDF Sandwich")


def make_and_send_pdfsandwich(modeladmin, request, queryset):
    base_url = email.get_base_url(request)

    def continuation(sandwich):
        email.send_pdfsandwich(sandwich, base_url)

    _make_pdfsandwich_(modeladmin, request, queryset, continuation)


make_and_send_pdfsandwich.short_description = _("Make and send PDF Sandwich")


def send_pdfsandwich(modeladmin, request, queryset):
    base_url = email.get_base_url(request)
    for sandwich in queryset:
        content_type = ContentType.objects.get_for_model(sandwich)
        if settings.SMMAPDFS_CELERY:
            f = tasks.send_pdfsandwich.delay
        else:
            f = tasks.send_pdfsandwich
        f(content_type.app_label, content_type.model, sandwich.pk, base_url)


send_pdfsandwich.short_description = _("Send PDF Sandwich")
