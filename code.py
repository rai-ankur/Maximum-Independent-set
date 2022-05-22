import matplotlib.pyplot as plt
import networkx as nx

def removable(neighbor, cover):
    check = True
    for i in range(len(neighbor)):
        if cover[neighbor[i]] == 0:
            check = False
            break
    return check


def max_removable(neighbors, cover):
    r, max = -1, -1
    for i in range(len(cover)):
        if cover[i] == 1 and removable(neighbors[i], cover) == True:
            temp_cover = cover
            temp_cover[i] = 0
            sum = 0
            for j in range(len(temp_cover)):
                if temp_cover[j] == 1 and removable(neighbors[j], temp_cover) == True:
                    sum += 1
            if sum > max:
                max = sum
                r = i
    return r


def procedure_1(neighbors, cover):
    temp_cover = cover
    r = 0
    while r != -1:
        r = max_removable(neighbors, temp_cover)
        if r != -1:
            temp_cover[r] = 0
    return temp_cover


def procedure_2(neighbors, cover, k):
    count = 0
    temp_cover = cover
    for i in range(len(temp_cover)):
        if temp_cover[i] == 1:
            sum, index = 0, 0
            for j in range(len(neighbors[i])):
                if temp_cover[neighbors[i][j]] == 0:
                    index = j
                    sum += 1
            if sum == 1 and cover[neighbors[i][index]] == 0:
                temp_cover[neighbors[i][index]] = 1
                count += 1
                temp_cover[i] = 0
                temp_cover = procedure_1(neighbors, temp_cover)
            if count > k:
                break
    return temp_cover


def cover_size(cover):
    count = 0
    for i in range(len(cover)):
        if cover[i] == 1:
            count += 1
    return count


def main():
    n = int(input())

    graph = [[]] * n
    for i in range(n):
        graph[i] = list(map(int, input().split()))

    neighbors = [[]] * n

    independent_set = []

    nodes = []
    for i in range(n):
        nodes.append(i + 1)

    for i in range(n):
        temp = []
        for j in range(n):
            if graph[i][j] == 1:
                temp.append(j)
        neighbors[i] = temp


    K = int(input())
    k = n - K
    found = False
    min = n + 1
    covers = []
    counter = 0
    s = 0
    for i in range(n):
        if found:
            break
        independent_set = []
        counter += 1
        print(counter, ". ", end="")
        cover = [1] * n
        cover[i] = 0
        cover = procedure_1(neighbors, cover)
        s = cover_size(cover)
        if s < min:
            min = s
        if s <= k:
            print("Independent Set (", n-s, "): ", end="")
            for j in range(len(cover)):
                if cover[j] == 0:
                    print(j + 1, end=" ")
                    independent_set.append(j + 1)
            print()
            found = True
            print("Independent Set Size: ", n-s)
            covers.append(cover)
            break

        for j in range(n-k):
            cover = procedure_2(neighbors, cover, j)
        s = cover_size(cover)
        if s < min:
            min = s
        print("Independent Set (", n-s, "): ", end="")
        for j in range(len(cover)):
            if cover[j] == 0:
                print(j + 1, end=" ")
                independent_set.append(j + 1)
        print()
        print("Independent Set Size: ", n-s)
        covers.append(cover)
        if s <= k:
            found = True
            break

    # Pairwise intersection
    for p in range(len(covers)):
        if found:
            break
        independent_set = []
        for q in range(p+1, len(covers)):
            if found:
                break
            counter += 1
            print(counter, ". ", end="")
            cover = [1] * n
            for r in range(len(cover)):
                if covers[p][r] == 0 and covers[q][r] == 0:
                    cover[r] = 0
            cover = procedure_1(neighbors, cover)
            s = cover_size(cover)
            if s < min:
                min = s
            if s <= k:
                print("Independent Set (", n-s, "): ", end="")
                for j in range(len(cover)):
                    if cover[j] == 0:
                        print(j + 1, end=" ")
                        independent_set.append(j + 1)
                print()
                found = True
                print("Independent Set Size: ", n-s)
                break
            for j in range(k):
                cover = procedure_2(neighbors, cover, j)
            s = cover_size(cover)
            if s < min:
                min = s
            print("Independent Set (", n-s, "): ", end="")
            for j in range(len(cover)):
                if cover[j] == 0:
                    print(j + 1, end=" ")
                    independent_set.append(j + 1)
            print()
            print("Independent Set Size: ", n-s)
            if s <= k:
                found = True
                break

    if found:
        print("Found Independent Set of size at least ", K, ".")
    else:
        print("No Independent Set of size at least ", K, ".")
        print("Maximum Independent Set size found is ", n-min, ".")


    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                edges.append((i + 1, j + 1))    

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    position = nx.circular_layout(G)

    non_independent_set = []
    for i in range(n):
        if i + 1 not in independent_set:
            non_independent_set.append(i + 1)

    nx.draw_networkx_nodes(G,position, nodelist=independent_set, node_color="b")
    nx.draw_networkx_nodes(G,position, nodelist=non_independent_set, node_color="r")

    nx.draw_networkx_edges(G,position)
    nx.draw_networkx_labels(G,position)

    plt.show()

if __name__ == '__main__':
    main()