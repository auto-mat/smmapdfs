# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
import os
from io import BytesIO

from PyPDF2 import PdfFileReader, PdfFileWriter

from django.contrib.gis.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _

from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .pdfsandwich_font import PdfSandwichFont

def normpath(*args):
    return os.path.normpath(os.path.abspath(os.path.join(*args)))


class PdfSandwichType(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        verbose_name=_("Template name"),
        max_length=20,
        blank=False,
        null=False,
    )
    template_pdf = models.FileField(
        verbose_name=_("PDF template"),
        upload_to='pdfsandwich_types',
        blank=False,
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    height = models.IntegerField(
        verbose_name=_("Height (mm)"),
        default=210,
    )
    width = models.IntegerField(
        verbose_name=_("Width (mm)"),
        default=297,
    )

    def build_with_canvas(self, draw_on_canvas):
        packet = BytesIO()
        for font in PdfSandwichFont.objects.all():
            pdfmetrics.registerFont(TTFont(font.name, font.ttf.open("r")))
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=(self.height * mm, self.width * mm))
        draw_on_canvas(can)
        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        output = PdfFileWriter()
        background_pdf = PdfFileReader(self.template_pdf, strict=False)
        page = background_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        return output
