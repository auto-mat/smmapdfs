# -*- coding: utf-8 -*-
# Copyright (C) 2018 o.s. Auto*Mat

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.utils.translation import ugettext_lazy as _

from reportlab.lib.units import mm

import uuid


class PdfSandwichABC(models.Model):
    pdfsandwich_type = models.ForeignKey(
        "PdfSandwichType",
        verbose_name=_("PDF sandwich template/type"),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    pdf = models.FileField(
        verbose_name=_(u"pdfsandwich PDF"),
        upload_to="pdfsandwichs",
        blank=True,
        null=True,
    )

    sent_time = models.DateTimeField(
        verbose_name=_("Sent time"), null=True, blank=True, default=None,
    )

    status = models.TextField(verbose_name=_("Status"), blank=True, default="",)

    def get_pdf_url(self, base_url):
        return (
            self.pdf.url
            if self.pdf.url.startswith("https")
            else base_url + self.pdf.url
        )

    def get_fields(self):
        return self.field_model.objects.filter(pdfsandwich_type=self.pdfsandwich_type)

    def get_context(self, base_url):
        context = {}
        for name, field in self.field_model.fields.items():
            context[name] = field(self.obj)
        return context

    def update_pdf(self, obj):
        self.status = ""
        temp = NamedTemporaryFile()

        def draw_fields(can):
            for field in self.get_fields():
                field.draw_on_canvas(can, obj)
            can.save()

        output = self.pdfsandwich_type.build_with_canvas(draw_fields, self)
        output.write(temp)
        filename = "%s/pdfsandwich_%s.pdf" % (self.pdfsandwich_type.name, uuid.uuid4())
        try:
            self.pdf.delete()
        except ValueError:
            pass
        self.pdf.save(filename, File(temp), save=False)
        self.save()
