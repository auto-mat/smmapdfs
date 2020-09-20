# -*- coding: utf-8 -*-

import re

from django.conf import settings
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):

        super().__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            self.rel_to_name = ' '.join(
                re.findall('[A-Z][^A-Z]*', rel_to.__name__),
            ).lower()

            app, model = (
                rel_to._meta.app_label,
                rel_to._meta.object_name.lower(),
            )
            related_url = "admin:{app}_{model}".format(
                app=app, model=model,
            )

        self.related_url = related_url
        self.url_query = '?_to_field=id&_popup=1'

    def render(self, name, value, *args, **kwargs):
        related_url_add = reverse(self.related_url + '_add')
        related_url_add += self.url_query
        output = [super().render(name, value, *args, **kwargs)]
        output.append(
            """<a href="{url}"
            class="related-widget-wrapper-link change-related"
            id="add_id_{name}" onclick="return showAddAnotherPopup(this);">
            """.format(
                url=related_url_add,
                name=name,
            ),
        )
        output.append(
            """<img src="{url}admin/img/icon-addlink.svg"
            width="13" height="13" alt="_('Add selected %(model)s') %
            {{'model': {name}}}"/></a>
            """.format(
                url=settings.STATIC_URL,
                name=self.rel_to_name,
            ),
        )

        return mark_safe(''.join(output))


class RelatedFieldWidgetCanAddAndUpdate(RelatedFieldWidgetCanAdd):

    def render(self, name, value, *args, **kwargs):
        related_url_change = reverse(
            self.related_url + '_change',
            args=[value],
        )
        url_query = '?_to_field=id&_popup=1'
        related_url_change += url_query
        output = [super().render(name, value, *args, **kwargs)]
        output.append(
            """<a href="{url}"
            class="related-widget-wrapper-link change-related"
            id="change_id_{name}" onclick="return showAddAnotherPopup(this)
            ;">""".format(
                url=related_url_change,
                name=name,
            ),
        )
        output.append(
            """<img src="{url}admin/img/icon-changelink.svg"
            width="13" height="13" alt="_('Change selected %(model)s') %
            {{'model': {name}}}"/></a>
            """.format(
                url=settings.STATIC_URL,
                name=self.rel_to_name,
            ),
        )
        return mark_safe(''.join(output))
