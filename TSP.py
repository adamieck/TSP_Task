from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def read_input_file(filename):
    travel_times = {}
    city_count = 0
    cities = set()
    start_city_name = None
    with open(filename, 'r', encoding='utf-8') as file:
        city_count, start_city_name = file.readline().split()
        city_count = int(city_count)
        i = 0
        for line in file:
            line = line.split()
            city_x, city_y, time = line[0], line[1], int(line[2])
            cities.add(city_x)
            cities.add(city_y)
            if city_x not in travel_times:
                travel_times[city_x] = {}
            if city_y not in travel_times:
                travel_times[city_y] = {}
            travel_times[city_x][city_y] = time
            travel_times[city_y][city_x] = time
            travel_times[city_x][city_x] = 0
            travel_times[city_y][city_y] = 0
    cities = sorted(cities)
    start_city = cities.index(start_city_name)
    return city_count, start_city, travel_times, cities

def create_data_model(city_count, start_city, travel_times):
    data = {}
    data['distance_matrix'] = [[0] * city_count for _ in range(city_count)]
    for i, city_i in enumerate(sorted(travel_times)):
        for j, city_j in enumerate(sorted(travel_times[city_i])):
            data['distance_matrix'][i][j] = travel_times[city_i][city_j] if city_i in travel_times and city_j in travel_times[city_i] else 0
    data['num_vehicles'] = 1
    data['depot'] = start_city
    return data

def print_solution(manager, routing, solution, cities):
    print(f'Shortest route: {solution.ObjectiveValue()} min')
    index = routing.Start(0)
    plan_output = 'Route:'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' -> {}'.format(cities[manager.IndexToNode(index)])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    print(plan_output)

def main():
    filename = 'input.txt'
    
    city_count, start_city, travel_times, cities = read_input_file(filename)
    data = create_data_model(city_count, start_city, travel_times)
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(manager, routing, solution, cities)

if __name__ == '__main__':
    main()
