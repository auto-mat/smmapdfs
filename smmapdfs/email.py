# -*- coding: utf-8 -*-
# Copyright (C) 2018 o.s. Auto*Mat
import re
from os.path import basename
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.template import engines
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site

from .models import PdfSandwichEmail


def get_base_url(request):
    return "%s://%s" % (request.scheme, request.META["HTTP_HOST"],)


def send_pdfsandwich(pdfsandwich, base_url):
    language = pdfsandwich.get_language()
    email_template = PdfSandwichEmail.objects.get(
        language=language, pdfsandwich_type=pdfsandwich.pdfsandwich_type
    )
    django_template = engines["django"].from_string(email_template.template)
    context = pdfsandwich.get_context(base_url=base_url)
    context["download_link"] = pdfsandwich.get_pdf_url(base_url)
    html_message = django_template.render(context)
    # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string#12982689
    cleanr = re.compile("<.*?>")
    message = re.sub(cleanr, "", html_message)
    email = EmailMultiAlternatives(
        subject=email_template.subject,
        body=message,
        from_email=None,
        to=[pdfsandwich.get_email()],
    )
    pdf = pdfsandwich.pdf
    pdf.open()
    email.attach(basename(pdf.name), pdf.read(), "application/pdf")
    email.attach_alternative(html_message, "text/html")
    email.send()
    pdfsandwich.sent_time = datetime.now()
    pdfsandwich.save()
