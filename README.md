# Modeling Bicycle Network Centrality using a 4-Step Model and Open Data to Support Bicycle Infrastructure Development

This repository contains the code for the article Modeling Bicycle Network Centrality using a 4-Step Model and Open Data to Support Bicycle Infrastructure Development, submitted for review to the 2nd World Symposium on Sustainable Transport and Livability (WSSTL-2027)


## Instructions for running the code for a new city.

1) Create a .env file with the following fields:
- POSTGRES_DB="your_db"
- POSTGRES_USER="your_user"
- POSTGRES_PASSWORD="your_password"
  
2)) Find the name, administrative_boundary and country tags for the desired city from [OSM](https://www.openstreetmap.org/). This can be done using the "Query Features" capability of OSM, clicking on a point of the city, and finding the relevant OSM feature in the left pane under "Enclosed Features", as shown in the screenshots below.
   
<img src="https://github.com/user-attachments/assets/8e4f62c6-fb63-4e8e-b140-854dbc6cb66b" style="max-width: 100%; height: auto;" alt="osm_example" />
<img src="https://github.com/user-attachments/assets/2e1aadca-1327-4227-a95c-3406d03366aa"  style="max-width: 100%; height: auto;" alt="image" />

3) Define a Polygon (in EPSG: 4326) to be the city center area. If not already defined, such a Polygon can be created with tools such as QGIS or online tools such as https://wktmap.com/. Add it to the city_center table, as shown in the exampes in src/python/city_center.sql
   
4) Use the script osm_data.py to fetch the bicycle infrastructure data from Overpass API
5) Run main.py with the names of the selected citie(s). This will create a table, called final_table, with the bicycle network and a percentile of each edge, based on the developed 4-step model for bicycle network centrality.

### Other folders included

Other folders included in the repository, not affecting the general workflow to apply the model to a new city: 
- calibration: Contains the code for calibration of the attraction coefficients based on BiciMad bike-sharing data from the city of Madrid.
- validation: Acquisition and processing of datasets used for evaluation in the cities of Graz, Berlin and Hamburg.
- results: Folder to produce the figures contained in the thesis


