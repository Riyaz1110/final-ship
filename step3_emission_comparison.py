import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

GRID_SIZE = 10
START = (0, 0)
END = (9, 9)

BASE_COST = 1
WIND_FACTOR = 0.5
CURRENT_FACTOR = 0.7

FUEL_BURN_PER_DAY = 120
EMISSION_FACTOR = 3.114
SPEED_KNOTS = 20
NAUTICAL_MILES_PER_UNIT = 10

def generate_environment(size):
    wind_field = np.random.uniform(-1, 1, (size, size))
    current_field = np.random.uniform(-1, 1, (size, size))
    return wind_field, current_field

def create_shortest_graph(size):
    G = nx.grid_2d_graph(size, size)
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = 1
    return G

def create_weather_graph(size, wind_field, current_field):
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

def calculate_voyage_metrics(path_length_units):
    distance_nm = path_length_units * NAUTICAL_MILES_PER_UNIT
    voyage_hours = distance_nm / SPEED_KNOTS
    voyage_days = voyage_hours / 24
    fuel_used = voyage_days * FUEL_BURN_PER_DAY
    co2_emission = fuel_used * EMISSION_FACTOR
    return fuel_used, co2_emission, voyage_hours

def main():
    wind_field, current_field = generate_environment(GRID_SIZE)

    shortest_graph = create_shortest_graph(GRID_SIZE)
    shortest_path = nx.shortest_path(shortest_graph, START, END, weight='weight')
    shortest_length = nx.shortest_path_length(shortest_graph, START, END, weight='weight')

    weather_graph = create_weather_graph(GRID_SIZE, wind_field, current_field)
    optimized_path = nx.shortest_path(weather_graph, START, END, weight='weight')
    optimized_length = nx.shortest_path_length(weather_graph, START, END, weight='weight')

    fuel_short, co2_short, time_short = calculate_voyage_metrics(shortest_length)
    fuel_opt, co2_opt, time_opt = calculate_voyage_metrics(optimized_length)

    fuel_saving_percent = ((fuel_short - fuel_opt) / fuel_short) * 100
    co2_saving = co2_short - co2_opt

    print("\n===== VOYAGE OPTIMIZATION REPORT =====")
    print("Baseline Fuel Used:", round(fuel_short, 2), "tons")
    print("Optimized Fuel Used:", round(fuel_opt, 2), "tons")
    print("Fuel Reduction:", round(fuel_saving_percent, 2), "%")
    print("CO2 Reduction:", round(co2_saving, 2), "tons")
    print("Arrival Time Difference:", round(time_short - time_opt, 2), "hours")

    pos = dict((n, n) for n in weather_graph.nodes())
    nx.draw(weather_graph, pos, node_size=20)
    path_edges = list(zip(optimized_path, optimized_path[1:]))
    nx.draw_networkx_edges(weather_graph, pos, edgelist=path_edges, edge_color='green', width=2)
    plt.title("Optimized Route with Emission Analysis")
    plt.show()

if __name__ == "__main__":
    main()
