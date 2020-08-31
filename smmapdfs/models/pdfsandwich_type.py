# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
import os
from io import BytesIO

from PyPDF2 import PdfFileReader, PdfFileWriter

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext as _

from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfgen import canvas


def normpath(*args):
    return os.path.normpath(os.path.abspath(os.path.join(*args)))


class PdfSandwichType(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        verbose_name=_("Template name"), max_length=20, blank=False, null=False,
    )
    template_pdf = models.FileField(
        verbose_name=_("PDF template"),
        upload_to="pdfsandwich_types",
        blank=False,
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    height = models.IntegerField(verbose_name=_("Height (mm)"), default=210,)
    width = models.IntegerField(verbose_name=_("Width (mm)"), default=297,)

    def build_with_canvas(self, draw_on_canvas, sandwich):
        packet = BytesIO()
        fonts = {}
        output = PdfFileWriter()
        for field in sandwich.get_fields():
            fonts[field.font.pk] = field.font

        for font in fonts.values():
            try:
                pdfmetrics.registerFont(TTFont(font.name, font.ttf.open("rb")))
            except (ValueError, TTFError):
                sandwich.status += _(
                    "\nCorrupt font file for font '%s'. Font must be a valid TTF file.\n"
                    % font.name
                )
                return output
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=(self.height * mm, self.width * mm))
        draw_on_canvas(can)
        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        background_pdf = PdfFileReader(self.template_pdf, strict=False)
        page = background_pdf.getPage(0)
        try:
            page.mergePage(new_pdf.getPage(0))
        except IndexError:
            sandwich.status += _("\nNo fields rendered.\n")
        output.addPage(page)
        return output
