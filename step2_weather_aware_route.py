import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

GRID_SIZE = 10
START = (0, 0)
END = (9, 9)

BASE_COST = 1
WIND_FACTOR = 0.5
CURRENT_FACTOR = 0.7

def generate_environment(size):
    wind_field = np.random.uniform(-1, 1, (size, size))
    current_field = np.random.uniform(-1, 1, (size, size))
    return wind_field, current_field

def create_ocean_grid(size, wind_field, current_field):
    G = nx.grid_2d_graph(size, size)

    for (u, v) in G.edges():
        x, y = u

        wind_effect = wind_field[x][y]
        current_effect = current_field[x][y]

        fuel_cost = BASE_COST + (WIND_FACTOR * wind_effect) - (CURRENT_FACTOR * current_effect)

        if fuel_cost < 0.1:
            fuel_cost = 0.1

        G.edges[u, v]['weight'] = fuel_cost

    return G

def calculate_total_fuel(path, graph):
    total = 0
    for i in range(len(path)-1):
        total += graph.edges[path[i], path[i+1]]['weight']
    return total

def main():
    wind_field, current_field = generate_environment(GRID_SIZE)
    ocean_graph = create_ocean_grid(GRID_SIZE, wind_field, current_field)

    optimized_path = nx.shortest_path(ocean_graph, START, END, weight='weight')
    optimized_fuel = calculate_total_fuel(optimized_path, ocean_graph)

    print("Weather-Aware Optimized Route Generated")
    print("Total Fuel Cost:", round(optimized_fuel, 2), "units")

    pos = dict((n, n) for n in ocean_graph.nodes())
    nx.draw(ocean_graph, pos, node_size=20)
    path_edges = list(zip(optimized_path, optimized_path[1:]))
    nx.draw_networkx_edges(ocean_graph, pos, edgelist=path_edges, edge_color='g', width=2)
    plt.title("Fuel-Optimized Route (Weather Aware)")
    plt.show()

if __name__ == "__main__":
    main()
