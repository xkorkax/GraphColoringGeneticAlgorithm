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

#algorytm zachłanny -> sekwencyjny 
def sekwencyjny2(W):
    n = len(W)
    
    DK = [-1] *n  #dostępne kolory
    KW = [-2] *n  #tablica pokolorowanych wierzchołków
    KW[0] = 1  #nadajemy wierzchołkowi 0 kolor 1

    for i in range(1, n):
        # omijamy wierzchołek 0, bo ma już początkową wartość nadaną
        # sprawdzamy po kolei sąsiadów danego wierzchołka, czy mają nadane kolory (-2 oznacza że nie ma)
        for peak in W[i]:
            if KW[peak-1] != -2:
                DK[KW[peak-1]] = 1
            else:
                DK[KW[peak-1]] = -1
        
        w = 1
        while DK[w] == 1:
            w += 1
        KW[i] = w
        
        # Resetujemy DK
        DK = [-1] * n
    
    liczba = max(KW)   #liczba wykorzystanych kolorów

    print("tablica pokolorowania:", KW)
    #print("liczba wykorzystanych kolorów:", liczba)
    return liczba

G = read_matrix_from_file('instancja.txt')
max_liczba_kolorow = sekwencyjny2(G)
print(max_liczba_kolorow)