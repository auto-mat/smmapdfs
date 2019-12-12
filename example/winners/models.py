from django.db import models
from django.contrib.auth.models import User

from smmapdfs.models import PdfSandwichType
from smmapdfs.model_abcs import  PdfSandwichABC, PdfSandwichFieldABC

from abc import abstractmethod


class CertificateField(PdfSandwichFieldABC):
    fields = {"name": (lambda w: w.user.username), "email": (lambda w: w.user.email)}


class Certificate(PdfSandwichABC):
    field_model = CertificateField
    obj = models.ForeignKey(
        'Winner',
        null=False,
        blank=False,
        default='',
        on_delete=models.CASCADE,
    )

    def get_email(self):
        return self.obj.user.email

    def get_context(self, base_url):
        context = super().get_context(base_url)
        context['base_url'] = base_url
        return context

    def get_language(self):
        return "en"


class Winner(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        default='',
        on_delete=models.CASCADE,
    )
    competition = models.ForeignKey(
        'Competition',
        null=False,
        blank=False,
        default='',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username

    sandwich_model = Certificate
    def get_sandwich_type(self):
        return self.competition.sandwich_type

class Competition(models.Model):
    name = models.CharField(
        max_length = 80,
    )
    sandwich_type = models.ForeignKey(
        PdfSandwichType,
        null=False,
        blank=False,
        default='',
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.name
