import networkx as nx
import matplotlib.pyplot as plt
import random
import string
from networkx import Graph
import time

#RULE:Check the number of 1's if

def generate_isomorphic_graphs(num_nodes):
    # Generate a random graph G1
    G1 = nx.fast_gnp_random_graph(num_nodes, 0.45) # p for possibility for edge creation

    ascii_identifiers = random.sample(string.ascii_letters, num_nodes)  # I used random ascii letters as identifiers
    labels = {node: random.choice([0, 1]) for node in G1.nodes()}

    g1_mapping = {node: ascii_identifiers[i] for i, node in enumerate(G1.nodes())}

    G1 = nx.relabel_nodes(G1, g1_mapping)

    nx.set_node_attributes(G1, labels, 'label')

    shuffled_identifiers = ascii_identifiers[:]
    random.shuffle(shuffled_identifiers)
    g2_mapping = {ascii_identifiers[i]: shuffled_identifiers[i] for i in range(num_nodes)}

    G2 = nx.relabel_nodes(G1, g2_mapping)

    nx.set_node_attributes(G2, labels, 'label')

    nx.random_layout(G1)
    nx.random_layout(G2)
    return G1, G2

def print_nodes(graph1:Graph,graph2:Graph):
    g1_set=set()
    g2_set=set()
    print("-------------- GRAPH 1 -----------")
    for node in graph1.nodes():
        g1_set.add(node)
        print(node,end=",")
    print()

    print("-------------- GRAPH 2 -----------")

    for node in graph2.nodes():
        g2_set.add(node)
        print(node,end=",")
    print()
    print(f"Are the nodes equal :{g1_set==g2_set}")








def color_node(G:Graph, key:str, g_color_mapping:dict,isGraphFullyColoured:bool)->None:
    #To implement if neighbor contains odd number of 1's
    oneCount=0
    neighbor_oneCount=0
    neighbor_redCount=0
    neighbor_greenCount=0
    neighbor_yellowCount=0
    neighbor_blueCount=0
    neighbor_blackCount=0
    for neighbor in G.neighbors(key):
        if G.nodes[neighbor].get('label', 1) == 1:
            oneCount+=1

    for neighbor in G.neighbors(key):
        for neighbor_of_neighbor in G.neighbors(neighbor):
            if G.nodes[neighbor_of_neighbor].get('label', 1) == 1:
                neighbor_oneCount+=1

    if isGraphFullyColoured:
        for neighbor in G.neighbors(key):
            if g_color_mapping[neighbor]=="red":
                neighbor_oneCount-=1 #Red neighbor also has an effect on neighborOne count for randomness
                neighbor_redCount+=1
            elif g_color_mapping[neighbor]=="green":
                neighbor_greenCount+=1
            elif g_color_mapping[neighbor]=="blue":
                neighbor_blueCount+=1
            elif g_color_mapping[neighbor]=="yellowCount":
                neighbor_yellowCount+=1
            else:
                neighbor_blackCount+=1

    #If graph is not fully coloured color it according to this:
    if not isGraphFullyColoured:
        if oneCount%2==0:
            if neighbor_oneCount%2==0:
                g_color_mapping[key]="red"
            else:
                g_color_mapping[key]="green"
        else:
            if neighbor_oneCount%2==0:
                g_color_mapping[key]="blue"
            else:
                g_color_mapping[key]="yellow"
    else:
        #When it is fully coloured, apply the rules below
        if neighbor_redCount >2:
            if oneCount%2==0:
                g_color_mapping[key]="red" #If more than 2 dying neighbors this node will also die
        if neighbor_greenCount >=3 and neighbor_redCount<2:
            if oneCount%2==0:
                g_color_mapping[key]="green" # if more than 3 healthy healthy as well and less than 2 dying
        if neighbor_yellowCount >=2 and neighbor_redCount<2:
            if oneCount%2==0:
                g_color_mapping[key]="yellow"
        if neighbor_blueCount>=2 and neighbor_redCount!=0 and neighbor_greenCount<2:
            if oneCount%2==0:
                g_color_mapping[key]="blue"
                #Red--> Dying
                #Blue --> Sick
                #Green --> Healthy
                #Yellow --> healing










def get_images(is_endless:bool,iter_number:int):
    G1, G2 = generate_isomorphic_graphs(20)

    g1_color_mapping = {}
    for i in G1.nodes():
        g1_color_mapping[i]="lightblue"

    g2_color_mapping = {}
    #Prepare labels
    G1_labels = {node: data.get('label', f'{random.choice([0,1])}') for node, data in G1.nodes(data=True)}
    G2_labels = {node: data.get('label', f'{random.choice([0,1])}') for node, data in G2.nodes(data=True)}

    pos1 = nx.spring_layout(G2)  # pos fix
    pos2 = nx.spring_layout(G2)  # pos fix


    #Mix G2.nodes() and G1.nodes()
    mixed_g1_nodes=list(G1.nodes())
    random.shuffle(mixed_g1_nodes)

    mixed_g2_nodes=list(G2.nodes())
    random.shuffle(mixed_g2_nodes)


    for i in G2.nodes():
        g2_color_mapping[i]="lightblue"


    mixed_g1_nodes_copy=[i for i in mixed_g1_nodes]
    mixed_g2_nodes_copy=[i for i in mixed_g2_nodes]


    iteration=0
    while True:
                iteration+=1
                print("Iteration =",iteration)
                if len(mixed_g1_nodes_copy)!=0:
                    random_node1=random.choice(mixed_g1_nodes_copy)
                else:
                    random_node1=random.choice(mixed_g1_nodes)
                if random_node1 in mixed_g1_nodes_copy:
                    mixed_g1_nodes_copy.remove(random_node1)

                if len(mixed_g2_nodes_copy)!=0:
                    random_node2=random.choice(mixed_g2_nodes_copy)
                else:
                    random_node2=random.choice(mixed_g2_nodes)
                if random_node2 in mixed_g2_nodes_copy:
                    mixed_g2_nodes_copy.remove(random_node2)

                color_node(G1, random_node1, g1_color_mapping,len(mixed_g1_nodes_copy)==0)
                color_node(G2, random_node2, g2_color_mapping,len(mixed_g2_nodes_copy)==0)

                if is_endless:
                    time.sleep(0.75)
                    plt.figure(figsize=(12, 6))

                    plt.subplot(121)
                    nx.draw(G1, pos1, with_labels=True, labels=G1_labels, node_color=list(g1_color_mapping.values()), node_size=500)
                    plt.title("Graph G1 with labels")

                    plt.subplot(122)
                    nx.draw(G2, pos2, with_labels=True, labels=G2_labels, node_color=list(g2_color_mapping.values()), node_size=500)
                    plt.title("Graph G2 with labels")

                    plt.show()
                else:
                    if iteration==iter_number:
                        plt.figure(figsize=(12, 6))

                        plt.subplot(121)
                        nx.draw(G1, pos1, with_labels=True, labels=G1_labels, node_color=list(g1_color_mapping.values()), node_size=500)
                        plt.title("Graph G1 with labels")

                        plt.subplot(122)
                        nx.draw(G2, pos2, with_labels=True, labels=G2_labels, node_color=list(g2_color_mapping.values()), node_size=500)
                        plt.title("Graph G2 with labels")
                        plt.show()
                        return

def main():
    get_images(False,75000)

if __name__== "__main__":
    main()


