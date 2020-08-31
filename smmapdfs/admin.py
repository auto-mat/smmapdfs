# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
from django.contrib import admin
from django.conf import settings
from django import forms

from import_export.admin import ImportExportMixin

from related_admin import RelatedFieldAdmin

from . import actions
from . import models


class PdfSandwichFieldAdminMixin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        "field",
        "x",
        "y",
        "pdfsandwich_type",
    )
    list_editable = ("x", "y", "pdfsandwich_type")


class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            more_attrs = settings.SMMAPDFS_EMAIL_CONTEXT_HELP
        except AttributeError:
            more_attrs = ""
        self.fields["template"].help_text = (
            "You can use the following variables in the email context:<br/>{{download_link|safe}} - Url for downlaoding the pdf sandwich\n"
            + more_attrs
        )

    class Meta:
        model = models.PdfSandwichEmail
        exclude = ()


@admin.register(models.PdfSandwichEmail)
class PdfSandwichEmailAdmin(ImportExportMixin, RelatedFieldAdmin):
    form = EmailForm
    list_display = (
        "pdfsandwich_type",
        "language",
    )


class PdfSandwichEmailAdminInline(admin.TabularInline):
    model = models.PdfSandwichEmail
    form = EmailForm
    extra = 0


@admin.register(models.PdfSandwichType)
class PdfSandwichTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "height",
        "width",
    )
    inlines = [
        PdfSandwichEmailAdminInline,
    ]


class PdfSandwichAdminMixin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        "obj",
        "pdfsandwich_type",
        "pdf",
        "sent_time",
    )
    actions = (actions.send_pdfsandwich,)


@admin.register(models.PdfSandwichFont)
class PdfSandwichFontAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        "name",
        "ttf",
    )
