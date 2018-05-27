# -*- coding: utf-8 -*-
# Copyright (C) 2018 o.s. Auto*Mat

from django.conf import settings
from django.contrib.gis.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.translation import ugettext_lazy as _

from reportlab.lib.units import mm


class PdfSandwichABC(models.Model):
    pdfsandwich_type = models.ForeignKey(
        'PdfSandwichType',
        verbose_name=_("PDF sandwich template/type"),
        null=False,
        blank=False,
        default='',
        on_delete=models.CASCADE,
    )

    pdf = models.FileField(
        verbose_name=_(u"pdfsandwich PDF"),
        upload_to='pdfsandwichs',
        blank=True,
        null=True,
    )

    sent_time = models.DateTimeField(
        verbose_name=_("Sent time"),
        null=True,
        blank=True,
        default=None,
    )

    def update_pdf(self, obj):
        temp = NamedTemporaryFile()

        def draw_fields(can):
            for field in self.field_model.objects.filter(pdfsandwich_type=self.pdfsandwich_type):
                field.draw_on_canvas(can, obj)
            can.save()
        output = self.pdfsandwich_type.build_with_canvas(draw_fields)
        output.write(temp)
        filename = "%s/pdfsandwich_%s.pdf" % (
            self.pdfsandwich_type.name,
            hash(str(self.pk) + settings.SECRET_KEY)
        )
        try:
            self.pdf.delete()
        except ValueError:
            pass
        self.pdf.save(filename, File(temp), save=True)
