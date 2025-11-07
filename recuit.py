import random
import math

def calculer_cout_total(solution, matrice_temps):
    cout = 0
    for i in range(len(solution) - 1):
        cout += matrice_temps[solution[i]][solution[i + 1]]
    return cout

def generer_voisin(solution):
    voisin = solution[:]
    i, j = random.sample(range(len(solution)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

def recuit_simule_ordo(matrice_temps, T0, Tmin, alpha, max_iterations):
    n = len(matrice_temps)

    solution_actuelle = list(range(n))
    random.shuffle(solution_actuelle)
    cout_actuel = calculer_cout_total(solution_actuelle, matrice_temps)

    meilleure_solution = solution_actuelle[:]
    meilleur_cout = cout_actuel

    T = T0
    iteration = 0

    while T > Tmin and iteration < max_iterations:
        voisin = generer_voisin(solution_actuelle)
        cout_voisin = calculer_cout_total(voisin, matrice_temps)
        
        delta_E = cout_voisin - cout_actuel

        if delta_E < 0:
            solution_actuelle = voisin
            cout_actuel = cout_voisin
        else:
            P = math.exp(-delta_E / T)
            if random.random() < P:
                solution_actuelle = voisin
                cout_actuel = cout_voisin
        
        if cout_actuel < meilleur_cout:
            meilleure_solution = solution_actuelle[:]
            meilleur_cout = cout_actuel

        T *= alpha
        iteration += 1

    return meilleure_solution, meilleur_cout


# Exemple : matrice des temps d’enchaînement entre 6 tâches
matrice_temps = [
    [0, 3, 5, 2, 8, 6],
    [4, 0, 2, 7, 3, 4],
    [6, 2, 0, 4, 6, 5],
    [5, 4, 7, 0, 3, 9],
    [6, 6, 4, 3, 0, 2],
    [7, 5, 8, 6, 2, 0]
]

T0 = 100
Tmin = 1
alpha = 0.95
max_iterations = 1000

solution, cout = recuit_simule_ordo(matrice_temps, T0, Tmin, alpha, max_iterations)

print("Ordonnancement optimal :", solution)
print("Coût minimal :", cout)
