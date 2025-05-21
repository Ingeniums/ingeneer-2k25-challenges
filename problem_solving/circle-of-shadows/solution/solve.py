# solve script for harry potter themed muddy children puzzle
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


N = 3
K = 0
#               # at least one know     + no one knows      + no one knows  + those who know step out
ANNOUNCEMENTS = 1                       + 1 + 1                + K             + 1


# Initial setup for the Muddy Children Puzzle.
def enumerate_possible_worlds(N):
    g = Graph()

    # Generate all possible N-bit combinations of 'c' and 'd'
    worlds = [''.join(bits) for bits in product('cd', repeat=N)]

    # Add possible worlds to the graph
    for world in worlds:
        g.add_world(world)
    # g.print_graph()
    # exit()

    # Add connections between worlds where <label> perspective is equivalent in both
    for i in range(len(worlds)):
        for j in range(i + 1, len(worlds)):
            w1, w2 = worlds[i], worlds[j]
            diff_positions = [idx + 1 for idx, (a, b) in enumerate(zip(w1, w2)) if a != b]

            if len(diff_positions) == 1:
                label = diff_positions[0]  # position (1-based)
                g.add_connection(w1, w2, label)

    return g


def handle_public_announcements(graph, announcements, N, K):
    """
    Process public announcements that remove worlds from the graph.

    Parameters:
    - graph: Graph object representing possible worlds.
    - announcements: list of integers [0,1,2,...] representing announcement indices.
    """

    # graph.print_graph()
    # exit()
    for ann in announcements:
        if ann == 0:
            # Remove world where all are clean (e.g., "ccc")
            all_clean = 'c' * N
            if all_clean in graph.adjacency_list:
                graph.remove_world(all_clean)

        elif ann < 2 + K:
            # Remove worlds where the number of muddy children == current round
            to_remove = []
            for world in graph.adjacency_list:
                muddy_count = world.count('d')
                if muddy_count == ann:
                    to_remove.append(world)
            for world in to_remove:
                graph.remove_world(world)

        elif ann == 2 + K:
            # Remove worlds where NO child knows their status — i.e., ¬N is FALSE.
            to_remove = []
            for world, neighbors in graph.adjacency_list.items():
                child_knows = False
                for i in range(N):
                    label = i + 1
                    status_set = set()

                    # Add the child's status in this world (reflexivity)
                    status_set.add(world[i])

                    # Look at all indistinguishable worlds for this child
                    for neighbor, edge_label in neighbors:
                        if edge_label == label:
                            status_set.add(neighbor[i])

                    # If all statuses are the same, the child knows their own status
                    if len(status_set) == 1:
                        child_knows = True
                        break

                # If no child knows, remove this world
                if not child_knows:
                    to_remove.append(world)

            for world in to_remove:
                graph.remove_world(world)


def count_muddy_children(graph):
    muddy_counts = set()

    for world in graph.adjacency_list:
        muddy_count = world.count('d')
        muddy_counts.add(muddy_count)

    assert len(muddy_counts) == 1, f"Inconsistent muddy children counts across worlds: {muddy_counts}"
    return muddy_counts.pop()


if __name__ == "__main__":
    with open("../files/circle-of-shadows.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) % 2 == 0, "Each scenario must have two lines: N and K."

    results = []

    for i in trange(0, len(lines), 2):
        N = int(lines[i])
        K = int(lines[i + 1])
        ANNOUNCEMENTS = 1 + 1 + K + 1  # at least one + no one knows + K + final
        announcements = list(range(ANNOUNCEMENTS))

        graph = enumerate_possible_worlds(N)
        handle_public_announcements(graph, announcements, N, K)
        muddy_count = count_muddy_children(graph)
        results.append(str(muddy_count))

    # Flag format
    print("Flag:", f"1ng3neer2k25{{{''.join(results)}}}")

