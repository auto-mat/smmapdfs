# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
from django import forms
from django.contrib import admin

from import_export.admin import ImportExportMixin

from related_admin import RelatedFieldAdmin

from . import models
import smmapdfs.actions


class PdfSandwichAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        "obj",
        "pdfsandwich_type",
        "pdf",
        "status",
        "recipient",
        "sent_time",
    )
    raw_id_fields = ("obj",)
    readonly_fields = (
        "obj",
        "pdfsandwich_type",
        "pdf",
        "status",
        "sent_time",
    )

    list_filter = (
        "pdfsandwich_type__name",
        "sent_time",
    )
    actions = (smmapdfs.actions.send_pdfsandwich,)

    def has_add_permission(self, request, obj=None):
        return False

    def recipient(self, obj):
        try:
            return obj.get_email()
        except AttributeError:
            return "-"


def fieldForm(form_model):
    class _FieldForm(forms.ModelForm):
        class Meta:
            model = form_model
            exclude = ("site_of_origin",)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["field"].widget = forms.Select(
                choices=self._meta.model.get_field_choices()
            )

    return _FieldForm


class PdfSandwichFieldAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = (
        "id",
        "pdfsandwich_type",
        "field",
        "x",
        "y",
        "font",
        "font_size",
        "alignment",
    )
    list_editable = (
        "x",
        "y",
        "font",
        "font_size",
        "alignment",
    )

    list_filter = ("pdfsandwich_type__name",)
