import math
import random

def objective_function(solution, profit, weight, capacity):
    total_profit = sum(x * y for x, y in zip(solution, profit))
    total_weight = sum(x * y for x, y in zip(solution, weight))
    if total_weight > capacity:
        total_profit = 0
    return total_profit

def firefly_knp(profit, weight, capacity, a, b, gamma, generations, num_fireflies):
    if len(profit) != len(weight):
        return "Profit and weight vectors must have the same length."

    num_items = len(profit)
    capacities = [capacity] * num_fireflies
    best_solutions = []

    # Initialize the first generation
    solutions = [[random.randint(0, 1) for _ in range(num_items)] for _ in range(num_fireflies)]
    objective_values = [objective_function(solution, profit, weight, capacity) for solution in solutions]

    for generation in range(generations):
        for i in range(num_fireflies):
            for j in range(num_fireflies):
                if objective_values[i] < objective_values[j]:
                    distance = sum((solutions[j][k] - solutions[i][k]) ** 2 for k in range(num_items)) ** 0.5
                    attraction = b * math.exp(-gamma * distance ** 2)
                    for k in range(num_items):
                        rand = random.random()
                        new_value = round((solutions[i][k] + a * (solutions[j][k] - solutions[i][k]) + attraction * rand) % 2)
                        solutions[i][k] = new_value

        objective_values = [objective_function(solution, profit, weight, capacity) for solution in solutions]
        best_index = objective_values.index(max(objective_values))
        best_solution = (solutions[best_index], objective_values[best_index])
        best_solutions.append(best_solution)

    return best_solutions

# Example usage
profit = [4, 3, 1, 5, 7, 4]
weight = [2, 1, 1, 6, 9, 6]
capacity = 12
a = 0.9
b = 1.0
gamma = 0.2
generations = 2
num_fireflies = 6

best_solutions = firefly_knp(profit, weight, capacity, a, b, gamma, generations, num_fireflies)

print("Best Solutions:")
for iteration, solution in enumerate(best_solutions, start=1):
    solution_vector, objective_value = solution
    print(f"Iteration {iteration}:")
    print(f"Weight: {sum(x * y for x, y in zip(solution_vector, weight))}")
    print(f"Profit: {objective_value}")
    print(f"Solution: {solution_vector}")
    print()