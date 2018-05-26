# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
from django.contrib import admin

from import_export.admin import ImportExportMixin

from related_admin import RelatedFieldAdmin


from . import models
import smmapdfs.actions


@admin.register(models.Winner)
class WinnerAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'user',
    )
    actions = smmapdfs.actions.pdfsandwich_actions(models.WinnerSandwich)


@admin.register(models.Competition)
class WinnerAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'name',
        'sandwich_type',
    )


@admin.register(models.Certificate)
class CertificateAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'pdfsandwich_type',
        'pdf',
        'pdfsandwich_type',
        'sent_time',
    )
    actions = (smmapdfs.actions.send_pdfsandwich,)


@admin.register(models.CertificateField)
class CertificateFieldAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'field',
        'x',
        'y',
        'font',
        'font_size',
    )
    list_editable = (
        'x',
        'y',
        'font',
        'font_size',
    )
