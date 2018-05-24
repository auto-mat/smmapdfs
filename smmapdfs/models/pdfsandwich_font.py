# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class PdfSandwichFont(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        verbose_name=_("Font name"),
        max_length=20,
        blank=False,
        null=False,
    )
    ttf = models.FileField(
        verbose_name=_("Font"),
        upload_to='pdfsandwich_fonts',
        blank=False,
        null=False,
    )
