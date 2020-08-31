# -*- coding: utf-8 -*-

# Copyright (C) 2016 o.s. Auto*Mat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from django.db import models
from django.utils.translation import ugettext_lazy as _


languages = [
    ("en", _("English")),
    ("cs", _("Czech")),
    ("dsnkcs", _("Škola")),
]


class PdfSandwichEmail(models.Model):
    def __str__(self):
        return self.subject

    pdfsandwich_type = models.ForeignKey(
        "PdfSandwichType",
        related_name="pdfsandwich_emails",
        null=True,
        blank=False,
        default=None,
        on_delete=models.CASCADE,
    )

    language = models.CharField(
        verbose_name=_("Language"),
        max_length=80,
        choices=languages,
        null=False,
        blank=False,
    )

    subject = models.CharField(
        verbose_name=_("Subject"), max_length=512, blank=False, null=False,
    )

    template = models.TextField(
        verbose_name=_("Background template"),
        blank=False,
        null=False,
        default="Dear {{name}},<br/>\n<a href='{{download_link|safe}}'>Here is your pdfsandwich.</a><br/>\n{{download_link|safe}}<br/>\nBye",
    )
