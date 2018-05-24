# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
from django.contrib import admin

from import_export.admin import ImportExportMixin

from related_admin import RelatedFieldAdmin


from . import email
from . import models


@admin.register(models.PdfSandwichType)
class PdfSandwichTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'height',
        'width',
    )
    actions = (email.send_celery,)


class PdfSandwichFieldAdminMixin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'field',
        'x',
        'y',
        'pdfsandwich_type',
    )
    list_editable = ('x', 'y', 'pdfsandwich_type')

@admin.register(models.PdfSandwichEmail)
class PdfSandwichEmailAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'pdfsandwich_type',
        'language',
    )


class PdfSandwichAdminMixin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'pdfsandwich_type',
        'pdf',
        'sent_time',
    )
    actions = (
        email.send,
    )


@admin.register(models.PdfSandwichFont)
class PdfSandwichAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        'name',
        'ttf',
    )
