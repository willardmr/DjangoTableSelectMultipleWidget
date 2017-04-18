#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.gis.db import models


class ChoiceType(models.Model):
    name = models.CharField(max_length=255)

    def get_name(self):
        return "Type: {}".format(self.name)


class Choice(models.Model):
    name = models.CharField(max_length=255)
    choice_type = models.ForeignKey(ChoiceType)
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
