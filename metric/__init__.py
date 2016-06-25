import numpy as np
import pandas as pd

def loadcsv():
  quality_df  = pd.read_csv("metric/data/hospital_quality_full.csv")
  print (">>>>>>CSV is loaded<<<<<<<")
  return 1 

#loadcsv()


