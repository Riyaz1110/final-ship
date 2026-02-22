import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

GRID_SIZE = 10
START = (0, 0)
END = (9, 9)

def create_ocean_grid(size):
    G = nx.grid_2d_graph(size, size)
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = 1
    return G

def calculate_fuel(distance, fuel_rate_per_unit=5):
    return distance * fuel_rate_per_unit

def main():
    ocean_graph = create_ocean_grid(GRID_SIZE)

    shortest_path = nx.shortest_path(ocean_graph, START, END, weight='weight')
    distance = nx.shortest_path_length(ocean_graph, START, END, weight='weight')

    fuel_used = calculate_fuel(distance)

    print("Baseline Shortest Route Generated")
    print("Distance:", distance, "units")
    print("Estimated Fuel Used:", fuel_used, "tons")

    pos = dict((n, n) for n in ocean_graph.nodes())
    nx.draw(ocean_graph, pos, node_size=20)
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    nx.draw_networkx_edges(ocean_graph, pos, edgelist=path_edges, edge_color='r', width=2)
    plt.title("Baseline Shortest Path Route")
    plt.show()

if __name__ == "__main__":
    main()
