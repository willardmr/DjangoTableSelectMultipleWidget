from string import capwords

from django.forms import CheckboxInput, SelectMultiple
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe


SHIFT_SELECT_JS = '''
$.fn.shiftClick = function () {
    var lastSelected; // Firefox error: LastSelected is undefined
    this.each(function () {
        $(this).click(function (event) {
            if (event.shiftKey) {
                var checkBoxes = $(".selectable-checkbox");
                var last = checkBoxes.index(lastSelected);
                var first = checkBoxes.index(this);
                var start = Math.min(first, last);
                var end = Math.max(first, last);
                var chk = lastSelected.checked;
                for (var i = start; i <= end; i++) {
                    checkBoxes[i].checked = chk;
                    $(checkBoxes[i].closest("tr")).toggleClass('active', chk);
                }
            } else {
                lastSelected = this;
            }
            $(this).closest("tr").toggleClass(
                'active', $(this).is(":checked")
            );
        })
    });
};
$('.selectable-checkbox').shiftClick();
'''

# Note: Paging cannot be easily turned on,
# because otherwise the checkboxes on unvisible pages are not in the request.
DATATABLES_JS = '''
$(document).ready(function(){{
    $('#{}').DataTable({{
        "order": [],
        "paging": false,
        "searching": false,
        "columnDefs": [{{
            "targets"  : 'no-sort',
            "orderable" : false,
        }}]
    }});
}});
'''


class TableSelectMultiple(SelectMultiple):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.
    Only for use with a ModelMultipleChoiceField
    """
    def __init__(
        self,
        item_attrs,
        enable_shift_select=False,
        enable_datatables=False,
        bootstrap_style=False,
        *args,
        **kwargs
    ):
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
        self.enable_shift_select = enable_shift_select
        self.enable_datatables = enable_datatables
        self.bootstrap_style = bootstrap_style

    def render(self, name, value,
               attrs=None, choices=()):
        if value is None:
            value = []
        output = []
        table_classes = "display"
        if self.bootstrap_style:
            table_classes += " table table-sm table-bordered"
        output.append(
            '<table id={} class="{}">'.format(escape(name), table_classes),
        )
        head = self.render_head()
        output.append(head)
        body = self.render_body(name, value, attrs)
        output.append(body)
        output.append('</table>')
        output.append('<script>')
        if self.enable_shift_select:
            output.append(SHIFT_SELECT_JS)
        if self.enable_datatables:
            output.append(DATATABLES_JS.format(escape(name)))
        output.append('</script>')
        return mark_safe('\n'.join(output))

    def render_head(self):
        output = []
        output.append('<thead><tr><th class="no-sort"></th>')
        for item in self.item_attrs:
            name = item if isinstance(item, str) else item[1]
            output.append(
                '<th>{}</th>'.format(clean_underscores(escape(name))),
            )
        output.append('</tr></thead>')
        return ''.join(output)

    def render_body(self, name, value, attrs):
        output = ['<tbody>']
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs)
        final_attrs['class'] = "tableselectmultiple selectable-checkbox"
        if self.bootstrap_style:
            final_attrs['class'] += " form-check-input"
        str_values = set([force_text(v) for v in value])
        choice_pks = [pk for (pk, item) in self.choices]
        choices = self.choices.queryset.filter(pk__in=choice_pks)
        for i, item in enumerate(choices):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(
                    final_attrs, id='{}_{}'.format(attrs['id'], i),
                )
            cb = CheckboxInput(final_attrs,
                               check_test=lambda value: value in str_values)
            option_value = force_text(item.pk)
            rendered_cb = cb.render(name, option_value)
            output.append('<tr><td>{}</td>'.format(rendered_cb))
            for item_attr in self.item_attrs:
                attr = item_attr \
                    if isinstance(item_attr, str) \
                    else item_attr[0]
                content = get_underscore_attrs(attr, item)
                output.append('<td>{}</td>'.format(escape(content)))
            output.append('</tr>')
        output.append('</tbody>')
        return ''.join(output)


def get_underscore_attrs(attrs, item):
    for attr in attrs.split('__'):
        if callable(attr):
            item = attr(item)
        elif callable(getattr(item, attr)):
            item = getattr(item, attr)()
        else:
            item = getattr(item, attr)
    if item is None:
        return ""
    return item


def clean_underscores(string):
    """
    Helper function to clean up table headers.  Replaces underscores
    with spaces and capitalizes words.
    """
    s = capwords(string.replace("_", " "))
    return s
