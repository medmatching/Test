from django.http import Http404
from django.http import HttpResponse
#from .models import Album
from django.shortcuts import render
from django.views.generic import FormView
import numpy
import pandas as pd
import ConfigParser
from .forms import NameForm
import os
from django.conf import settings
import googlemaps
import json
from pandas.io.json import json_normalize
from django.utils.safestring import mark_safe
from django.template import Library
from pyzipcode import ZipCodeDatabase
import json
import pickle
import re

register = Library()
@register.filter(is_safe=True)

map_file = os.path.join(settings.STATIC_ROOT, '/Users/trendini/backend/medmatch/metric/static/metric/data/condition2metric.csv')

mapping_df        = pd.read_csv(map_file)
condition_measures_df = mapping_df[ mapping_df['condition'] == condition ]


