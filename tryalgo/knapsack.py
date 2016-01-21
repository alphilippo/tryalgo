#!/usr/bin/env python3
# Knapsack
# jill-jenn vie et christoph durr - 2015


# snip{
def knapsack(p, v, cmax):
    """Knapsack

    :param p: table with size of items
    :param v: table with value of items
    :param cmax: capacity of bag
    :returns: value optimal solution, list of item indexes in solution
    :complexity: O(n * cmax), for n = number of items
    """
    n = len(p)
    Opt = [[0] * (cmax + 1) for _ in range(n + 1)]
    Sel = [[False] * (cmax + 1) for _ in range(n + 1)]
    #                               --- cas de base
    for cap in range(p[0], cmax + 1):
        Opt[0][cap] = v[0]
        Sel[0][cap] = True
    #                               --- cas d'induction
    for i in range(1, n):
        for cap in range(cmax + 1):
            if cap >= p[i] and Opt[i-1][cap - p[i]] + v[i] > Opt[i-1][cap]:
                Opt[i][cap] = Opt[i-1][cap - p[i]] + v[i]
                Sel[i][cap] = True
            else:
                Opt[i][cap] = Opt[i-1][cap]
                Sel[i][cap] = False
    #                               --- lecture solution
    cap = cmax
    sol = []
    for i in range(n-1, -1, -1):
        if Sel[i][cap]:
            sol.append(i)
            cap -= p[i]
    return (Opt[n - 1][cmax], sol)
# snip}


def knapsack2(p, v, cmax):
    n = len(p)
    # Plus grande valeur obtenable avec objets ≤ i et capacité c
    pgv = [[0] * (cmax + 1) for _ in range(n)]
    for c in range(cmax + 1):  # Initialisation
        pgv[0][c] = v[0] if c >= p[0] else 0
    pred = {}  # Prédécesseurs pour mémoriser les choix faits
    for i in range(1, n):
        for c in range(cmax + 1):
            pgv[i][c] = pgv[i - 1][c]  # Si on ne prend pas l'objet i
            pred[(i, c)] = (i - 1, c)
            # Est-ce que prendre l'objet i est préférable ?
            if c >= p[i] and pgv[i - 1][c - p[i]] + v[i] > pgv[i][c]:
                pgv[i][c] = pgv[i - 1][c - p[i]] + v[i]
                pred[(i, c)] = (i - 1, c - p[i])  # On marque le prédécesseur
    # On pourrait s'arrêter là, mais si on veut un sous-ensemble d'objets
    # optimal, il faut remonter les marquages
    cursor = (n - 1, cmax)
    chosen = []
    while cursor in pred:
        # Si la case prédécesseur a une capacité inférieure
        if pred[cursor][1] < cursor[1]:
            # C'est qu'on a ramassé l'objet sur le chemin
            chosen.append(cursor[0])
        cursor = pred[cursor]
    if cursor[1] > 0:  # A-t-on pris le premier objet ?
        # (La première ligne n'a pas de prédécesseur.)
        chosen.append(cursor[0])
    return pgv[n - 1][cmax], chosen

if __name__ == '__main__':
    # poids, valeur, capacité, optimum
    for f in [knapsack, knapsack2]:
        L = [([580, 1616, 1906, 1942, 50, 294],
              [874, 620, 345, 269, 360, 470], 2000, 1704),
             ([2, 3, 5], [6, 4, 2], 9, 10),
             ([5, 4, 3, 2, 1], [30, 19, 20, 10, 20], 10, 70),
             ([3, 3, 2, 2, 2], [40, 40, 10, 20, 30], 7, 90),
             ([2], [42], 1, 0),
             ([1], [42], 0, 0)]
        for p, v, cmax, opt in L:
            assert f(p, v, cmax)[0] == opt