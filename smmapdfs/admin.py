# -*- coding: utf-8 -*-
# Copyright (C) 2016 o.s. Auto*Mat

import re

from django import forms
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from fieldsets_with_inlines import FieldsetsInlineMixin

from import_export.admin import ImportExportMixin

from related_admin import RelatedFieldAdmin


from . import actions
from . import models
from .widgets import RelatedFieldWidgetCanAdd


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


def get_competition_admin_mixin(
        competition_model, pdfsandwich_type_model,
        certificate_field_model, proxy_model,
):
    class BaseCompetitionModelForm(forms.ModelForm):
        class Meta:
            model = competition_model
            fields = '__all__'

    class CompetitionWithSandwichTypeFieldModelForm(
            BaseCompetitionModelForm
    ):
        stype = forms.ModelChoiceField(
            queryset=pdfsandwich_type_model.objects.all(),
            widget=RelatedFieldWidgetCanAdd(
                related_model=pdfsandwich_type_model,
            ),
            label=_('Sandwich type'),
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if kwargs.get('instance'):
                self.initial['stype'] = self.instance.sandwich_type

        def save(self, commit=True, **kwargs):
            form = super().save(commit=False)
            if 'stype' in self.changed_data:
                form.sandwich_type = self.cleaned_data['stype']
            form.save()
            return form

    class CompetitionWithSandwichTypeFieldInline(admin.StackedInline):
        model = competition_model
        form = CompetitionWithSandwichTypeFieldModelForm
        extra = 1
        max_num = 1
        min_num = 1
        can_delete = False

        def get_queryset(self, request):
            qs = super().get_queryset(request)
            competiton_id = re.findall(r'[0-9]+', request.path)
            if competiton_id:
                competiton_id = int(competiton_id[0])
                return qs.filter(id=competiton_id)
            return qs

    class CompetitionInline(CompetitionWithSandwichTypeFieldInline):
        form = BaseCompetitionModelForm

    class CertificateFieldInline(admin.TabularInline):
        model = certificate_field_model
        extra = 0
        max = 1

    class CompetitionAdminMixin(FieldsetsInlineMixin, admin.ModelAdmin):
        list_display = (
            'competition_name',
            'sw_type',
        )

        def competition_name(self, obj):
            return obj

        competition_name.admin_order_field = 'name'
        competition_name.short_description = _('Competition name')

        def sw_type(self, obj):
            url = self.get_sandwich_type_obj_url(
                obj_id=obj.sandwich_type.id,
            )
            url += '?_to_field=id&_popup=1'
            return format_html(
                """
                <b>
                <a href="{url}"
                onclick="return showAddAnotherPopup(this);">
                {obj_name}</a>
                </b>
                """, url=url, obj_name=obj.sandwich_type.name,
            )

        sw_type.admin_order_field = 'sandwich_type'
        sw_type.short_description = _('Sandwich type')

        def get_fieldsets(self, request, obj=None):
            sandwich_type_objs = pdfsandwich_type_model.objects.all()

            if obj:
                self.fieldsets_with_inlines = [
                    CompetitionWithSandwichTypeFieldInline,
                    (
                        self.get_fieldset_root_name(
                            name=pdfsandwich_type_model.__name__,
                        ), {
                            'fields': (
                                'name', 'template_pdf', 'width',
                                'height',
                            ),
                        }
                    ),
                    CertificateFieldInline,
                    PdfSandwichEmailAdminInline,
                ]
            elif sandwich_type_objs:
                self.fieldsets_with_inlines = [
                    CompetitionWithSandwichTypeFieldInline,
                ]
            else:
                self.fieldsets_with_inlines = [
                    CompetitionInline,
                    (
                        self.get_fieldset_root_name(
                            name=pdfsandwich_type_model.__name__,
                        ), {
                            'fields': (
                                'name', 'template_pdf', 'width',
                                'height',
                            ),
                        }
                    ),
                    CertificateFieldInline,
                    PdfSandwichEmailAdminInline,
                ]

            return super().get_fieldsets(request, obj)

        def get_queryset(self, request):
            app, model = (
                proxy_model._meta.app_label,
                proxy_model._meta.object_name.lower(),
            )
            related_url = "admin:{app}_{model}_add".format(
                app=app, model=model,
            )
            url = reverse(related_url)
            url = url.split('add', 3)[0]
            if request.path == url:
                # View list
                return competition_model.objects.all()
            # Change model object
            return super().get_queryset(request)

        def change_view(
                self, request, object_id, form_url='',
                extra_context=None,
        ):
            extra_context = extra_context or {}
            self.parent_obj_id = object_id
            object_id = str(
                competition_model.objects.get(
                    id=object_id,
                ).sandwich_type.id,
            )
            return super().change_view(
                request, object_id, form_url,
                extra_context=extra_context,
            )

        def save_model(self, request, obj, form, change):
            if not isinstance(form, int):
                return super().save_model(request, obj, form, change)

        def message_user(self, *args, **kwargs):
            competiton_id = re.findall(r'[0-9]+', args[1])
            if competiton_id:
                competiton_id = int(competiton_id[0])
                competition_objs = competition_model.objects.filter(
                    id=competiton_id,
                )
                for obj in competition_objs:
                    args = list(args)
                    args[1] = format_html(
                        re.sub(r'>.*?<', ">{}<".format(obj.name), args[1]),
                    )
            super().message_user(*args)

        def get_fieldset_root_name(self, name):
            return ' '.join(
                re.findall('[A-Z][^A-Z]*', name),
            ).upper()

        def get_sandwich_type_obj_url(self, obj_id):
            app, model = (
                pdfsandwich_type_model._meta.app_label,
                pdfsandwich_type_model._meta.object_name.lower(),
            )
            related_url = "admin:{app}_{model}_change".format(
                app=app, model=model,
            )
            url = reverse(related_url, args=(obj_id,))
            return url

    return CompetitionAdminMixin


def get_competition_admin_mixin_proxy_model(
        model, class_name, meta_attrs, module,
):
    def create_class(module, meta_attrs=None):
        class Meta:
            proxy = True
        if meta_attrs is not None:
            for k, v in meta_attrs.items():
                setattr(Meta, k, v)
        attrs = {'__module__': module, 'Meta': Meta}
        return type(class_name, model, attrs)

    return create_class(module, meta_attrs)
