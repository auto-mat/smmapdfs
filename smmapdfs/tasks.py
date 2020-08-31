from celery import task

from django.contrib.contenttypes.models import ContentType

from . import email


@task()
def make_pdfsandwich(app_label, obj_model, obj_pk, continuation=None):
    try:
        object_model = ContentType.objects.get(app_label=app_label, model=obj_model)
    except ContentType.DoesNotExist:
        # https://stackoverflow.com/questions/29193141/contenttype-matching-query-does-not-exist-only-on-sqlite-not-mysql
        object_model = ContentType.objects.get(
            app_label=app_label, model=obj_model.lower()
        )
    obj = object_model.get_object_for_this_type(pk=obj_pk)
    sandwich, _ = obj.sandwich_model.objects.get_or_create(
        obj=obj, pdfsandwich_type=obj.get_sandwich_type(),
    )
    sandwich.update_pdf(obj)
    sandwich.save()
    if continuation is not None:
        continuation(sandwich)


@task()
def send_pdfsandwich(app_label, model, pk, base_url):
    sandwich = ContentType.objects.get(
        app_label=app_label, model=model
    ).get_object_for_this_type(pk=pk)
    email.send_pdfsandwich(sandwich, base_url)
