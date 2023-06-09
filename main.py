from functools import partial
import geopandas as gpd
import gerrychain
import gerrychain as gc
import matplotlib.pyplot as plt
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from functools import partial
import pandas as pd
from gerrychain import Graph, Partition, MarkovChain, proposals, accept, constraints, GeographicPartition, updaters, graph
from gerrychain.constraints import within_percent_of_ideal_population, single_flip_contiguous
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Read shapefile
df = gpd.read_file("AlamedaCountyPopCorrected")

# check coord system
# print(df.crs)

# convert coord system
df_utm = df.to_crs("EPSG:32610")

# load graph and population data from graph
graph = gc.Graph.from_geodataframe(df_utm)


# cast Population to integer from string
# remove commas from Population number ie 3,000 - > 3000
df_utm["Population"] = df_utm["Population"].str.replace(",", "")
df_utm["Population"] = df_utm["Population"].astype(int)

total_pop = df_utm["Population"].sum()

graph.add_data(df_utm, columns=["Population"])
graph.add_data(df_utm, columns=["NAME"])

# create copy to filter out tracts of 0 population, not working
# df_filtered = df_utm.copy()
# df_filtered = df_filtered[df_filtered["Population"] > 0]

# define numb of districts, steps, compactness bound of population
districts = 7
steps = 1000
compactness_bound = 0.01

init_partition = Partition(graph, "NAME", {"population": updaters.Tally("Population", alias="population")})
pop_updater = gerrychain.updaters.Tally("population", alias="population")


constraints = [
    # within_percent_of_ideal_population(init_partition, 0.1),
    single_flip_contiguous,
]

plan = Partition(init_partition.graph,"NAME")
population_target = sum(init_partition["population"].values()) / districts
proposal = gc.proposals.propose_random_flip
chain = MarkovChain(
    proposal=proposal,
    constraints=constraints,
    accept=accept.always_accept,
    initial_state=init_partition,
    total_steps=50,
)
#
# # colors = ["red", "blue", "green", "purple", "orange", "yellow", "brown"]
# #
# # # Loop over the chain and plot each partition
for partition in chain:
    plan = Partition(partition.graph, "NAME")
    plan.plot(df_utm, figsize=(10, 10), cmap="tab20")
    plt.axis('off')
    plt.show()


#
#
# print(population_target)
#
plan = Partition(graph, "NAME")
plan.plot(df_utm, figsize=(10, 10), cmap="tab20")
plt.axis('off')
plt.show()
