import random

class GeneticAlgorithm:
    def __init__(self, file_path, iterations):
        self.file_path = file_path
        self.target = None
        self.batsman, self.avg_run = self.populate_batsman_and_avg_run()
        self.population = self.create_initial_population()
        self.iterations = iterations
        self.run_genetic_algorithm()

    def populate_batsman_and_avg_run(self):
        file = open(self.file_path, "r")
        first_line = file.readline().split()

        num_of_batsman, self.target = int(first_line[0]), int(first_line[1])
        self.batsman, self.avg_run = [0] * num_of_batsman, [0] * num_of_batsman

        i = 0
        for line in file:
            line_arr = line.split()
            self.batsman[i], self.avg_run[i] = line_arr[0], int(line_arr[1])
            i += 1
        
        return self.batsman, self.avg_run

    def create_initial_population(self):
        population = []

        for i in range(len(self.avg_run)):
            chromosome = []

            for j in range(len(self.avg_run)):
                select = random.randint(0, 1)
                chromosome.append(select)

            population.append(chromosome)

        return population
    
    def run_genetic_algorithm(self):
        iterations = 0
        best_chromosome = None
    
        while iterations != self.iterations:
            fitness = self.calculate_fitness()

            for i in range(len(fitness)):
                if fitness[i] == 0:
                    best_chromosome = self.population[i]

            if best_chromosome != None:
                break    

            self.discard_least_fit(fitness)
            
            random_chromosome = self.selection()
            self.crossover(random_chromosome)
            self.mutate()

            iterations += 1

        if best_chromosome != None:
            print(self.batsman)
            print(best_chromosome)
        else:
            print("-1")

    def calculate_fitness(self):
        fitness = []

        for chromosome in self.population:
            total_avg_run = 0

            for i in range(len(chromosome)):
                if chromosome[i] == 1:
                    total_avg_run += self.avg_run[i]
            
            fitness.append(self.target - total_avg_run)

        return fitness

    def discard_least_fit(self, fitness):
        max_index = 0

        for i in range(1, len(fitness)):
            if fitness[i] > fitness[max_index]:
                max_index = i

        del self.population[max_index]

    def selection(self):
        random_index = random.randint(0, len(self.population) - 1)
        return self.population.pop(random_index)

    def crossover(self, random_chromosome):
        new_population = []

        for chromosome in self.population:
            random_index = random.randint(0, len(chromosome) - 1)

            first_offspring = random_chromosome[ : random_index + 1] + chromosome[random_index + 1 : ]
            second_offspring = chromosome[ : random_index + 1] + random_chromosome[random_index + 1 : ]

            new_population.append(first_offspring)
            new_population.append(second_offspring)

        self.population = new_population

    def mutate(self):
        for chromosome in self.population:
            random_index = random.randint(0, len(chromosome) - 1)
            mutation = random.randint(0, 1)
            chromosome[random_index] = mutation

GA = GeneticAlgorithm("Lab - 2/Input3.txt", 100)