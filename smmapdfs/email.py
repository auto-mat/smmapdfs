# -*- coding: utf-8 -*-
# Copyright (C) 2018 o.s. Auto*Mat
import re
from datetime import datetime

from django.core.mail import send_mail
from django.template import engines
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site

from .models import PdfSandwichEmail


def get_base_url(request):
    return '%s://%s' % (
        request.scheme,
        request.META['HTTP_HOST'],
    )

def send_pdfsandwich(pdfsandwich, base_url):
    language = pdfsandwich.get_language()
    email_template = PdfSandwichEmail.objects.get(language=language, pdfsandwich_type=pdfsandwich.pdfsandwich_type)
    django_template = engines['django'].from_string(email_template.template)
    html_message = django_template.render({
        'name': pdfsandwich.get_name(),
        'download_link': pdfsandwich.get_pdf_url(base_url),
    })
    # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string#12982689
    cleanr = re.compile('<.*?>')
    message = re.sub(cleanr, '', html_message)
    send_mail(email_template.subject, message, None, [pdfsandwich.get_email()], fail_silently=False, html_message=html_message)
    pdfsandwich.sent_time = datetime.now()
    pdfsandwich.save()
