from string import capwords
from django.forms import CheckboxInput, SelectMultiple, Select
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe
from datetime import datetime
from django.utils import timezone


class TableSelectMultiple(SelectMultiple):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.
    Only for use with a ModelMultipleChoiceField
    """
    def __init__(self, item_attrs, *args, **kwargs):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callables in item_attrs will be called with the item to be
            displayed as the sole parameter.

            Any callable attribute names specified will be called and have
            their return value used for display.

            All attribute values will be escaped.
        """
        super(TableSelectMultiple, self).__init__(*args, **kwargs)
        self.item_attrs = item_attrs

    def render(self, name, value,
               attrs=None, choices=()):
        if value is None:
            value = []
        output = []
        output.append('<table id={} class="display">'.format(escape(name)))
        head = self.render_head()
        output.append(head)
        body = self.render_body(name, value, attrs)
        output.append(body)
        output.append('</table>')
        return mark_safe('\n'.join(output))

    def render_head(self):
        output = []
        output.append('<thead><tr><th class="no-sort"></th>')
        for item in self.item_attrs:
            output.append('<th>{}</th>'.format(clean_underscores(escape(item))))
        output.append('</tr></thead>')
        return ''.join(output)

    def render_body(self, name, value, attrs):
        output = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        str_values = set([force_text(v) for v in value])
        for i, (pk, item) in enumerate(self.choices):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='{}_{}'.format(attrs['id'], i))
            item = self.choices.queryset.get(pk=pk)
            cb = CheckboxInput(final_attrs,
                               check_test=lambda value: value in str_values)
            option_value = force_text(pk)
            rendered_cb = cb.render(name, option_value)
            output.append('<tr><td>{}</td>'.format(rendered_cb))
            for attr in self.item_attrs:
                if callable(attr):
                    content = attr(item)
                elif callable(getattr(item, attr)):
                    content = getattr(item, attr)()
                else:
                    content = getattr(item, attr)
                output.append('<td>{}</td>'.format(escape(content)))
            output.append('</tr>')
        output.append('</tbody>')
        return ''.join(output)
        
def clean_underscores(string):
    """
    Helper function to clean up table headers.  Replaces underscores
    with spaces and capitalizes words.
    """
    s = capwords(string.replace("_", " "))
    return s
