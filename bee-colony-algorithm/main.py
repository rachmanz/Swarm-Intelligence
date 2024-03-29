#---
# Date : 06 March 2024 
# Author : Abdurrahman Al-atsary 
# Place : Institut Teknologi Sumatera
#---


# Library yang digunakan
import random # Generate Random Number 
import numpy as np # Proses Matematika dan rumus matematis 


# Hasil random ditetapkan menjadi tetap
random.seed(121450128) # Btw ini NIM saya :)

# Fungsi objektif target yang harus dioptimalisasi
def obj(x, y):
    return 19 + x * np.sin(x * np.pi) + (10 - y) * np.sin(y * np.pi)

# Parameter yang digunakan selama jalannya program (Dapat diubah)
dim = 2
num_scouts = 7
max_iterations = 3
num_onlookers = 7
limit = 1

# Insialisasi Populasi Awal dengan Constrain yang ada
population = np.zeros((num_scouts, dim))
population[:, 0] = np.random.uniform(-5, 9.8, num_scouts)
population[:, 1] = np.random.uniform(0, 7.3, num_scouts)

# Fungsi Fitness 
def fitness(value):
    if value >= 0:
        return 1 / (1 + value)
    else:
        return 1 + abs(value)

# Fungsi lebah pengintai
def scout_bee(population, fitness_values, trials):
    for j in range(num_scouts):
        random_dim = random.sample([0, 1], 1)[0]
        if random_dim == 1:
            random_scout = random.sample(list(set(range(num_scouts)) - {j}), 1)[0]
            x_neighbor = population[random_scout, 0]
            y_old = population[j, 1]
            y_new = y_old + random.uniform(-1, 1) * (y_old - x_neighbor)
            obj_new = obj(population[j, 0], y_new)
            if 0 <= y_new <= 7.3 and fitness(obj_new) > fitness_values[j]:
                population[j, 1] = y_new
                fitness_values[j] = fitness(obj_new)
                trials[j] = 0
            else:
                trials[j] += 1
        else:
            random_scout = random.sample(list(set(range(num_scouts)) - {j}), 1)[0]
            x_old = population[j, 0]
            x_neighbor = population[random_scout, 0]
            x_new = x_old + random.uniform(-1, 1) * (x_old - x_neighbor)
            obj_new = obj(x_new, population[j, 1])
            if -5 <= x_new <= 9.8 and fitness(obj_new) > fitness_values[j]:
                population[j, 0] = x_new
                fitness_values[j] = fitness(obj_new)
                trials[j] = 0
            else:
                trials[j] += 1

# Fungsi Lebah Pengangguran 
def onlooker_bee(population, fitness_values, trials):
    prob_fit = fitness_values / np.sum(fitness_values)
    num_recruited = 0
    while num_recruited < num_onlookers:
        r = np.zeros(num_onlookers)
        for j in range(num_onlookers):
            r[j] = random.uniform(0, 1)
        for j in range(num_onlookers):
            if r[j] < prob_fit[j]:
                num_recruited += 1
                random_dim = random.sample([0, 1], 1)[0]
                if random_dim == 1:
                    random_scout = random.sample(list(set(range(num_scouts)) - {j}), 1)[0]
                    x_neighbor = population[random_scout, 0]
                    y_old = population[j, 1]
                    y_new = y_old + random.uniform(-1, 1) * (y_old - x_neighbor)
                    obj_new = obj(population[j, 0], y_new)
                    if 0 <= y_new <= 7.3 and fitness(obj_new) > fitness_values[j]:
                        population[j, 1] = y_new
                        fitness_values[j] = fitness(obj_new)
                        trials[j] = 0
                    else:
                        trials[j] += 1
                else:
                    random_scout = random.sample(list(set(range(num_scouts)) - {j}), 1)[0]
                    x_old = population[j, 0]
                    x_neighbor = population[random_scout, 0]
                    x_new = x_old + random.uniform(-1, 1) * (x_old - x_neighbor)
                    obj_new = obj(x_new, population[j, 1])
                    if -5 <= x_new <= 9.8 and fitness(obj_new) > fitness_values[j]:
                        population[j, 0] = x_new
                        fitness_values[j] = fitness(obj_new)
                        trials[j] = 0
                    else:
                        trials[j] += 1

# Funsgi lebah operator pengintai
def scout_bee_operator(population, fitness_values, trials):
    scouting = trials > limit
    for scout in range(len(scouting)):
        if scouting[scout]:
            population[scout, 0] = np.random.uniform(-5, 9.8)
            population[scout, 1] = np.random.uniform(0, 7.3)
            trials[scout] = 0
            fitness_values[scout] = fitness(obj(population[scout, 0], population[scout, 1]))

# Fungsi mencetah hasil rapih
def print_results(population, fitness_values, trials, iteration):
    print(f"\nIteration {iteration+1}")
    print("Food Source")
    print(np.round(population, 3))
    print("Fitness")
    print(np.round(fitness_values, 5))
    print("Trial")
    print(np.round(trials))

    best_index = np.argmax(fitness_values)
    print(f"Koordinat X Terbaik: {round(population[best_index, 0], 3)}")
    print(f"Koordinat Y Terbaik: {round(population[best_index, 1], 3)}")
    print(f"Fitnessnya: {round(fitness_values[best_index], 3)}")
    print(f"Nilai Objektif Paling Berkualitas: {obj(population[best_index, 0], population[best_index, 1])}")
    print(f"Trialnya: {trials}")
    print(f"Sumber Makanan Terbaik Ada di: {best_index}")


# Penerapan fungsi optimum Bee Colony (ABC)
fitness_values = np.array([fitness(obj(x, y)) for x, y in population])
trials = np.zeros(num_scouts)

for iteration in range(max_iterations):
    print_results(population, fitness_values, trials, iteration)

    scout_bee(population, fitness_values, trials)
    onlooker_bee(population, fitness_values, trials)
    scout_bee_operator(population, fitness_values, trials)

# Mencetak hasil
print_results(population, fitness_values, trials, max_iterations)