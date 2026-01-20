# -*- coding: utf-8 -*-

from import_export import resources
from import_export.fields import Field

from smmapdfs.models import PdfSandwichEmail, PdfSandwichFont, \
    PdfSandwichType

import tablib

from .models import CertificateField, Competition


class CompetitionResource(resources.ModelResource):

    # Competition
    cname = Field(column_name='competition_name', attribute='name')

    sandwich_type = Field(
        column_name='sandwich_type_id', attribute='sandwich_type',
    )

    # PdfSandwichType
    name = Field(column_name='sandwich_type_name')
    height = Field(column_name='height', attribute='height')
    width = Field(column_name='width', attribute='width')
    template_pdf = Field(
        column_name='template_pdf', attribute='template_pdf',
    )

    # PdfSandwichEmail
    sandwich_email_id = Field(
        column_name='sandwich_email_id', attribute='sandwich_email_id',
    )
    language = Field(column_name='language', attribute='language')
    subject = Field(column_name='subject', attribute='subject')
    template = Field(column_name='template', attribute='template')

    # Certificate
    field = Field(column_name='field', attribute='field')
    font_size = Field(column_name='font_size', attribute='font_size')
    font_id = Field(column_name='font_id', attribute='font_id')
    font_name = Field(column_name='font_name', attribute='font_name')
    font = Field(column_name='font', attribute='font')
    x = Field(column_name='x', attribute='x')
    y = Field(column_name='y', attribute='y')
    alignment = Field(column_name='alignment', attribute='alignment')
    stroke_color = Field(column_name='stroke_color', attribute='stroke_color')
    fill_color = Field(column_name='fill_color', attribute='fill_color')

    separator = '\n\n'

    class Meta:
        model = Competition
        export_order = ('id', 'cname', 'sandwich_type')

    def export(self, queryset=None, *args, **kwargs):
        queryset = Competition.objects.all()
        self.before_export(queryset, *args, **kwargs)
        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)

        for obj in self.iter_queryset(queryset):
            data.append(self.export_resource(obj))
        self.after_export(queryset, data, *args, **kwargs)
        return data

    def _get_values(self, obj, model, field, cast=None):
        if isinstance(obj, PdfSandwichType):
            values = model.objects.filter(
                pdfsandwich_type=obj,
            ).values_list(field, flat=True)
        else:
            values = model.objects.filter(
                pdfsandwich_type=obj.sandwich_type,
            ).values_list(field, flat=True)
        if cast:
            return self.separator.join([cast(i) for i in values])
        return self.separator.join(values)

    def dehydrate_id(self, obj):
        if obj.pk:
            if isinstance(obj, PdfSandwichType):
                return Competition.objects.filter(
                    sandwich_type=obj,
                ).first().id
            else:
                return obj.id

    def dehydrate_sandwich_type(self, obj):
        if obj.pk:
            if isinstance(obj, PdfSandwichType):
                return obj.id
            else:
                return obj.sandwich_type.id

    def dehydrate_name(self, obj):
        if obj.pk:
            if isinstance(obj, PdfSandwichType):
                return obj.name
            else:
                return obj.sandwich_type

    def dehydrate_width(self, obj):
        if obj.pk:
            if isinstance(obj, PdfSandwichType):
                return obj.name
            else:
                return obj.sandwich_type.width

    def dehydrate_height(self, obj):
        if obj.pk:
            if isinstance(obj, PdfSandwichType):
                return obj.name
            else:
                return obj.sandwich_type.height

    def dehydrate_template_pdf(self, obj):
        if obj.pk:
            if isinstance(obj, PdfSandwichType):
                return obj.name
            else:
                return obj.sandwich_type.template_pdf

    def dehydrate_cname(self, obj):
        if obj.pk:
            if isinstance(obj, PdfSandwichType):
                return Competition.objects.filter(
                    sandwich_type=obj,
                ).first().name
            else:
                return obj.name

    def dehydrate_sandwich_email_id(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=PdfSandwichEmail, field='id', cast=str,
            )

    def dehydrate_subject(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=PdfSandwichEmail, field='subject',
            )

    def dehydrate_language(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=PdfSandwichEmail, field='language',
            )

    def dehydrate_template(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=PdfSandwichEmail, field='template',
            )

    def dehydrate_field(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='field',
            )

    def dehydrate_font_size(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='font_size',
                cast=str,
            )

    def dehydrate_font_id(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='font', cast=str,
            )

    def dehydrate_font_name(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='font__name',
            )

    def dehydrate_font(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='font__ttf',
            )

    def dehydrate_x(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='x', cast=str,
            )

    def dehydrate_y(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='y', cast=str,
            )

    def dehydrate_alignment(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='alignment',
            )

    def dehydrate_stroke_color(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='stroke_color',
            )

    def dehydrate_fill_color(self, obj):
        if obj.pk:
            return self._get_values(
                obj=obj, model=CertificateField, field='fill_color',
            )

    def import_obj(self, obj, data, dry_run):  # noqa
        # PdfSandwichType
        sandwich_type_id = data.pop('sandwich_type_id')
        super().import_obj(obj, data, dry_run)

        sandwich_type_obj = PdfSandwichType.objects.filter(
            id=sandwich_type_id,
        )
        if sandwich_type_obj:
            sandwich_type_obj.update(
                template_pdf=data.get('template_pdf'),
                name=data.get('sandwich_type_name'),
                width=data.get('width'),
                height=data.get('height'),
            )
            sandwich_type_obj = sandwich_type_obj[0]
        else:
            sandwich_type_obj, _ = PdfSandwichType.objects.get_or_create(
                template_pdf=data.get('template_pdf'),
                name=data.get('sandwich_type_name'),
                width=data.get('width'),
                height=data.get('height'),

            )
        # PdfSandwichEmail

        if data.get('sandwich_email_id'):
            emails_ids = data.get('sandwich_email_id').split(self.separator)
            emails_languages = data.get('language').split(self.separator)
            emails_subjects = data.get('subject').split(self.separator)
            emails_templates = data.get('template').split(self.separator)

            for index, email_id in enumerate(emails_ids):
                email_obj = PdfSandwichEmail.objects.filter(
                    id=int(email_id),
                )
                if email_obj:
                    email_obj.update(
                        pdfsandwich_type=sandwich_type_obj,
                        language=emails_languages[index],
                        subject=emails_subjects[index],
                        template=emails_templates[index],
                    )
                    email_obj = email_obj[0]
                else:
                    email_obj, _ = PdfSandwichEmail.objects.get_or_create(
                        pdfsandwich_type=sandwich_type_obj,
                        language=emails_languages[index],
                        subject=emails_subjects[index],
                        template=emails_templates[index],
                    )

        # Certificate
        if data.get('field'):
            fields = data.get('field').split(self.separator)
            font_sizes = data.get('font_size').split(self.separator)
            font_ids = data.get('font_id').split(self.separator)
            font_names = data.get('font_name').split(self.separator)
            fonts = data.get('font').split(self.separator)
            xs = data.get('x').split(self.separator)
            ys = data.get('y').split(self.separator)
            alignments = data.get('alignment').split(self.separator)
            stroke_colors = data.get('stroke_color').split(self.separator)
            fill_colors = data.get('fill_color').split(self.separator)

            for index, field in enumerate(fields):
                if font_ids[index]:
                    font_obj = PdfSandwichFont.objects.filter(
                        id=font_ids[index],
                    )
                    if font_obj:
                        font_obj.update(
                            name=font_names[index],
                            ttf=fonts[index],
                        )
                        font_obj = font_obj[0]
                    else:
                        font_obj, _ = PdfSandwichFont.objects.get_or_create(
                            name=font_names[index],
                            ttf=fonts[index],
                        )
                if fields[index]:
                    certificate_obj, created = CertificateField.objects.\
                        get_or_create(
                            pdfsandwich_type=sandwich_type_obj,
                            field=fields[index],
                            font_size=font_sizes[index],
                            font=font_obj,
                            x=xs[index],
                            y=ys[index],
                            alignment=alignments[index],
                            stroke_color=stroke_colors[index],
                            fill_color=fill_colors[index],
                        )
                    if not created:
                        certificate_obj.pdfsandwich_type = sandwich_type_obj
                        certificate_obj.field = fields[index]
                        certificate_obj.font_size = font_sizes[index]
                        certificate_obj.font = font_obj
                        certificate_obj.x = xs[index]
                        certificate_obj.y = ys[index]
                        certificate_obj.alignment = alignments[index]
                        certificate_obj.stroke_color = stroke_colors[index]
                        certificate_obj.fill_color = fill_colors[index]
                        certificate_obj.save()

        obj.sandwich_type = sandwich_type_obj
        obj.save()
