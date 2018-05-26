from . import email
from celery import task
from django.contrib.contenttypes.models import ContentType
from .models import PdfSandwichType

from django.conf import settings

def pdfsandwich_actions(sandwich_model):
    def make_pdfsandwich(modeladmin, request, queryset):
        sandwich_model_type = ContentType.objects.get_for_model(sandwich_model.sandwich_model)
        sandwich_field_model_type = ContentType.objects.get_for_model(sandwich_model.sandwich_field_model)

        for obj in queryset:
            if settings.SMMAPDFS_CELERY:
                f = make_pdfsandwich_task.delay
            else:
                f = make_pdfsandwich_task
            f(
                sandwich_model_type.app_label,
                obj.__class__.__name__,
                sandwich_model_type.model,
                sandwich_field_model_type.model,
                obj.pk,
                sandwich_model.get_sandwich_type(obj).pk,
            )
    return (make_pdfsandwich,)

@task()
def make_pdfsandwich_task(app_label, origin_model, sandwich_model, sandwich_field_model, obj_pk, sandwich_type_pk):
    sandwich_model = ContentType.objects.get(app_label=app_label, model=sandwich_model).model_class()
    sandwich_field_model = ContentType.objects.get(app_label=app_label, model=sandwich_field_model).model_class()
    print(app_label, origin_model, obj_pk)
    try:
        object_model = ContentType.objects.get(app_label=app_label, model=origin_model)
    except ContentType.DoesNotExist:
        # https://stackoverflow.com/questions/29193141/contenttype-matching-query-does-not-exist-only-on-sqlite-not-mysql
        object_model = ContentType.objects.get(app_label=app_label, model=origin_model.lower())
    obj = object_model.get_object_for_this_type(pk=obj_pk)
    sandwich, _ = sandwich_model.objects.get_or_create(
        obj=obj,
        pdfsandwich_type=PdfSandwichType.objects.get(pk=sandwich_type_pk),
    )
    sandwich.update_pdf(obj, sandwich_field_model)
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

@task()
def send_pdfsandwich_task(app_label, model, pk, base_url):
    sandwich = ContentType.objects.get(app_label=app_label, model=model).get_object_for_this_type(pk=pk)
    email.send_pdfsandwich(sandwich, base_url)
