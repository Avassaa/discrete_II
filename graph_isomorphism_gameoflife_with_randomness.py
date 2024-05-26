import time
import networkx as nx
import matplotlib.pyplot as plt
import random
import string


def generate_isomorphic_graphs(num_nodes):
    G1 = nx.fast_gnp_random_graph(num_nodes, 0.45)
    ascii_identifiers = random.sample(string.ascii_letters, num_nodes)
    labels = {node: random.choice([0, 1]) for node in G1.nodes()}
    g1_mapping = {node: ascii_identifiers[i] for i, node in enumerate(G1.nodes())}
    G1 = nx.relabel_nodes(G1, g1_mapping)
    nx.set_node_attributes(G1, labels, 'label')

    shuffled_identifiers = ascii_identifiers[:]
    random.shuffle(shuffled_identifiers)
    g2_mapping = {ascii_identifiers[i]: shuffled_identifiers[i] for i in range(num_nodes)}
    G2 = nx.relabel_nodes(G1, g2_mapping)
    labels = {node: random.choice([0, 1]) for node in G1.nodes()}

    nx.set_node_attributes(G2, labels, 'label')

    pos1 = nx.spring_layout(G1)
    pos2 = nx.spring_layout(G2)

    return G1, G2, pos1, pos2


def color_node(G, key, g_color_mapping, random_modifier, disableRandomness):
    oneCount = sum(1 for neighbor in G.neighbors(key) if G.nodes[neighbor].get('label', 1) == 1)
    neighbor_redCount = sum(1 for neighbor in G.neighbors(key) if g_color_mapping[neighbor] == "red")
    neighbor_greenCount = sum(1 for neighbor in G.neighbors(key) if g_color_mapping[neighbor] == "green")
    neighbor_yellowCount = sum(1 for neighbor in G.neighbors(key) if g_color_mapping[neighbor] == "yellow")
    neighbor_blueCount = sum(1 for neighbor in G.neighbors(key) if g_color_mapping[neighbor] == "blue")

    current_color = g_color_mapping[key]
    potential_colors = ["red", "green", "blue", "yellow"]
    potential_colors.remove(current_color)

    if neighbor_redCount > 2:
        if oneCount % 2 == 0:
            g_color_mapping[key] = "red"
    if neighbor_greenCount >= 3 and neighbor_redCount < 2:
        if oneCount % 2 == 0:
            g_color_mapping[key] = "green"
    if neighbor_yellowCount >= 2 and neighbor_redCount == 0:
        if oneCount % 2 == 0:
            g_color_mapping[key] = "blue"
    if neighbor_blueCount >= 2 and neighbor_greenCount < 2 and neighbor_redCount > 0:
        if oneCount % 2 == 0:
            g_color_mapping[key] = "yellow"
    else:
        # Introduce a random color change with a small probability to avoid stagnation
        if not disableRandomness:
            if random.random() < random_modifier:
                g_color_mapping[key] = random.choice(potential_colors)


def compare_color_distributions(color_mapping1, color_mapping2):
    return (
            sum(1 for color in color_mapping1.values() if color == 'red') == sum(
        1 for color in color_mapping2.values() if color == 'red') and
            sum(1 for color in color_mapping1.values() if color == 'green') == sum(
        1 for color in color_mapping2.values() if color == 'green') and
            sum(1 for color in color_mapping1.values() if color == 'blue') == sum(
        1 for color in color_mapping2.values() if color == 'blue') and
            sum(1 for color in color_mapping1.values() if color == 'yellow') == sum(
        1 for color in color_mapping2.values() if color == 'yellow')
    )


def get_images(iter_number, stability_threshold=1000, color_change_threshold=5000,
               random_modifier=0.001, node_size=15, disableRandomness=False, isTestInstance=False):
    try:
        if disableRandomness:
            f = open(f"{node_size}_nodeSize_{random_modifier}_randomRate.txt", "a")  #For logging
        else:
            f = open(f"{node_size}_nodeSize_{random_modifier}_randomRate.txt", "a")  #For logging

    except IOError:
        print("I/O error({0}): {1}")
        return

    G1, G2, pos1, pos2 = generate_isomorphic_graphs(node_size)
    colors = ["red", "green", "blue", "yellow"]

    # Initial random coloring
    g1_color_mapping = {i: random.choice(colors) for i in G1.nodes()}
    g2_color_mapping = {i: random.choice(colors) for i in G2.nodes()}

    G1_labels = {node: data.get('label', f'{random.choice([0, 1])}') for node, data in G1.nodes(data=True)}
    G2_labels = {node: data.get('label', f'{random.choice([0, 1])}') for node, data in G2.nodes(data=True)}

    print("Initial Labels for Graph G1:")
    for key, value in G1_labels.items():
        print(f"{key}: {value}")

    print("\nInitial Labels for Graph G2:")
    for key, value in G2_labels.items():
        print(f"{key}: {value}")

    mixed_g1_nodes = list(G1.nodes())
    random.shuffle(mixed_g1_nodes)
    mixed_g2_nodes = list(G2.nodes())
    random.shuffle(mixed_g2_nodes)

    iteration = 0
    g1_prev_colors = {i: None for i in G1.nodes()}
    g2_prev_colors = {i: None for i in G2.nodes()}
    g1_color_change_counts = {i: 0 for i in G1.nodes()}
    g2_color_change_counts = {i: 0 for i in G2.nodes()}
    uncolorable_nodes_G1 = set()
    uncolorable_nodes_G2 = set()

    current_frozen_graph = random.choice(['G1', 'G2'])
    print(f"Graph {current_frozen_graph} is initially frozen.")

    g1_prev_color_distribution = None
    g2_prev_color_distribution = None
    stability_count = 0
    isMatched = False

    while iteration < iter_number:
        print(f"Iteration: {iteration} for {random_modifier} random modifier, {node_size} node size.")

        if current_frozen_graph == 'G1':
            if mixed_g2_nodes:
                random_node2 = random.choice(mixed_g2_nodes)
                mixed_g2_nodes.remove(random_node2)
            else:
                random_node2 = random.choice(list(G2.nodes()))
            color_node(G2, random_node2, g2_color_mapping, random_modifier, disableRandomness)
            prev_color = g2_prev_colors[random_node2]
            new_color = g2_color_mapping[random_node2]
            if new_color != prev_color:
                g2_color_change_counts[random_node2] = 0
            else:
                g2_color_change_counts[random_node2] += 1
                if g2_color_change_counts[random_node2] >= color_change_threshold:
                    uncolorable_nodes_G2.add(random_node2)
            g2_prev_colors[random_node2] = new_color
        else:
            if mixed_g1_nodes:
                random_node1 = random.choice(mixed_g1_nodes)
                mixed_g1_nodes.remove(random_node1)
            else:
                random_node1 = random.choice(list(G1.nodes()))
            color_node(G1, random_node1, g1_color_mapping, random_modifier, disableRandomness)
            prev_color = g1_prev_colors[random_node1]
            new_color = g1_color_mapping[random_node1]
            if new_color != prev_color:
                g1_color_change_counts[random_node1] = 0
            else:
                g1_color_change_counts[random_node1] += 1
                if g1_color_change_counts[random_node1] >= color_change_threshold:
                    uncolorable_nodes_G1.add(random_node1)
            g1_prev_colors[random_node1] = new_color

        if compare_color_distributions(g1_color_mapping, g2_color_mapping):
            isMatched = True
            if isMatched:
                try:
                    f.write(f"Pattern matched after {iteration} iterations ---- SUCCESSFUL\n")
                    f.flush()
                    f.close()
                except IOError as e:
                    print("IO ERROR!")
            if not isTestInstance:
                plt.figure(figsize=(12, 6))
                plt.subplot(121)
                nx.draw(G1, pos1, with_labels=True, labels=G1_labels, node_color=list(g1_color_mapping.values()),
                        node_size=500)
                plt.title(f"Iteration {iteration + 1}: Graph G1,Frozen graph:{current_frozen_graph}")

                plt.subplot(122)
                nx.draw(G2, pos2, with_labels=True, labels=G2_labels, node_color=list(g2_color_mapping.values()),
                        node_size=500)
                plt.title(f"Iteration {iteration + 1}: Graph G2, Frozen graph:{current_frozen_graph}")
                plt.show()
            print(f"Graphs matched color distribution after {iteration + 1} iterations.")
            print("Graph G1:")
            print(nx.get_node_attributes(G1, 'label'))
            print({color: list(g1_color_mapping.values()).count(color) for color in colors})
            print("\nGraph G2:")
            print(nx.get_node_attributes(G2, 'label'))
            print({color: list(g2_color_mapping.values()).count(color) for color in colors})
            return

        colored_nodes_g1 = {color: [] for color in set(g1_color_mapping.values())}
        colored_nodes_g2 = {color: [] for color in set(g2_color_mapping.values())}

        for node, color in g1_color_mapping.items():
            if color:
                colored_nodes_g1[color].append(node)
        for node, color in g2_color_mapping.items():
            if color:
                colored_nodes_g2[color].append(node)

        if g1_prev_color_distribution == colored_nodes_g1 and g2_prev_color_distribution == colored_nodes_g2:
            stability_count += 1
        else:
            stability_count = 0

        g1_prev_color_distribution = colored_nodes_g1
        g2_prev_color_distribution = colored_nodes_g2

        if stability_count >= stability_threshold:
            current_frozen_graph = 'G2' if current_frozen_graph == 'G1' else 'G1'
            print(f"Stability threshold reached, switching to {current_frozen_graph}.")
            uncolorable_nodes_G1.clear()
            uncolorable_nodes_G2.clear()
            stability_count = 0

        if len(uncolorable_nodes_G1) == len(G1.nodes()) or len(uncolorable_nodes_G2) == len(G2.nodes()):
            current_frozen_graph = 'G2' if current_frozen_graph == 'G1' else 'G1'
            print(f"All nodes became uncolorable, switching to {current_frozen_graph}.")
            uncolorable_nodes_G1.clear()
            uncolorable_nodes_G2.clear()

        iteration += 1

        if iteration % 10000 == 0 or isMatched:

            if not isTestInstance:
                time.sleep(1)
                plt.figure(figsize=(12, 6))
                plt.subplot(121)
                nx.draw(G1, pos1, with_labels=True, labels=G1_labels, node_color=list(g1_color_mapping.values()),
                        node_size=500)
                if current_frozen_graph == "G1":
                    plt.title(f"Iteration {iteration + 1}: Graph G1 (frozen)")
                else:
                    plt.title(f"Iteration {iteration + 1}: Graph G1")
                plt.subplot(122)
                nx.draw(G2, pos2, with_labels=True, labels=G2_labels, node_color=list(g2_color_mapping.values()),
                        node_size=500)
                if current_frozen_graph == "G2":
                    plt.title(f"Iteration {iteration + 1}: Graph G2(frozen)")
                else:
                    plt.title(f"Iteration {iteration + 1}: Graph G2")

                plt.show()

    if not isMatched:
        print("Reached the maximum number of iterations without matching color distributions.")
        try:
            f.write(f"Pattern could not match after {iteration} iterations ---- UNSUCCESSFUL\n")
            f.flush()
            f.close()
        except IOError:
            print("IO error occured")
            return

    print("Final Color Counts:")
    print("Graph G1:")
    print(nx.get_node_attributes(G1, 'label'))
    print({color: list(g1_color_mapping.values()).count(color) for color in colors})
    print("Uncolorable Nodes in Graph G1:")
    print(uncolorable_nodes_G1)

    print("\nGraph G2:")
    print(nx.get_node_attributes(G2, 'label'))
    print({color: list(g2_color_mapping.values()).count(color) for color in colors})
    print("Uncolorable Nodes in Graph G2:")
    print(uncolorable_nodes_G2)


def main():
    while True:
        random_modifier = 0.1
        while random_modifier >= 0.0001:
            node_size = 20
            while node_size >= 5:
                print("--------------------------------------------------------------------")
                print(f"Testing for ---- {random_modifier} random modifier, {node_size} node size with 10000000 iterations")
                time.sleep(0.5)
                get_images(10_000_000, random_modifier=random_modifier, node_size=node_size,disableRandomness=False,isTestInstance=True)
                #get_images(10_000_000, random_modifier=random_modifier, node_size=node_size,disableRandomness=True,isTestInstance=True)
                node_size-= 5
            random_modifier*= 0.1



if __name__ == "__main__":
    main()
