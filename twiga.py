#!/usr/bin/env python
# coding: utf-8

# # Heat Stress Indices

# In[1]:


#############################
# Load some libraries       #
#############################
import requests
import json
import datetime
import pandas as pd
import matplotlib
import numpy as np

import pprint
pp = pprint.PrettyPrinter(depth=1)

# plot figures directly into the notebook
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#############################
# TWIGA API settings        #
#############################

# The HydroNET/TWIGA API endpoint
api = 'https://hnapi.hydronet.com/api/'

# The bearer token for the TWIGA user
# this token is used to identify as a valid TWIGA user to the API
api_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJZX2pEcG9IWUY3b3lxOWxsVVFoRTlqUTVwb0NfdkZ6MVQ0V19pTW00encwIn0.eyJleHAiOjE2NjY0MTYwMDgsImlhdCI6MTYzNDg4MDAwOCwianRpIjoiMWJlZmFkNzEtNWNlMy00NzZiLWJkNzEtOWI5ZGMxMjVjYWMxIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5oeWRyb25ldC5jb20vYXV0aC9yZWFsbXMvaHlkcm9uZXQiLCJhdWQiOlsicG9ydGFsLmJhY2tlbmQuYXBpIiwiYWNjb3VudCJdLCJzdWIiOiI3Njg2ZmZiMy02NzRjLTRiMzEtYTdkZi0zYjNmZTJhYzQ4MTkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhcGktaHlkcm9uZXQtdHdpZ2EiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJjbGllbnRJZCI6ImFwaS1oeWRyb25ldC10d2lnYSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiY2xpZW50SG9zdCI6IjE5Mi4xNjguMTIuMTEyOjYwMTcyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWFwaS1oeWRyb25ldC10d2lnYSIsImNsaWVudEFkZHJlc3MiOiIxOTIuMTY4LjEyLjExMjo2MDE3MiJ9.p13NIP-_zpr7NOJ1i2r9JeIhBi-Sj_c1p12OWL7eENYWsSwOPohgjTrKsFLgtoJKqmmzUcFWnJ7xjs8VIq5iMYgCur0VPA0dTp3ngBCGUc_9hXjbhvPScMmJJ_cZQE-FCJYtuQubA2BFKwaaFYIj-7sp8Hr74ikfMRReRBUFt8C3LdowoJz5WJTpzbQvK_rFnGkscG8NxGziEghU5AchNliJhdqqUVVOcudN43i4rxK1kX2WPfYF_JlYQdYVs4DmqF8xoA4Lzay7QH3-0hEGvsspxRPMCGWcEkWKIrmXUwuzGhsVS1g-wO6pvA6-2XFEo3erHqtdeyN7DaMWPu4mtw'

# Using the token, generate a valid header for requests to the API
api_header = {'content-type': 'application/json', 'Authorization': 'bearer ' + api_token}


# In[3]:


# an empty request which can be send to the TWIGA API
datasource_metadata = {}

# Send the request to the datasources endpoint of the API
datasource_response = requests.post(api + 'entity/datasources/get', headers=api_header, data=json.dumps(datasource_metadata))

# The response of the API is in JSON. Parse this with Python
datasource_metadata = datasource_response.json()

# print the result, as indented json
pp.pprint(json.dumps(datasource_metadata, indent=2))


# In[ ]:





# In[4]:


# The API returns a JSON with all the information
# this JSON is parsed into a python dictionary
# the raw data above shows that there is a key called DataSources
# this key can be referenced, to get the total number of available data sources
print(f"There are a total of {len(datasource_metadata['DataSources'])} datasources in the API\n")
# which gives you a total of 21 data sources as the time of writing

# as the json is parsed as a dictionary, we can extract information using the keys
print("The datasources codes/names are:")
for key, value in datasource_metadata["DataSources"].items() :
    print(key)


# In[22]:


# From the response of the TWIGA API we can see that
# there are two twiga data sources
# twiga.Stations.Data.Distribution.Hourly and twiga.Stations.Data.Distribution.Measurements

# the first provides hourly values, the second provides higher resolution data (i.e. 5 minute intervals)

# store the selected data source code

selected_datasource_code = "Twiga.Heatstress.Forecast"

# json request to ask metadata of a single datasource
request_metadata_twiga= {
     "DataSourceCodes": [selected_datasource_code]
}

# Send the request to the datasources endpoint of the API
datasource_twiga_response = requests.post(api + 'entity/datasources/get', headers=api_header, data=json.dumps(request_metadata_twiga))

# The response of the API is in JSON. Parse this with Python
datasource_twiga_metadata = json.loads(datasource_twiga_response.content.decode('utf-8-sig'))

# print the result, as indented json
print(json.dumps(datasource_twiga_metadata, indent=2))


# In[27]:


df1=pd.json_normalize(datasource_twiga_metadata)
df1.info()


# In[30]:


df1.shape
df1


# In[16]:


# twiga stations are spread over continental Africa
# we can ask the available locations through the TWIGA API

# again we define a JSON request which we can send the the TWIGA API
request_locations_twiga = {
     "DataSourceCodes": [selected_datasource_code]
}

# This time we send the request to the variables endpoint of the API
locations_twiga_response = requests.post(api + 'entity/locations/get', headers=api_header, data=json.dumps(request_locations_twiga))

# The response of the API is in JSON. Parse this with Python
locations_twiga = locations_twiga_response.json()

# print the result, as indented json
print(json.dumps(locations_twiga, indent=2))


# In[14]:


# Try to retrieve data of this twiga stations
request_twiga_data = {
    "Readers": [{
        "DataSourceCode": selected_datasource_code,
        "Settings": {
            "VariableCodes": ["P"],
            "StartDate": "20191001000000",
            "EndDate": "20191109000000",
            "StructureType": "TimeSeries"
        }
    }]
}

# send the request to the TWIGA API, this time the modelTimeseries endpoint
data_response = requests.post(api + 'data/get', headers=api_header, data=json.dumps(request_twiga_data))

# parse response into JSON object
twiga_data = data_response.json()

# print the result, as indented json
print(json.dumps(twiga_data, indent=2))


# In[ ]:




