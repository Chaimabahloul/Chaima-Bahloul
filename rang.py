import random

# -----------------------------
# Matrice des distances
# -----------------------------
matrice_distances = [
    [0,2,2,7,15,2,5,7,6,5],
    [2,0,10,4,7,3,7,15,8,2],
    [2,10,0,1,4,3,3,4,2,3],
    [7,4,1,0,2,15,7,7,5,4],
    [15,7,4,2,0,7,3,2,2,7],
    [2,3,3,15,7,0,2,10,1,7],
    [5,7,3,7,3,2,0,2,1,3],
    [7,15,4,7,2,10,2,0,1,10],
    [6,8,2,5,2,1,1,1,0,15],
    [5,2,3,4,7,7,3,10,15,0]
]

# -----------------------------
# Paramètres GA
# -----------------------------
population_size = 20
generations = 200
mutation_rate = 0.2

# -----------------------------
# Fonctions GA
# -----------------------------
def calculer_distance_totale(solution, matrice):
    distance = 0
    for i in range(len(solution)-1):
        distance += matrice[solution[i]][solution[i+1]]
    distance += matrice[solution[-1]][solution[0]]
    return distance

def fitness(solution):
    return 1 / calculer_distance_totale(solution, matrice_distances)

# -----------------------------
# Sélection par RANG
# -----------------------------
def selection_par_rang(population):
    # On trie la population selon la fitness décroissante
    population_triée = sorted(population, key=lambda x: fitness(x), reverse=True)
    # On attribue un rang : meilleur = plus grand rang
    n = len(population_triée)
    rangs = list(range(n, 0, -1))  # meilleur = n, pire = 1
    total_rangs = sum(rangs)
    probs = [r/total_rangs for r in rangs]  # probabilité proportionnelle au rang
    # Cumul des probabilités
    cum_probs = []
    cum_sum = 0
    for p in probs:
        cum_sum += p
        cum_probs.append(cum_sum)
    # Tirage aléatoire
    r = random.random()
    for i, cp in enumerate(cum_probs):
        if r <= cp:
            return population_triée[i]
    return population_triée[-1]

# -----------------------------
# Crossovers
# -----------------------------
def crossover_uniforme(p1, p2):
    enfant = [None]*len(p1)
    for i in range(len(p1)):
        enfant[i] = p1[i] if random.random() < 0.5 else p2[i]
    missing = [v for v in p1 if v not in enfant]
    for i in range(len(enfant)):
        if enfant.count(enfant[i]) > 1:
            enfant[i] = missing.pop(0)
    return enfant

def crossover_1point(p1, p2):
    point = random.randint(1, len(p1)-1)
    enfant = p1[:point]
    for v in p2:
        if v not in enfant:
            enfant.append(v)
    return enfant

def crossover_2points(p1, p2):
    size = len(p1)
    pt1, pt2 = sorted(random.sample(range(1, size), 2))
    enfant = [None]*size
    enfant[pt1:pt2] = p1[pt1:pt2]
    pos = pt2
    for v in p2:
        if v not in enfant:
            if pos >= size:
                pos = 0
            enfant[pos] = v
            pos += 1
    return enfant

# -----------------------------
# Mutation
# -----------------------------
def mutation(solution):
    s = solution[:]
    if random.random() < mutation_rate:
        i,j = random.sample(range(len(s)),2)
        s[i], s[j] = s[j], s[i]
    return s

# -----------------------------
# Initialisation population
# -----------------------------
nombre_villes = len(matrice_distances)
population = [random.sample(range(nombre_villes), nombre_villes) for _ in range(population_size)]

# -----------------------------
# Choix utilisateur UNE SEULE FOIS
# -----------------------------
print("Choisir le type de crossover pour toute la génération :")
print("1 -> Uniforme")
print("2 -> 1-point")
print("3 -> 2-points")
choix_utilisateur = input("Votre choix (1/2/3) : ").strip()
if choix_utilisateur == '1':
    type_cross = 'uniforme'
elif choix_utilisateur == '2':
    type_cross = '1point'
elif choix_utilisateur == '3':
    type_cross = '2points'
else:
    print("Choix invalide, croisement uniforme par défaut")
    type_cross = 'uniforme'

# -----------------------------
# Boucle GA
# -----------------------------
for gen in range(generations):
    nouvelle_population = []
    while len(nouvelle_population) < population_size:
        parent1 = selection_par_rang(population)
        parent2 = selection_par_rang(population)

        # Appliquer le crossover choisi
        if type_cross=='uniforme':
            enfant = crossover_uniforme(parent1,parent2)
        elif type_cross=='1point':
            enfant = crossover_1point(parent1,parent2)
        else:
            enfant = crossover_2points(parent1,parent2)

        # Mutation
        enfant = mutation(enfant)

        nouvelle_population.append(enfant)
    
    population = nouvelle_population
1

# -----------------------------
# Meilleure solution finale
# -----------------------------
meilleure_solution = min(population, key=lambda x: calculer_distance_totale(x, matrice_distances))
meilleure_distance = calculer_distance_totale(meilleure_solution, matrice_distances)

print("\nAlgorithme Génétique (TSP) - Sélection par RANG")
print("Meilleure solution trouvée :", meilleure_solution)
print("Distance minimale :", meilleure_distance)
