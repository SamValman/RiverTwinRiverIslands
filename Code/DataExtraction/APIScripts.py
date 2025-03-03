# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:15:53 2023

@author: lgxsv2
"""

import json
import os
import requests
from requests.auth import HTTPBasicAuth
import pathlib
import time

# key from Planet
os.environ['PL_API_KEY']= ***PUT KEY HERE

# API Key stored as an env variable
PLANET_API_KEY = os.getenv('PL_API_KEY')


orders_url = 'https://api.planet.com/compute/ops/orders/v2'


# set up requests to work with api
auth = HTTPBasicAuth(PLANET_API_KEY, '')
headers = {'content-type': 'application/json'}

# The product I want to download, mostly copied from https://developers.planet.com/docs/integrations/gee/delivery/
# Changed name to the island im downloading "bimini_1"
# changed item ids to just two images to check 
# changed the co-ordinates to those used on the standard download to hardrive which worked before
# changed project name 
# changed collection name 

t_gee_product = {
  "name": "DS_13_2023",
  "products": [
    {
      "item_ids": [
"20180930_152557_1018",
"20180913_152517_1033"
      ],
      "item_type": "PSScene4Band",
      "product_bundle": "analytic_sr"
    }
  ],
  "tools": [
    {
      "clip": {
        "aoi": { 
            "type": "Polygon",
            "coordinates": The json would go here?
        }
      }
    }
  ],
  "delivery": {
    "google_earth_engine": {
      "project": "projects/ee-samuelvalman/assets/",
      "collection": "Bahamas"
    }
  }
}


# function to order the product (I didn't write any of this)
def place_order(request, auth):
    response = requests.post(orders_url, data=json.dumps(request), auth=auth, headers=headers)
    print(response)
    order_id = response.json()['id']
    print(order_id)
    
    
    
    
# call function expecting <Response [202]>
place_order(t_gee_product, auth)   

###############################################################################
# Will need to run the below section in comand line after changing order number below
###############################################################################

# theres probably an easier way of doing this but I just copied the order number from above
orders_url = 'https://api.planet.com/compute/ops/orders/v2'
o_url = orders_url + '/7a2e5f3a-df37-4f8f-a0a7-bcf97dcdd059'


# checks status of order - order fails eventually

def poll_for_success(order_url, auth, num_loops=30):
    count = 0
    while(count < num_loops):
        count += 1
        r = requests.get(order_url, auth=auth)
        response = r.json()
        state = response['state']
        print(state)
        end_states = ['success', 'failed', 'partial']
        if state in end_states:
            break
        time.sleep(10)
        
poll_for_success(o_url, auth)