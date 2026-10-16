"""
Case study for further e-bike adoption
"""
import psycopg2
import os
from dotenv import load_dotenv
from modules import category_processing, network_preparation, network_processing, network_reduction, final_table_creation, poidpy_trip_generation, trip_distribution
import time
from sqlalchemy import create_engine

import pandas as pd
import geopandas as gpd

load_dotenv()

DB_CONFIG = {
    'host': 'localhost',
    'dbname': os.getenv("POSTGRES_DB"),
    'user': os.getenv("POSTGRES_USER"),
    'password': os.getenv("POSTGRES_PASSWORD"),
    'port': 5432
}

city_list = ["Greater Graz"]
pois_table_name = "pois_greater_graz" 
NUM_ODS = 100 *1000


for index,city in enumerate(city_list):
    
    print("city")
    conn = psycopg2.connect(**DB_CONFIG)

    category_processing.create_cycling_categories(conn)
    network_preparation.pgrouting_start(conn)

    network_preparation.prepare_network(conn, city, out_edge_table = "temp_raw_edges")
    network_preparation.intersect_network(conn,in_edge_table = "temp_raw_edges", out_edge_table = "temp_edges")
    network_processing.network_creation(conn, edge_table = "temp_edges", vertex_table="temp_vertices")
    network_processing.keep_main_component(conn, in_edge_table = "temp_edges", vertex_table = "temp_vertices", component_table = "temp_comp_table", out_edge_table = "temp_filtered_edges")
    network_processing.remove_dead_ends(conn,edge_table = "temp_filtered_edges", vertex_table = "temp_vertices", num_it = 5)
    network_processing.simplify_network(conn,in_edge_table = "temp_filtered_edges", out_edge_table = "temp_filtered_edges", vertex_table="temp_vertices")



    network_reduction.create_grid_table(conn, city_name = city, 
                                        grid_size = 2000, grid_table_name = "temp_grid", vertex_table = "temp_vertices")

    
    conn.commit()
    conn.close()
    
    start_time = time.time()

    engine = create_engine(f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
                    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")

    zones_gdf = poidpy_trip_generation.poidpy_trip_generation(engine, grid_table = "temp_grid", pois_table_name = pois_table_name)
    
    # Uncomment if want to save zones.csv from Poidpy and reuse later
    zones_gdf.to_csv(city + "_zones.csv", index=False)

        

    trip_distribution.sample_od_pairs(engine, zones_gdf, grid_table = "temp_grid", vertex_table = "temp_vertices", 
    number_ods= NUM_ODS,pois_table_name = pois_table_name, selected_ods_table = "greater_graz_selected_ods_lambda_7",
     use_zones = True, use_distances = True, random_destination = False)


    trip_distribution.sample_od_pairs(engine, zones_gdf, grid_table = "temp_grid", vertex_table = "temp_vertices", 
    number_ods= NUM_ODS,pois_table_name = pois_table_name, selected_ods_table = "greater_graz_selected_ods_lambda_9",
     use_zones = True, use_distances = True, random_destination = False, lambda_weibull = 9)


    conn = psycopg2.connect(**DB_CONFIG)


    network_reduction.calculate_edge_percentiles(conn, starting_seed = 0.4, edge_table = "temp_filtered_edges", 
                                                 out_table = "greater_graz_lambda_7",selected_ods_table = "greater_graz_selected_ods_lambda_7",num_ods = NUM_ODS * 2,
                                                 include_different_sensitivity = True)


        
    network_reduction.gap_filling(conn, num_iterations = 50, edge_table = "greater_graz_lambda_7", interval_length = 5)

    # final_table_creation.add_city(conn, city_name = city, final_table_name = "final_table", 
    #                               city_table_name = "temp_city_table")
    

    network_reduction.calculate_edge_percentiles(conn, starting_seed = 0.4, edge_table = "temp_filtered_edges", 
                                                 out_table = "greater_graz_lambda_9",selected_ods_table = "greater_graz_selected_ods_lambda_9",num_ods = NUM_ODS * 2,
                                                 include_different_sensitivity = True)

    network_reduction.gap_filling(conn, num_iterations = 50, edge_table = "greater_graz_lambda_9", interval_length = 5)

    conn.commit()
    conn.close()
    
    
        

    print("--- %s seconds ---" % (time.time() - start_time))

