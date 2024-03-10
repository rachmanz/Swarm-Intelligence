import random
import numpy as np 
import math

# Fungsi untuk menghitung nilai objektif
def objective_function(x):
    # Contoh fungsi objektif (Sphere Function)
    return sum(map(lambda xi: pow(xi, 2), x))

# Fungsi Levy Flight
def levy_flight(lamb, alpha=1.5):
    sigma_u = math.gamma(1 + alpha) * math.sin(math.pi * alpha / 2) / (math.gamma((1 + alpha) / 2) * alpha * (2 ** ((alpha - 1) / 2)))
    sigma_v = 1

    u = np.random.randn() * sigma_u 
    v = np.random.randn()

    step = u / (abs(v) ** (1 / alpha))

    return lamb * step

# Implementasi Algoritma Cuckoo
def cuckoo_search(objective_func, n_nests, max_iter, lb, ub, alpha=1.5, pa=0.25):
    dim = len(lb)  # Dimensi ruang pencarian
    nests = [[lb[i] + random.random() * (ub[i] - lb[i]) for i in range(dim)] for j in range(n_nests)]
    fitness = [objective_func(nest) for nest in nests]
    best_nest = nests[fitness.index(min(fitness))]
    best_fitness = min(fitness)

    for it in range(max_iter):
        # Perkembangbiakan cuckoo dengan menghasilkan solusi baru
        new_nests = []
        for nest in nests:
            new_nest = nest.copy()
            k = random.randint(0, dim - 1)
            new_nest[k] += levy_flight(alpha) * (lb[k] - ub[k])

            # Evaluasi kesesuaian sarang baru
            new_fitness = objective_func(new_nest)
            new_nests.append(new_nest)

            # Pembaruan sarang terbaik
            if new_fitness < best_fitness:
                best_fitness = new_fitness
                best_nest = new_nest

        # Pembuangan solusi buruk dan pembangunan sarang baru
        fitness = [objective_func(nest) for nest in new_nests]
        nests = sorted(new_nests, key=lambda x: fitness[new_nests.index(x)])[:n_nests]

        # Pembangunan sarang baru dengan probabilitas pa
        for j in range(n_nests):
            if random.random() < pa:
                nests[j] = [lb[i] + random.random() * (ub[i] - lb[i]) for i in range(dim)]

    return best_nest, best_fitness

# Contoh penggunaan
n_nests = 50  # Jumlah sarang
max_iter = 1000  # Jumlah iterasi maksimum
lb = [-5] * 2  # Batas bawah ruang pencarian
ub = [5] * 2  # Batas atas ruang pencarian

best_solution, best_fitness = cuckoo_search(objective_function, n_nests, max_iter, lb, ub)
print("Solusi terbaik:", best_solution)
print("Nilai objektif terbaik:", best_fitness)