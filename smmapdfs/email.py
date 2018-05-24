# -*- coding: utf-8 -*-
# Copyright (C) 2018 o.s. Auto*Mat
import re
from datetime import datetime

from celery import shared_task

from django.core.mail import send_mail
from django.template import engines
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site

from .models import PdfSandwichEmail


def get_base_url(request, slug=None):
    return '%s://%s.%s' % (
        request.scheme,
        slug if slug is not None else request.campaign.slug,
        get_current_site(request).domain,
    )


def send(modeladmin, request, queryset):
    send_pdfsandwichs_from_queryset(queryset, get_base_url(request))


send.short_description = _("Send")


def send_celery(modeladmin, request, queryset):
    for pdfsandwich_type in queryset:
        send_pdfsandwichs_of_type.apply_async(args=(pdfsandwich_type.pk, get_base_url(request)))


send_celery.short_description = _("Odeslat přes celerem")


@shared_task(bind=True)
def send_pdfsandwichs_of_type(self, sandwich_model, pdfsandwich_type_pk, base_url):
    send_pdfsandwichs_from_queryset(sandwhich_model.objects.filter(pdfsandwich_type__pk=pdfsandwich_type_pk), base_url)


def send_pdfsandwichs_from_queryset(queryset, base_url):
    for pdfsandwich in queryset:
        send_pdfsandwich(pdfsandwich, base_url)


def send_pdfsandwich(pdfsandwich, base_url):
    #userprofile = pdfsandwich.user_attendance.userprofile
    #language = userprofile.language
    language="en"
    email_template = PdfSandwichEmail.objects.get(language=language, pdfsandwich_type=pdfsandwich.pdfsandwich_type)
    django_template = engines['django'].from_string(email_template.template)
    html_message = django_template.render({
        'name': pdfsandwich.get_name(),
        'download_link': pdfsandwich.pdf.url if pdfsandwich.pdf.url.startswith("https") else base_url + pdfsandwich.pdf.url,
    })
    # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string#12982689
    cleanr = re.compile('<.*?>')
    message = re.sub(cleanr, '', html_message)
    send_mail(email_template.subject, message, None, [pdfsandwich.get_email()], fail_silently=False, html_message=html_message)
    pdfsandwich.sent_time = datetime.now()
    pdfsandwich.save()
