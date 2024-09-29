from random import choice, randint, choices
from timeit import default_timer as timer

import random

#generowanie instancji grafu
#n - liczba wierzchołków
def generowanie3(n, filename):
    with open(filename, 'w') as file:
        file.write(f"{n}\n")
        for i in range(1, n+1):
            for j in range(i + 1, n+1):
                if random.randint(0, 1) == 0:
                    file.write(f"{i} {j}\n")



import random

def generuj(n, nasycenie, filename):
    with open(filename, 'w') as file:
        file.write(f"{n}\n")
        max_krawedzie = nasycenie * n * (n-1) // 200  # Oblicz maksymalną liczbę krawędzi
        krawedzie = set()

        while len(krawedzie) < max_krawedzie:
            i, j = random.randint(1, n), random.randint(1, n)
            if i != j and (i, j) not in krawedzie and (j, i) not in krawedzie:
                krawedzie.add((i, j))

        for edge in krawedzie:
            file.write(f"{edge[0]} {edge[1]}\n")



def check_if_valid(graf, kolorowanie):
    for wierzcholek, sasiady in graf.items():
        kolor = kolorowanie[wierzcholek]
        for sasiad in sasiady:
            if kolorowanie[sasiad] == kolor:
                print("invalid!")
    print("valid!")
#===========================================================================

#wczytujemy plik 
def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        graph_dict = dict()
        file.readline()
        for line in file:
            row = [int(num) for num in line.strip().split()]
            sasiady = graph_dict.get(row[0], set())
            sasiady.add(row[1])
            graph_dict[row[0]] = sasiady
            sasiady = graph_dict.get(row[1], set())
            sasiady.add(row[0])
            graph_dict[row[1]] = sasiady
    return graph_dict

#algorytm zachłanny
def sekwencyjny(graph):
    colors = {}
    color_count = 0

    def is_color_available(node, color):
        for neighbor in graph[node]:
            if colors.get(neighbor) == color: return False
        return True
    for node in graph:
        for color in range(color_count):
            if is_color_available(node, color):
                colors[node] = color
                break
        else:
            colors[node] = color_count
            color_count += 1
    print(colors)
    return color_count

#================================METAHEURYSTYKA=================================

#tworzy slownik:
#   klucze: numery osobników
#   wartości: osobik jako słownik (klucz: numer wierzcholka, wartośc: kolor wierzcholka)
def create_population(num_of_vertecs, wynik_zachlannego, population_size):
    return {i: {j: randint(1, wynik_zachlannego) for j in range(1, num_of_vertecs+1)} for i in range(population_size)}


#uywamy, gdy schodzimy o jeden kolor
def change_population(population, color, graf, ):
    new_population = dict()

    for ch_num, chromosome  in population.items():
        new_population[ch_num] = dict()
        for n_num, node in chromosome['population'].items():
            if node == color:
                new_population[ch_num][n_num] = choice([i+1 for i in range(color-1)])
            else:
                new_population[ch_num][n_num] = node
    return add_fitness(graf, new_population, )

#dodaje wartosc dopasowania - ilość błędnych krawedzi
def add_fitness(graf, raw_population, ):
    return {i: {"population" : raw_population[i], "fit": check_fittness(graf, raw_population[i], )} for i in raw_population}

#funkcja sprawdza ile jest błędnych krawędzi w danym chromosomie
def check_fittness(graf, chromosome):
    wynik = 0
    for wierzcholek, sasiady in graf.items():
        kolor = chromosome[wierzcholek]
        wynik += sum(1 for i in sasiady if chromosome[i] == kolor) #sumuje liczbę sąsiadów, których kolory są takie same jak kolor danego wierzchołka - bledne krawedzie
    return wynik

#wybiera rodziców (dwa chromosomy) z posortowanej populacji:
    #jeśli dopasowanie jest mniejsze niz 50 to na rodziców wybierane są chromosomy 2-3 (dopasowanie pod względem fitness)
    #jeśli dopasowanie jest większe niz 50 to wybieramy rodzica 0-1
def parentSelection1(population):
    x = 0 if population[len(population)-1]['fit'] < 50 else 1
    return sorted(choices(population, k=4), key=lambda x: x['fit'])[1-x:3-x]

def crossover(parents):
    crosspoint = randint(0, chromosome_size-1)
    sliced_parent = { k: v for (k,v) in parents[0]['population'].items() if k > crosspoint}
    child = parents[1]['population'].copy()
    child.update(sliced_parent)
    return child


def mutation1(chromosome, all_colors, graf, verify=False):                                      #tworzy zbiór kolory zawierający kolory sąsiadów danego wierzchołka
    for wierzcholek, sasiady in graf.items():                                                   #jesli lista x nie jest pusta to oznacza istnieją kolory dostępne do wyboru
        kolory = {chromosome[sasiad] for sasiad in sasiady}                                     #losowo wybiera nowy kolor dla danego wierzchołka z kolorow dostepnych na liscie x
        if (x := [i for i in all_colors if i not in kolory]):                                       
            chromosome[wierzcholek] = choice(x)
    return chromosome


#naprawa chromosomu
def gaRun(graf, all_colors, population):
    return mutation1(crossover(parentSelection1(population)) , all_colors, graf) if population[0]['fit'] > 8 else mutation1(mutation1(crossover(parentSelection1(population)) , all_colors, graf), all_colors, graf)
        
#
def get_generation(all_colors, population):
    for j in range(30):
        child = gaRun(G, all_colors, population)
        if((x:=check_fittness(G, child, )) == 0):
            return (child, x)
        else:
            population[j+99] = {'population': child, 'fit': x}
    return 0


#============================MAIN - GŁÓWNA CZĘŚĆ PROGRAMU==============================


#generujemy instancję
generuj(250, 90, "instancja.txt")

#G = read_matrix_from_file('queen6.txt')
#G = read_matrix_from_file('miles250.txt')
#G = read_matrix_from_file('gc500.txt')
#G = read_matrix_from_file('le450_5a.txt')
#G = read_matrix_from_file('gc_1000.txt')
G = read_matrix_from_file('instancja.txt')
chromosome_size = len(G)
population_size = 100
max_liczba_kolorow = sekwencyjny(G)
print("zachlanny: ", max_liczba_kolorow)

all_colors = [i+1 for i in range(max_liczba_kolorow)]           #numeracja od 1

population = create_population(chromosome_size, max_liczba_kolorow, population_size)
population = add_fitness(G, population)
counter = 0 
while True:
    start = timer()
    for i in range(10000):
        temp_population = dict()
        if (x:=get_generation(all_colors, population)):
            counter = 0 
            all_colors.pop()
            end = timer()
            print(f"dopsaowanie dla: {max_liczba_kolorow}")
            print(end - start)
            start = timer()
            population = change_population(population, max_liczba_kolorow, G,)
            max_liczba_kolorow -= 1
            break
        else:
            if len(set([i['fit'] for i in population.values()])) == 1:
            #if len(set([i['fit'] for i in population.values()])) < 3:
                counter += 1
                if counter == 1:
                    print("poszło")
                    counter = 0
                    population = create_population(chromosome_size, max_liczba_kolorow, population_size)
                    #population = change_population(population, max_liczba_kolorow, G,)
                    population = add_fitness(G, population)
            else: 
                sorted_pop = sorted(population, key=lambda x: population[x]['fit'])
                #population = { i:population[v] for i,v in enumerate(sorted_pop[:69] + [sorted_pop[75]] +sorted_pop[95:125]) } #wywalamy ostatni //dla le450_5a
                population = { i:population[v] for i,v in enumerate(sorted_pop[:79] + [sorted_pop[85]] +sorted_pop[105:125]) } #wywalamy ostatni //znaleziono 6!
                #population = { i:population[v] for i,v in enumerate(sorted_pop[:29] + [sorted_pop[35]] +sorted_pop[59:79]) } #wywalamy ostatni
                #population = { i:population[v] for i,v in enumerate(sorted_pop[:69] + [sorted_pop[75]] +sorted_pop[79:129]) } #wywalamy ostatni //poprzednia wersja
                #population = { i:population[v] for i,v in enumerate(sorted_pop[:59] + [sorted_pop[75]] +sorted_pop[79:119]) } #wywalamy ostatni
                #print(len(population))
        
