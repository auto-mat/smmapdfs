# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat
from django.contrib import admin
from django.utils.translation import gettext as _

from import_export.admin import ImportExportMixin

from related_admin import RelatedFieldAdmin

import smmapdfs.actions
from smmapdfs.admin import PdfSandwichTypeAdmin,\
    get_competition_admin_mixin, get_competition_admin_mixin_proxy_model
from smmapdfs.admin_abcs import PdfSandwichAdmin, PdfSandwichFieldAdmin,\
    fieldForm

from . import models
from .resources import CompetitionResource


@admin.register(models.Winner)
class WinnerAdmin(ImportExportMixin, RelatedFieldAdmin):
    list_display = ("user",)
    actions = (
        smmapdfs.actions.make_pdfsandwich,
        smmapdfs.actions.make_and_send_pdfsandwich,
    )


proxy_model = get_competition_admin_mixin_proxy_model(
    model=(models.PdfSandwichType,),
    class_name='CompetitionProxy',
    meta_attrs={
        'verbose_name': _('Competition'),
        'verbose_name_plural': _('Competitions'),
    },
    module='winners',
)
@admin.register(proxy_model)
class CompetitionAdmin(
        ImportExportMixin, RelatedFieldAdmin,
        get_competition_admin_mixin(
            competition_model=models.Competition,
            pdfsandwich_type_model=models.PdfSandwichType,
            certificate_field_model=models.CertificateField,
            proxy_model=proxy_model,
        ),
):
    resource_class = CompetitionResource


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
