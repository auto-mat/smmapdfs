# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
from django.contrib import admin

from import_export.admin import ImportExportMixin

from related_admin import RelatedFieldAdmin

from . import models
import smmapdfs.actions
from smmapdfs.admin import PdfSandwichTypeAdmin
from smmapdfs.admin_abcs import PdfSandwichAdmin, PdfSandwichFieldAdmin, fieldForm
from smmapdfs.models import PdfSandwichType

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


""" this is optional just for better admin view """
class CertificateFieldInline(admin.TabularInline):
    model = models.CertificateField
    can_delete = True
    extra = 0

admin.site.unregister(models.CertificateField)
admin.site.unregister(models.PdfSandwichType)
@admin.register(models.PdfSandwichType)
class _PdfSandwichTypeAdmin(PdfSandwichTypeAdmin):
    inlines = (CertificateFieldInline,)
