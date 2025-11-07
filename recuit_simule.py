import random
import math

# -----------------------------------------------
# Fonction pour calculer la distance totale d'une solution (parcours)
# solution : liste d'indices de villes, ex: [0, 3, 1, 2]
# matrice_distances : matrice des distances entre les villes
# -----------------------------------------------
def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    # On parcourt toutes les villes et on additionne les distances
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    # Ajouter la distance pour revenir au départ (circuit fermé)
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

# -----------------------------------------------
# Fonction pour générer un voisin
# Principe : échanger 2 villes au hasard dans la solution
# Ex : [A, B, C, D] -> swap B et D -> [A, D, C, B]
# -----------------------------------------------
def generer_voisin(solution):
    voisin = solution[:]  # copie de la solution actuelle
    i, j = random.sample(range(len(solution)), 2)  # choisir 2 indices différents
    voisin[i], voisin[j] = voisin[j], voisin[i]    # échanger les deux villes
    return voisin

# -----------------------------------------------
# Recuit simulé pour le TSP
# matrice_distances : matrice des distances
# T0 : température initiale (ex : 100)
# Tmin : température finale (ex : 1)
# alpha : facteur de refroidissement (ex : 0.95)
# max_iterations : nombre max d'itérations
# -----------------------------------------------
def recuit_simule(matrice_distances, T0, Tmin, alpha, max_iterations):
    nombre_villes = len(matrice_distances)
    
    # --------------------------
    # 1. Solution initiale
    # On crée une solution aléatoire, ex: [0, 2, 1, 3, 4,...]
    # --------------------------
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
    
    # On initialise la meilleure solution trouvée
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle
    
    T = T0
    iteration = 0
    
    # --------------------------
    # 2. Boucle principale
    # Tant que la température > Tmin et qu'on n'a pas dépassé le max d'itérations
    # --------------------------
    while T > Tmin and iteration < max_iterations:
        # Générer un voisin aléatoire
        voisin = generer_voisin(solution_actuelle)
        distance_voisin = calculer_distance_totale(voisin, matrice_distances)
        
        # Calculer ΔE (différence de distance)
        delta_E = distance_voisin - distance_actuelle
        
        # --------------------------
        # 3. Décision d'accepter le voisin
        # --------------------------
        if delta_E < 0:   #Accepter ΔE < 0 → toujours (solution meilleure)
            # Si le voisin est meilleur (distance plus petite), on accepte toujours
            solution_actuelle = voisin
            distance_actuelle = distance_voisin
            # Exemple : distance_actuelle = 95 -> voisin = 80 -> accepte
        else:
            # Si le voisin est pire, on peut l'accepter avec probabilité P
            P = math.exp(-delta_E / T)
            # Exemple : ΔE = 5, T = 100 -> P = exp(-5/100) ≈ 0.951
            if random.random() < P:  #random.random() tire un nombre entre 0 et 1
                #Accepter ΔE > 0 → avec probabilité P qui diminue avec T
                solution_actuelle = voisin
                distance_actuelle = distance_voisin
                # Parfois, on accepte une solution pire pour sortir d'un minimum local
        
        # --------------------------
        # 4. Mise à jour de la meilleure solution
        # --------------------------
        if distance_actuelle < meilleure_distance:
            # On a trouvé une nouvelle meilleure solution
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle
            # Exemple : meilleure_distance passe de 95 -> 80
        
        # --------------------------
        # 5. Refroidissement
        # --------------------------
        T = T * alpha  # diminuer la température
        iteration += 1  # incrémenter le compteur

    return meilleure_solution, meilleure_distance

# -----------------------------------------------
# Exemple de matrice des distances entre 10 villes
# matrice_distances[i][j] = distance de la ville i à j
# -----------------------------------------------
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

# Paramètres du recuit
T0 = 100          # Température initiale
Tmin = 1          # Température finale
alpha = 0.95      # Facteur de refroidissement
max_iterations = 1000

# -----------------------------------------------
# Exécution du recuit simulé
# -----------------------------------------------
meilleure_solution, meilleure_distance = recuit_simule(
    matrice_distances, T0, Tmin, alpha, max_iterations
)

# Affichage des résultats
print("Recuit Simulé")
print("Meilleure Solution trouvée :", meilleure_solution)
print("Distance Minimale :", meilleure_distance)
