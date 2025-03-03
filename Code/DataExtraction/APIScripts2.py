# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:36:00 2023

@author: lgxsv2
"""

import requests
import json

start_date = '2023-07-01T00:00:00Z'
end_date = '2023-10-30T00:00:00Z'
fp_ds = "DataFolder\AoIs\DS_13.geojson" # change to just ds and in getcords function

def getCords(fp):
    with open(fp, 'r') as file:
        data = json.load(file)
    # Extract coordinates from the first feature (or choose the desired feature)
    coords = data['features'][0]['geometry']['coordinates'][0]

    return coords


#%%   





# Define your Planet API key and request URL
api_key = 'KEYYY'
url = 'https://api.planet.com/data/v1/quick-search'

# Define your date range and GeoJSON boundary
coords = getCords(fp_ds)
geometry = {
    "type": "Polygon",
    "coordinates": [coords]
}

# Create the request payload
request_data = {
    "item_types": ["PSScene"],
    "filter": {
        "type": "AndFilter",
        "config": [
            {
                "type": "DateRangeFilter",
                "field_name": "acquired",
                "config": {
                    "gte": start_date,
                    "lte": end_date
                }
            },
            {
                "type": "GeometryFilter",
                "field_name": "geometry",
                "config": geometry
            }
        ]
    }
}

# Set up the request headers
headers = {
    "Authorization": f"api-key {api_key}",
    "Content-Type": "application/json"
}
#%%
# Make the POST request to the Planet API
r = requests.post(url, data=json.dumps(request_data), headers=headers)
#%%
# Check if the request was successful
if r.status_code == 200:
    # Parse the JSON response
    response_data = r.json()
    # Extract and process the image information as needed
    for feature in response_data.get("features", []):
        scene_id = feature["id"]
        
        # Perform actions like downloading the scene using the scene ID or links
        # You can also find download links in the "assets" field of each feature
else:
    print(f"Request to Planet API failed with status code {r.status_code}: {r.text}")
