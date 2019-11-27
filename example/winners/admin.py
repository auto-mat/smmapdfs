# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
from django.contrib import admin

from import_export.admin import ImportExportMixin

from related_admin import RelatedFieldAdmin


from . import models
import smmapdfs.actions
from smmapdfs.admin_abcs import PdfSandwichAdmin, PdfSandwichFieldAdmin, fieldForm


@admin.register(models.Winner)
class WinnerAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'user',
    )
    actions = (smmapdfs.actions.make_pdfsandwich,)


@admin.register(models.Competition)
class CompetitionAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'name',
        'sandwich_type',
    )


@admin.register(models.Certificate)
class CertificateAdmin(PdfSandwichAdmin):
    pass

@admin.register(models.CertificateField)
class CertificateFieldAdmin(PdfSandwichFieldAdmin):
    form = fieldForm(models.CertificateField)
