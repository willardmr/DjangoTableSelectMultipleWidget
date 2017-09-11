# DjangoTableSelectMultipleWidget
A Django widget for use with a ModelMultipleChoiceField to allow easy jQuery DataTables sorting and pagination by rendering the selector as a table.

![Table select widget screenshot](https://raw.githubusercontent.com/PetrDlouhy/DjangoTableSelectMultipleWidget/master/table_select_widget.png "Table select widget screenshot (with datables and bootstrap enabled")

## Installation

```bash
pip install django-table-select-widget
```

Example form field:
```python
from table_select_widget import TableSelectMultiple

items = forms.ModelMultipleChoiceField(
    queryset=myqueryset,
    widget=TableSelectMultiple(
       item_attrs=[
           'tablecolumn1',
           ('tablecolumn2', "Table coulmn 2 header"),
           'same__related__parameter',
       ],
       enable_shift_select=True,
       enable_datatables=True,
       bootstrap_style=True,
       datatable_options={'language': {'url': '/foobar.js'}},
    ),
)
```
        
Render it normally with a Django form.

### Parameters

#### `enable_shift_select`
Default: `False`

If `True`, it inserts JavaScripts, that enables shift-selection of multiple checkboxes. JQuery is required to be activated for this feature.

#### `enable_datatables`
Default: `False`

If `True`, it inserts JavaScripts, that enables DataTables for the select table. JQuery and DataTables is required to be activated for this feature:
```javascript
<script src="https://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.7/css/jquery.dataTables.css"></link>
</script>
```

#### `bootstrap_style`
Default: `False`

If `True`, it inserts BootStrap classes to the table.

#### `datatable_options`
Default: `{}`

Dictionary with additional parameters which will be passed to DataTable initialization.
These options will get formated by `json.dumps`, so it can contain more complex structures.
Default parameter values set by `DjangoTableSelectMultipleWidget` can be overriden by this parameter.


## Origin

Modified from https://djangosnippets.org/snippets/518/ for use with Python 3, Django 1.7.


Very similar to my TableSelect widget found here: https://github.com/willardmr/DjangoTableSelectWidget
