from celery import task

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .models import PdfSandwichType
from . import email

def make_pdfsandwich(modeladmin, request, queryset):
    for obj in queryset:
        content_type = ContentType.objects.get_for_model(obj)
        if settings.SMMAPDFS_CELERY:
            f = make_pdfsandwich_task.delay
        else:
            f = make_pdfsandwich_task
        f(
            content_type.app_label,
            content_type.model,
            obj.pk,
        )

make_pdfsandwich.short_description = _("Make PDF Sandwich")

@task()
def make_pdfsandwich_task(app_label, obj_model, obj_pk):
    try:
        object_model = ContentType.objects.get(app_label=app_label, model=obj_model)
    except ContentType.DoesNotExist:
        # https://stackoverflow.com/questions/29193141/contenttype-matching-query-does-not-exist-only-on-sqlite-not-mysql
        object_model = ContentType.objects.get(app_label=app_label, model=origin_model.lower())
    obj = object_model.get_object_for_this_type(pk=obj_pk)
    sandwich, _ = obj.sandwich_model.objects.get_or_create(
        obj=obj,
        pdfsandwich_type=obj.get_sandwich_type(),
    )
    sandwich.update_pdf(obj)
    sandwich.save()

def send_pdfsandwich(modeladmin, request, queryset):
    base_url = email.get_base_url(request)
    for sandwich in queryset:
        content_type = ContentType.objects.get_for_model(sandwich)
        if settings.SMMAPDFS_CELERY:
            f = send_pdfsandwich_task.delay
        else:
            f = send_pdfsandwich_task
        f(content_type.app_label, content_type.model, sandwich.pk, base_url)

send_pdfsandwich.short_description = _("Send PDF Sandwich")

@task()
def send_pdfsandwich_task(app_label, model, pk, base_url):
    sandwich = ContentType.objects.get(app_label=app_label, model=model).get_object_for_this_type(pk=pk)
    email.send_pdfsandwich(sandwich, base_url)
