# solution script for The Unseen Curse challenge
#!/usr/bin/env python3

from itertools import product
from tqdm import trange


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_world(self, world):
        if world not in self.adjacency_list:
            self.adjacency_list[world] = []

    def add_connection(self, world1, world2, label):
        self.add_world(world1)
        self.add_world(world2)

        if (world2, label) not in self.adjacency_list[world1]:
            self.adjacency_list[world1].append((world2, label))
        if (world1, label) not in self.adjacency_list[world2]:
            self.adjacency_list[world2].append((world1, label))

    def remove_connection(self, world1, world2):
        if world1 in self.adjacency_list:
            self.adjacency_list[world1] = [
                (w, label) for (w, label) in self.adjacency_list[world1] if w != world2
            ]
        if world2 in self.adjacency_list:
            self.adjacency_list[world2] = [
                (w, label) for (w, label) in self.adjacency_list[world2] if w != world1
            ]

    def remove_world(self, world):
        if world in self.adjacency_list:
            for neighbor, _ in self.adjacency_list[world]:
                self.adjacency_list[neighbor] = [
                    (w, label) for (w, label) in self.adjacency_list[neighbor] if w != world
                ]
            del self.adjacency_list[world]

    def get_neighbors(self, world):
        return self.adjacency_list.get(world, [])

    def print_graph(self):
        for world in self.adjacency_list:
            print(f"{world}: {self.adjacency_list[world]}")


def enumerate_possible_worlds(A, B, X, Y):
    g = Graph()

    possible_worlds = set()
    for T in [X, Y]:
        for a in range(T + 1):
            b = T - a
            if b >= 0:
                possible_worlds.add((a, b))


    for world in possible_worlds:
        g.add_world(world)

    worlds = list(possible_worlds)
    for i in range(len(worlds)):
        for j in range(i + 1, len(worlds)):
            w1, w2 = worlds[i], worlds[j]
            diff_indices = [idx for idx, (a, b) in enumerate(zip(w1, w2)) if a != b]
            if len(diff_indices) == 1:
                idx = diff_indices[0]
                label = 'B' if idx == 0 else 'A'
                g.add_connection(w1, w2, label)

    return g


c = 1
def handle_public_announcements(graph, A, B, X, Y):
    nights_needed = 1
    atleast = 0
    upto = Y
    delta = Y - X

    for _ in range(30):
        if not graph.adjacency_list:
            print(f"{c}: No worlds left, logic contradiction or puzzle solved.")
            break

        potential_worlds = []
        for world, neighbors in graph.adjacency_list.items():
            playerA_knows, playerB_knows = False, False

            # Player A tries to know B's count - A's actual state is world[0]
            status_set_A = set()
            status_set_A.add(world[1])
            for neighbor, edge_label in neighbors:
                if edge_label == 'A':
                    status_set_A.add(neighbor[1])
            if len(status_set_A) == 1:
                playerA_knows = True

            # Question to the ai: if i change the graph right here and now,
            # will i affect further calculations??
            # It seems like this is the only right option, because when the first answers/refrain from answering
            # the other immediately knows something (gets the feedback)

            # Player B tries to know A's count - B's actual state is world[1]
            status_set_B = set()
            status_set_B.add(world[0])
            for neighbor, edge_label in neighbors:
                if edge_label == 'B':
                    status_set_B.add(neighbor[0])
            if len(status_set_B) == 1:
                playerB_knows = True

            if playerA_knows or playerB_knows:
                potential_worlds.append(world)

        if (A, B) in potential_worlds:
            print(f"{c}: Declaration possible on night {nights_needed}")
            return str(nights_needed)

        for to_remove in potential_worlds:
            a, b = to_remove
            # collect all worlds where first == a or second == b
            worlds_to_remove = [w for w in graph.adjacency_list if w[0] == a or w[1] == b]
            for w in worlds_to_remove:
                graph.remove_world(w)

        nights_needed += 1

    return "-1"  # Should not happen unless contradictory input


if __name__ == "__main__":
    with open("../files/the-unseen-curse.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) % 2 == 0, "Each scenario must have two lines: (A,B) and (X,Y)."

    results = []

    for i in range(0, len(lines), 2):
        A, B = int(lines[i].split()[0]), int(lines[i].split()[1])
        X, Y = int(lines[i + 1].split()[0]), int(lines[i + 1].split()[1])

        g = enumerate_possible_worlds(A, B, X, Y)
        res = handle_public_announcements(g, A, B, X, Y)
        results.append(res)
        c += 1

    print("Flag:", f"1ng3neer2k25{{{''.join(results)}}}")

