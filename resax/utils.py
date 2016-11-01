# coding: utf-8

from __future__ import unicode_literals

from datetime import timedelta

def iter_daterange(start_date, end_date):
    for offset in range((end_date - start_date).days):
        yield start_date + timedelta(days=offset)
