
import geopandas as gpd
import gerrychain as gc
from gerrychain import Graph, Partition, MarkovChain, proposals, accept, constraints, GeographicPartition, updaters, graph
from gerrychain.updaters import cut_edges
import pandas as pd
from shapely.geometry import shape
import chardet

# with open('alamedacounty_fixedcommas.csv', 'rb') as f:
#     result = chardet.detect(f.read(10000))
#
# # Print the detected encoding
# print(result['encoding'])

gdf = gpd.read_file("run it back/AlaToData.shp")
gdf = gdf.to_crs("EPSG:32610")
pop_df = pd.read_csv('alamedacounty_fixedcommas.csv', encoding='ISO-8859-1')
pop_df['NAME'] = pop_df['NAME'].astype(str)

geo_pop_gdf = gdf.merge(pop_df, on='NAME')

graph = gc.Graph.from_geodataframe(geo_pop_gdf)
partition = GeographicPartition(graph, 'NAME')
