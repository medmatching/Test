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
import sys

register = Library()
@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))




def index(request):
    print ("inside index fo form")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'metric/index.html', {'form': form})


def get_name(request):
  print (">>>>>>>>>Index<<<<<<")
  #all_albums = Album.objects.all()
  context  = { 'context': "nocontext", }
  #response = HttpResponse(contenttype="text/html")
  #content = "".join(open("/Users/trendini/MedMatch/medmatching.html").readlines())
  #response = HttpResponse( content )
  #print (content)
  #response._set_content(content)
  #return response
  return render(request, 'metric/index.html', context) 


def detail(request):
  print (">>>>>>>>>Detail<<<<<<<")
  #all_albums = Album.objects.all()
  zipcode   = request.GET['zipcode']
  condition = request.GET['condition']
  #new_condition = "Heart Attack or Chest Pain" 
  new_condition  = condition
 
  ## **REZA** find how static root should be set
  csv_file = os.path.join(settings.STATIC_ROOT, '/Users/trendini/backend/medmatch/metric/static/metric/data/ny_hq.csv')
  map_file = os.path.join(settings.STATIC_ROOT, '/Users/trendini/backend/medmatch/metric/static/metric/data/condition2metric.csv')
  print(csv_file)
  quality_df  = pd.read_csv(csv_file)
  zcdb = ZipCodeDatabase()
  zipc_info     = zcdb[int(zipcode)]
  city_ofzip  = (zipc_info.city).upper()
  #zip_df      = quality_df[ quality_df['ZIP.Code'] == int(zipcode) ]
  #indexlist   = zip_df.index.tolist()
  #index       = indexlist[0]
  #city        = zip_df['City'][index]
  metric2code_file  = os.path.join(settings.STATIC_ROOT, '/Users/trendini/backend/medmatch/metric/static/metric/data/metric2code')
  mapping_df        = pd.read_csv(map_file)
  condition_measures_df = mapping_df[ mapping_df['condition'] == new_condition ]
  print ( condition_measures_df )
  print ("---------------------------------------------------")
  payment_code = condition_measures_df['payment'].iloc[0]
  mortality_code = condition_measures_df['mortality'].iloc[0]
  readmission_code = condition_measures_df['readmission'].iloc[0]
  print ( payment_code )
  print ( mortality_code )
  print ( readmission_code )
  print ("---------------------------------------------------")

  measure_payment      = 'Payment.'+ payment_code
  measure_mortality    = 'Score.'  + mortality_code
  measure_readmission  = 'Score.'  + readmission_code

  measure_payment_rel      = 'Payment.category.'+ payment_code
  measure_mortality_rel    = 'Compared.to.National.'  + mortality_code
  measure_readmission_rel  = 'Compared.to.National.'  + readmission_code



  #metric2code_h     = open(metric2code_file, 'rb')
  #metric2code_dict  = pickle.load(metric2code_h)
  #measure_name      = metric2code_dict [ condition ]
  #measure_code      = measure_name.split('Measure.Name.', 1)[1]
  #measure_score     = 'Score.'+ measure_code
  #measure_score_rel = 'Compared.to.National.'+ measure_code		## score compared to national average
  
  print ( city_ofzip )
   
  city_df     = quality_df[ quality_df['City'] == city_ofzip ]

  if ( payment_code != 'Not Available' ):
    table_df    = city_df [ ['Hospital.Name', 'Address', 'City', 'State', 'Emergency.Services', 
				measure_payment, measure_payment_rel, measure_mortality, measure_mortality_rel, measure_readmission, measure_readmission_rel ] ]
  else:
    table_df    = city_df [ ['Hospital.Name', 'Address', 'City', 'State', 'Emergency.Services', 
				measure_mortality, measure_mortality_rel, measure_readmission, measure_readmission_rel ] ]
 
  #table_df.rename(columns={measure_score: condition, measure_score_rel:'Compared to National Average'}, inplace=True)


  table_df.reset_index(drop=True, inplace=True)

  table_df['lat'] = 0
  table_df['lng'] = 0
  
# Replace the API key below with a valid API key.
  gmaps = googlemaps.Client(key='AIzaSyBRKYSSAzH271QZvtFdhUaf-0iqHn6-Gz4')

  center = []
  # Geocoding and address
  geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
  #geocode_result = gmaps.geocode(city_df['Address'][1]+" "+city_df['City'][1]+" "+city_df['Country'][1])
  for index in range(len(table_df.index)):
    geocode_result = gmaps.geocode(table_df['Address'][index]+", "+table_df['City'][index]+", "+table_df['State'][index])
    lat  = geocode_result[0]['geometry']['location']['lat']
    lang = geocode_result[0]['geometry']['location']['lng']
    print( lang  )
    center.insert(index,{'lat':lat, 'lng':lang, 'hospitalname':table_df['Hospital.Name'][index] })

  center = json.dumps(center)

  del table_df['lat']
  del table_df['lng']
  del table_df['State']

  print ( table_df ) 
  
  #sys.exit()
 
  ## sql injection 
  context = {'data':table_df.to_html(classes='tablesorter" id ="hospitallist'), 'center': center }

  
  return render(request, "metric/googlemap.html", context )


def loadcsv():
  #zipcode    = context['zipcode']
  #condition  = context['condition']
  print (">>>>>>CSV is loaded<<<<<<<")
  return 1 

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1 



#  try:
#    album = Album.objects.get(id=album_id)
#  except Album.DoesNotExist:
#    raise Http404("Album does not exist")
#  return render(request, 'metric/detail.html', { 'album': album, }) 
