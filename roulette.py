import random

# -----------------------------
# Matrice des distances
# -----------------------------
# Exemple : 10 villes, matrice[i][j] = distance entre ville i et ville j
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
population_size = 20  # nombre d'individus
generations = 200     # nombre de générations
mutation_rate = 0.2   # probabilité de mutation

# -----------------------------
# Fonctions GA
# -----------------------------
def calculer_distance_totale(solution, matrice):
    """
    Calcule la distance totale pour un circuit fermé.
    Exemple : solution=[0,2,1] -> distance = 0->2 + 2->1 + 1->0
    """
    distance = 0
    for i in range(len(solution)-1):
        distance += matrice[solution[i]][solution[i+1]]
    distance += matrice[solution[-1]][solution[0]]  # retour au point de départ
    return distance

def fitness(solution):
    """
    Fitness = 1 / distance_totale
    Plus fitness est élevée -> meilleur individu
    """
    return 1 / calculer_distance_totale(solution, matrice_distances)

# -----------------------------
# Sélection roulette
# -----------------------------
def roulette_selection(population):
    """
    Sélection par roulette :
    1. Calculer fitness de chaque individu
       Exemple : population=[A,B,C], fitness=[0.2,0.1,0.7]
    2. Probabilité de sélection proportionnelle à la fitness
       Exemple : total_fitness=1.0 -> probs=[0.2,0.1,0.7]
    3. Tirage aléatoire selon ces probabilités
    """
    f_values = [fitness(ind) for ind in population]
    total_fitness = sum(f_values)
    probs = [f/total_fitness for f in f_values]

    # Cumul des probabilités pour tirer l'individu
    cum_probs = []
    cum_sum = 0
    for p in probs:
        cum_sum += p
        cum_probs.append(cum_sum)

    r = random.random()
    for i, cp in enumerate(cum_probs):
        if r <= cp:
            return population[i]
    return population[-1]  # au cas où r > cum_probs[-1]

# -----------------------------
# Crossovers
# -----------------------------
def crossover_uniforme(p1, p2):
    """
    CrossOver uniforme :
    Chaque position prend aléatoirement le gène de p1 ou p2
    Exemple : p1=[0,1,2,3], p2=[3,2,1,0] -> enfant=[0,2,2,3] (avec correction)
    """
    enfant = [None]*len(p1)
    for i in range(len(p1)):
        enfant[i] = p1[i] if random.random() < 0.5 else p2[i]
    # Correction des doublons
    missing = [v for v in p1 if v not in enfant]
    for i in range(len(enfant)):
        if enfant.count(enfant[i]) > 1:
            enfant[i] = missing.pop(0)
    return enfant

def crossover_1point(p1, p2):
    """
    CrossOver 1 point :
    Exemple : p1=[0,1,2,3], p2=[3,2,1,0], point=2 -> enfant=[0,1,3,2]
    """
    point = random.randint(1, len(p1)-1)
    enfant = p1[:point]
    for v in p2:
        if v not in enfant:
            enfant.append(v)
    return enfant

def crossover_2points(p1, p2):
    """
    CrossOver 2 points :
    Exemple : p1=[0,1,2,3,4], p2=[4,3,2,1,0], pt1=1, pt2=3 -> enfant=[4,1,2,0,3]
    """
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
# Mutation (swap)
# -----------------------------
def mutation(solution):
    """
    Swap mutation : échange deux villes aléatoirement
    Exemple : solution=[0,1,2,3] -> mutation -> [0,2,1,3]
    """
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
# Boucle GA principale
# -----------------------------
for gen in range(generations):
    nouvelle_population = []
    while len(nouvelle_population) < population_size:
        # Sélection par roulette
        parent1 = roulette_selection(population)
        parent2 = roulette_selection(population)

        # Appliquer le crossover choisi UNE FOIS
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

# -----------------------------
# Meilleure solution finale
# -----------------------------
meilleure_solution = min(population, key=lambda x: calculer_distance_totale(x, matrice_distances))
meilleure_distance = calculer_distance_totale(meilleure_solution, matrice_distances)

print("\nAlgorithme Génétique (TSP) - Sélection Roulette")
print("Meilleure solution trouvée :", meilleure_solution)
print("Distance minimale :", meilleure_distance)
