import random
from collections import deque

def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    # On parcourt la solution et on additionne les distances entre chaque ville consécutive
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    # On ajoute la distance pour retourner au point de départ (circuit fermé)
    # Exemple : si solution = [0, 2, 1]
    # On ajoute la distance entre 1 → 0
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisins(solution):
    # Génère toutes les solutions voisines en échangeant 2 villes dans la solution
    # Exemple : solution = [0,1,2]
    # voisins = [[1,0,2], [2,1,0], [0,2,1]]
    voisins = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]  # copie de la solution
            voisin[i], voisin[j] = voisin[j], voisin[i]  # permutation de deux villes
            voisins.append(voisin)
    return voisins

def tabu_search(matrice_distances, nombre_iterations, taille_tabu):
    nombre_villes = len(matrice_distances)
    
    # Création d'une solution initiale aléatoire
    # Exemple : [0, 1, 2, 3, ..., n] puis on mélange
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    
    # On suppose que cette solution initiale est la meilleure pour l'instant
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)
    
    # Liste Taboue : mémorise les dernières solutions visitées pour éviter de les revisiter
    # maxlen = taille maximale, elle supprime automatiquement les anciennes solutions
    tabu_list = deque(maxlen=taille_tabu)
    
    # Boucle d'optimisation
    for _ in range(nombre_iterations):
        # Générer toutes les solutions voisines
        voisins = generer_voisins(solution_actuelle)
        
        # On enlève les solutions déjà tabou
        voisins = [v for v in voisins if v not in tabu_list]
        
        # Si aucun voisin disponible (par exemple si tout est tabou), on arrête
        if not voisins:
            break
        
        # On choisit le voisin qui donne la plus petite distance totale
        # On minimise la fonction coût = calculer_distance_totale
        solution_actuelle = min(voisins, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
        
        # On ajoute cette solution à la liste taboue pour ne pas y revenir rapidement
        tabu_list.append(solution_actuelle)
        
        # Si cette solution est meilleure que la meilleure trouvée jusque-là, on la garde
        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle
    
    return meilleure_solution, meilleure_distance


# Matrice des distances entre villes (10 villes)
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

# Paramètres de recherche tabou
nombre_iterations = 1000  # nombre de recherches/générations
taille_tabu = 50  # taille de la mémoire taboue

# Exécution de la recherche
meilleure_solution, meilleure_distance = tabu_search(matrice_distances, nombre_iterations, taille_tabu)

print("Tabu Search")
print("Meilleur Solution trouvée:", meilleure_solution)
print("Distance Minimale:", meilleure_distance)
