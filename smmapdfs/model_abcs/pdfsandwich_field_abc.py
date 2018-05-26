# -*- coding: utf-8 -*-

# Copyright (C) 2016 o.s. Auto*Mat

from django.contrib.gis.db import models
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import ugettext_lazy as _

from reportlab.lib.units import mm


class PdfSandwichFieldABC(models.Model):
    class Meta:
        abstract = True
        def __new__(cls, clsname, bases, dct):
            res = type.__new__(cls, clsname, bases, dct)
            cls.field.choices = [(a, a) for a in cls.fields.keys()]
            return res

    def __str__(self):
        return self.field

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/questions/6001986/dynamic-choices-field-in-django-models
        super().__init__(*args, **kwargs)
        self._meta.get_field('field').choices = [(a, a) for a in self.fields.keys()]

    pdfsandwich_type = models.ForeignKey(
        'smmapdfs.PdfSandwichType',
        related_name="pdfsandwich_fields",
        null=True,
        blank=False,
        default=None,
        on_delete=models.CASCADE,
    )
    field = models.CharField(
        verbose_name=_("field"),
        choices=[],
        max_length=36,
        default=None,
        null=False,
        blank=False,
    )
    font_size = models.IntegerField(
        verbose_name=_("Font size"),
        default=16,
        null=False,
        blank=False,
    )
    font = models.ForeignKey(
        'smmapdfs.PdfSandwichFont',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    x = models.IntegerField(
        verbose_name=_("X (mm)"),
        default=0,
    )
    y = models.IntegerField(
        verbose_name=_("Y (mm)"),
        default=0,
    )
    def draw_on_canvas(self, can, obj):
        can.setFont(self.font.name, self.font_size)
        can.drawString(self.x * mm, self.y * mm, self.fields[self.field](obj))
