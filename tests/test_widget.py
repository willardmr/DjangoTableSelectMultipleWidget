#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-table-select-widget
------------

Tests for `django-table-select-widget` models module.
"""

import django
from django import forms
from django.test import TestCase

from model_mommy import mommy

from table_select_widget import TableSelectMultiple

from .models import Choice


class TestTableSelectWidget(TestCase):
    def setUp(self):
        mommy.make(
            "Choice",
            name="Choice 1",
            description="Choice 1 description",
            choice_type__name="Foo type",
        )

    maxDiff = None

    def test_widget(self):
        class ChoiceForm(forms.Form):
            choice_field = forms.ModelMultipleChoiceField(
                queryset=Choice.objects.all(),
                widget=TableSelectMultiple(
                    item_attrs=[
                        'name',
                        'description',
                    ],
                ),
            )
        render = ChoiceForm().as_p()
        self.assertHTMLEqual(
            '<p>'
            '    <label for="id_choice_field">Choice field:</label>'
            '    <table id=choice_field class="display">'
            '        <thead>'
            '            <tr>'
            '                <th class="no-sort"></th>'
            '                <th>Name</th>'
            '                <th>Description</th>'
            '            </tr>'
            '        </thead>'
            '        <tbody>'
            '            <tr>'
            '                <td>'
            '                    <input '
            '                        class='
            '                        "tableselectmultiple selectable-checkbox"'
            '                        id="id_choice_field_0"'
            '                        name="choice_field"'
            '                        type="checkbox"'
            '                        value="1"'
            '                        {}'
            '                        />'
            '                </td>'
            '                <td>Choice 1</td><td>Choice 1 description</td>'
            '            </tr>'
            '        </tbody>'
            '    </table>'
            '    <script>'
            '    </script>'
            '</p>'.format("required" if django.VERSION > (1,10,0) else ""),
            render,
        )

    def test_widget_datatables(self):
        class ChoiceForm(forms.Form):
            choice_field = forms.ModelMultipleChoiceField(
                queryset=Choice.objects.all(),
                widget=TableSelectMultiple(
                    item_attrs=['name'],
                    enable_datatables=True,
                ),
            )
        render = ChoiceForm().as_p()
        self.assertTrue("$('#choice_field').DataTable({" in render)

    def test_widget_bootstrap(self):
        class ChoiceForm(forms.Form):
            choice_field = forms.ModelMultipleChoiceField(
                queryset=Choice.objects.all(),
                widget=TableSelectMultiple(
                    item_attrs=['name'],
                    bootstrap_style=True,
                ),
            )
        render = ChoiceForm().as_p()
        self.assertTrue("form-check-input" in render)
        self.assertTrue("table table-sm table-bordered" in render)

    def test_widget_shift_select(self):
        class ChoiceForm(forms.Form):
            choice_field = forms.ModelMultipleChoiceField(
                queryset=Choice.objects.all(),
                widget=TableSelectMultiple(
                    item_attrs=['name'],
                    enable_shift_select=True,
                ),
            )
        render = ChoiceForm().as_p()
        self.assertTrue("$.fn.shiftClick = function () {" in render)

    def test_widget_related(self):
        """ Test, that function on related field is called """
        class ChoiceForm(forms.Form):
            choice_field = forms.ModelMultipleChoiceField(
                queryset=Choice.objects.all(),
                widget=TableSelectMultiple(
                    item_attrs=[('choice_type__get_name', 'Type')],
                ),
            )
        render = ChoiceForm().as_p()
        self.assertTrue("<th>Type</th>" in render)
        self.assertTrue("<td>Type: Foo type</td>" in render)

    def test_widget_none(self):
        """ If value of variable is null, render it as blank cell """
        mommy.make(
            "Choice",
            name="Choice 2",
            description=None,
        )
        class ChoiceForm(forms.Form):
            choice_field = forms.ModelMultipleChoiceField(
                queryset=Choice.objects.all(),
                widget=TableSelectMultiple(
                    item_attrs=['description'],
                ),
            )
        render = ChoiceForm().as_p()
        self.assertTrue("</td><td></td></tr>" in render)
