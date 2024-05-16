class GraphAndHeuristicBuilder:
    def __init__(self, file_path):
        self.graph = {}
        self.heuristic = {}
        self.file_path = file_path

    def create_graph_and_heuristic(self):
        file = open(self.file_path, "r")
        
        for line in file:
            line_arr = line.split()
            self.populate_graph_and_heuristic(line_arr)

    def populate_graph_and_heuristic(self, line_arr):
        for i in range(len(line_arr)):
            if i == 0:
                self.graph[line_arr[i]] = []
            elif i == 1:
                self.heuristic[line_arr[0]] = int(line_arr[i])
            else:
                if i % 2 == 0:
                    self.graph[line_arr[0]].append((line_arr[i], int(line_arr[i + 1])))

    def print(self):
        print("Graph:")
        for key, value in self.graph.items():
            print(f'{key}: {value}')
        print("--------------------------------")

        print("Heuristic Table:")
        for key, value in self.heuristic.items():
            print(f'{key}: {value}')
        print("---------------------------------")

    def get_graph_heuristic(self):
        return self.graph, self.heuristic

class A_star:
    def __init__(self, graph, heuristic, start=None, goal=None):
        self.graph = graph
        self.heuristic = heuristic
        self.start = start
        self.goal = goal
    
    def set_start_and_goal(self):
        start = input("Start: ")
        goal = input("Destination: ")
        self.start = start
        self.goal = goal

    def check_variables(self):
        if self.graph == None or self.heuristic == None:
            print("Please create graph and heuristic using the GraphAndHeuristicBuilder class")
            return False
        elif self.start == None or self.goal == None:
            print("Please set start and goal using parameters or set_start_and_goal method")
            return False
        else:
            return True

    def run_a_star(self):
        run = self.check_variables()
        if run == False:
            return
        
        priority_queue = []
        priority_queue.append((self.start, 0))
        came_from = []
        goal_cost = 99999
        goal_counter = 0
        
        while True:
            node = priority_queue.pop(0)[0]
            goal = False

            if node == self.goal:
                break

            for adj_node, cost in self.graph[node]:
                total_cost = 0
                node_cost = 0
                
                if adj_node in came_from:
                    continue
                else:
                    temp_node = node
                    for i in range(len(came_from) - 1, -1, -1):
                        for tupl in self.graph[temp_node]:
                            if tupl[0] == came_from[i]:
                                node_cost += tupl[1]
                                temp_node = tupl[0]
                                break

                    total_cost = cost + node_cost + self.heuristic[adj_node]
                    if adj_node == self.goal and total_cost < goal_cost:
                        goal_cost = goal_cost
                        goal = True
                        if goal_counter == 0:
                            came_from.append(node)
                            goal_counter += 1
                        else:
                            came_from[-1] = node

                    priority_queue.append((adj_node, total_cost))
            
            if goal == False:
                came_from.append(node)
            priority_queue.sort(key=lambda x: x[1])

        self.print_path_distance(came_from)
        
    def print_path_distance(self, came_from):
        distance = 0
        temp_node = self.goal
        path = "Bucharest"
        for i in range(len(came_from) - 1, -1, -1):
            for tupl in self.graph[temp_node]:
                if tupl[0] == came_from[i]:
                    distance += tupl[1]
                    temp_node = tupl[0]
                    break
            
            path = temp_node + " -> " + path
        
        print("Path:", path)
        print("Distance:", distance)


graph_heuristic = GraphAndHeuristicBuilder("Lab - 1/Input file.txt")
graph_heuristic.create_graph_and_heuristic()
graph_heuristic.print()
graph, heuristic = graph_heuristic.get_graph_heuristic()

a_star = A_star(graph, heuristic)
a_star.set_start_and_goal()
a_star.run_a_star()