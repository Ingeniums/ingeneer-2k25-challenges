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

        # Avoid duplicate connections with same label
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


# Initial setup for the Muddy Children Puzzle.
def enumerate_possible_worlds(A, B, X, Y):
    g = Graph()

    # After the first announcements, all the worlds where a+b != x or y will be deleted
    # the format is A-B
    worlds = [
        (A,Y-A),
        (A,X-A),
        (Y-B,B),
        (X-B,B),
    ]
    worlds = list(set(worlds))

    # Add possible worlds to the graph
    for world in worlds:
        g.add_world(world)

    # Add connections between worlds where exactly one position differs (those are equivalent to the other party)
    for i in range(len(worlds)):
        for j in range(i + 1, len(worlds)):
            w1, w2 = worlds[i], worlds[j]

            # Check if they differ in exactly one position
            diff_indices = [idx for idx, (a, b) in enumerate(zip(w1, w2)) if a != b]
            if len(diff_indices) == 1:
                idx = diff_indices[0]
                # Label is the other person's perspective (1-based)
                label = 'B' if idx == 0 else 'A'
                g.add_connection(w1, w2, label)
    # g.print_graph()
    # exit()

    return g


def handle_public_announcements(graph):
    """
    Process public announcements that remove worlds from the graph.

    Parameters:
    - graph: Graph object representing possible worlds.
    """

    # graph.print_graph()
    # exit()
    nights_needed = 1
    for _ in range(30): # 30 here is just a placeholder because i believe we won't reach night 30
        if not graph.adjacency_list:
            print("No worlds left, logic contradiction or puzzle solved.")
            break

        # check if a player knows the what the other sees
        actual_worlds = []
        for world, neighbors in graph.adjacency_list.items():
            playerA_knows, playerB_knows = False, False

            # Player A tries to know B's count
            status_set_A = set()
            status_set_A.add(world[1])  # B's count in this world
            for neighbor, edge_label in neighbors:
                if edge_label == 'A':
                    status_set_A.add(neighbor[1])
            if len(status_set_A) == 1:
                playerA_knows = True

            # Player B tries to know A's count
            status_set_B = set()
            status_set_B.add(world[0])  # A's count in this world
            for neighbor, edge_label in neighbors:
                if edge_label == 'B':
                    status_set_B.add(neighbor[0])
            if len(status_set_B) == 1:
                playerB_knows = True

            if playerA_knows or playerB_knows:
                actual_worlds.append(world)

        if actual_worlds:
            print(f"Declaration possible on night {nights_needed}")
            break

        nights_needed += 1

def count_muddy_children(graph):
    muddy_counts = set()

    for world in graph.adjacency_list:
        muddy_count = world.count('d')
        muddy_counts.add(muddy_count)

    assert len(muddy_counts) == 1, f"Inconsistent muddy children counts across worlds: {muddy_counts}"
    return muddy_counts.pop()


if __name__ == "__main__":
    with open("../files/the-unseen-curse.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) % 2 == 0, "Each scenario must have two lines: (A,B) and (X,Y)."

    results = []

    for i in range(0, len(lines), 2):
        A, B = int(lines[i].split()[0]), int(lines[i].split()[1])
        X, Y = int(lines[i + 1].split()[0]), int(lines[i + 1].split()[1])

        enumerate_possible_worlds(A, B, X, Y)

    # Flag format
    print("Flag:", f"1ng3neer2k25{{{''.join(results)}}}")
