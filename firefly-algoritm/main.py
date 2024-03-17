import math
import random

# Fungsi Objektif (Ubah fungsi sesuai dengan soal Anda)
def f(x):
    return math.sqrt(x) + 12 + x**2 * math.sin(x) + 200*x

# Firefly Algorithm
def firefly_algorithm(n, alpha, beta, gamma, max_iter, lb, ub):
    # Inisalisasi yang digunakan
    fireflies = [random.uniform(lb, ub) for _ in range (n)]
    intensities = [f(x) for x in fireflies]
    best_idx = intensities.index(min(intensities))
    best_sol = fireflies[best_idx]
    
    for i in range(max_iter):
        # Pindahkan kunang-kunang yang lebih terang
        for j in range(n):
            for k in range(n):
                if intensities[k] < intensities[j]:
                    r = math.sqrt((fireflies[j] - fireflies[k])**2)
                    beta_r = beta * math.exp(-gamma * r**2)
                    fireflies[j] = (1 - beta_r) * fireflies[j] + beta_r * fireflies[k] + alpha * (random.random() - 0.5)
                    
            # Evaluasi solusi baru
            fireflies[j] = max(lb, min(ub, fireflies[j]))
            intensities[j] = f(fireflies[j])
            
            # Update solusi terbaik
            if intensities[j] < intensities[best_idx]:
                best_idx = j
                best_sol = fireflies[j]
                
        # Memunculkan proses iterasi dan hasil pada output
        print(f"Iteration {i+1}: Best solution = {best_sol}, f({best_sol}) = {intensities[best_idx]}")
        
    return best_sol

# Parameter yang digunakan untuk solusi dari fungsi diatas (Dapat diubah disini)
n = 6
alpha = 0.5
beta = 1
gamma = 0.6
max_iter = 2
lb = 40
ub = 220

# Jalankan algoritma firefly
best_solution = firefly_algorithm(n, alpha, beta, gamma, max_iter, lb, ub)
print(f"\nBest solution found: x = {best_solution}, f(x) = {f(best_solution)}")