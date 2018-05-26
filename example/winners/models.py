from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


from smmapdfs.models import PdfSandwichType
from smmapdfs.model_abcs import  PdfSandwichABC, PdfSandwichFieldABC

from abc import abstractmethod


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


class Winner(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        default='',
        on_delete=models.CASCADE,
    )
    competition = models.ForeignKey(
        Competition,
        null=False,
        blank=False,
        default='',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username

class CertificateField(PdfSandwichFieldABC):
    fields = {"name": (lambda w: w.user.username), "email": (lambda w: w.user.name)}


class Certificate(PdfSandwichABC):
    field_model = CertificateField
    obj = models.ForeignKey(
        Winner,
        null=False,
        blank=False,
        default='',
        on_delete=models.CASCADE,
    )

    def get_email(self):
        return self.obj.user.email

    def get_name(self):
        return self.obj.user.username

    def get_language(self):
        return "en"


class WinnerSandwich():
    sandwich_model = Certificate

    sandwich_field_model = CertificateField

    @abstractmethod
    def get_sandwich_type(winner):
        return winner.competition.sandwich_type
