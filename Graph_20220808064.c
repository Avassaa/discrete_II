#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>


// Graph structure
typedef struct Graph {
    int V;          // Number of vertices
    int** adj;      // Pointer to an array containing adjacency lists
    int* adjSize;   // Array to store the size of each adjacency list
    int** weights;
    int* colors;
    int* graphColSize;
} Graph;

// Function to create a graph of V vertices
Graph* createGraph(int V) {
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    printf("Size of a graph in bytes: %d\n", sizeof(Graph));
    printf("Size of an integer in bytes: %d\n", sizeof(int));
    printf("Size of an integer pointer in bytes: %d\n", sizeof(int*));
    printf("Size of an integer pointer pointer in bytes: %d\n", sizeof(int**));
    graph->V = V;
    graph->graphColSize = (int*)malloc(V * sizeof(int));

    // Create an array of pointers for each vertex's adjacency list
    graph->adj = (int**)malloc(V * sizeof(int*));
    graph->weights=(int**)malloc(V*sizeof(int*));
    graph->adjSize = (int*)malloc(V * sizeof(int));
    graph->colors=(int*)malloc(V*sizeof(int));
    // Initialize each adjacency list as empty by setting size to 0
    for (int i = 0; i < V; i++) {
        graph->weights[i]=NULL;
        graph->adj[i] = NULL; // No adjacency list yet
        graph->adjSize[i] = 0; // Initial size is 0
        graph->graphColSize[i]=0;
    }

    return graph;
}

// Function to add an edge to an undirected graph
void addEdge(Graph* graph, int src, int dest,int weight) {
    // Add an edge from src to dest. A new node is added to the adjacency list of src.
    // The node is added at the beginning for simplicity.
    // Resize the adjacency list for src and add dest
    graph->adjSize[src]++;
    graph->adj[src] = (int*)realloc(graph->adj[src], graph->adjSize[src] * sizeof(int));
    graph->adj[src][graph->adjSize[src] - 1] = dest;
    graph->weights[src]=(int*)realloc(graph->weights[src],graph->adjSize[src]*sizeof(int));
    graph->weights[src][graph->adjSize[src]-1]=weight;
    graph->graphColSize[src]++;


    // Since the graph is undirected, add an edge from dest to src as well
    graph->adjSize[dest]++;
    graph->graphColSize[dest]++;
    graph->adj[dest] = (int*)realloc(graph->adj[dest], graph->adjSize[dest] * sizeof(int));
    graph->adj[dest][graph->adjSize[dest] - 1] = src;
    graph->weights[dest]=(int*)realloc(graph->weights[dest],graph->adjSize[dest]*sizeof(int));
    graph->weights[dest][graph->adjSize[dest]-1]=weight;

}

// Function to free the graph memory
void freeGraph(Graph* graph) {
    for (int i = 0; i < graph->V; i++) {
        free(graph->adj[i]);     // Free adjacency list of vertex i
        free(graph->weights[i]); // Free weights array of vertex i
    }
    free(graph->adj);     // Free the array of adjacency lists
    free(graph->weights); // Free the array of weights arrays
    free(graph->adjSize);  // Free the array of adjacency list sizes
    free(graph->colors);   // Free the array of colors
    free(graph->graphColSize); // Free the array of graphColSize
    free(graph);           // Finally, free the graph
}


bool isBipartite(int** graph, int graphSize, int* graphColSize) {
    int* colors = (int*)malloc(graphSize * sizeof(int));
    for (int i = 0; i < graphSize; ++i) {
        colors[i] = -1; // Initialize colors as -1 (uncolored)
    }

    // Queue for BFS
    int* queue = (int*)malloc(graphSize * sizeof(int));

    for (int i = 0; i < graphSize; ++i) {
        if (colors[i] == -1) { // If the node is uncolored, start BFS from this node
            int front = 0, rear = 0;
            queue[rear++] = i; // Enqueue
            colors[i] = 0; // Color the first node with color 0

            while (front < rear) {
                int node = queue[front++]; // Dequeue

                for (int j = 0; j < graphColSize[node]; ++j) {
                    int adj = graph[node][j];
                    if (colors[adj] == -1) { // If the adjacent node is uncolored, color it with an opposite color
                        colors[adj] = 1 - colors[node];
                        queue[rear++] = adj; // Enqueue
                    } else if (colors[adj] == colors[node]) {
                        // If the adjacent node has the same color, the graph is not bipartite
                        free(colors);
                        free(queue);
                        return false;
                    }
                }
            }
        }
    }

    free(colors);
    free(queue);
    return true; // If all nodes are successfully colored, the graph is bipartite
}

void colorGraph(Graph* graph,int** adjList,int graphSize){
    for (int i = 0; i < graphSize; ++i) {
        graph->colors[i] = -1; // Initialize colors as -1 (uncolored)
    }

    // Queue for BFS
    int* queue = (int*)malloc(graphSize * sizeof(int));

    for (int i = 0; i < graphSize; ++i) {
        if (graph->colors[i] == -1) { // If the node is uncolored, start BFS from this node
            int front = 0, rear = 0;
            queue[rear++] = i; // Enqueue
            graph->colors[i] = 0; // Color the first node with color 0

            while (front < rear) {
                int node = queue[front++]; // Dequeue

                for (int j = 0; j < graph->graphColSize[node]; ++j) {
                    int adj = adjList[node][j];
                    if (graph->colors[adj] == -1) { // If the adjacent node is uncolored, color it with an opposite color
                        graph->colors[adj] = 1 - graph->colors[node];
                        queue[rear++] = adj; // Enqueue
                    }
                }
            }
        }
    }



}


bool isAlmostBipartite(Graph* graph, int upperBound) {
    colorGraph(graph, graph->adj, graph->V);
    int count = 0;
    int graph_len = graph->V;

    for (int i = 0; i < graph_len; i++) {
        int* current = graph->adj[i]; //get row of adj array

        for (int j = 0; j < graph->adjSize[i]; j++) {
            int cmp = current[j];//get int from adj array

            if (graph->colors[i] == graph->colors[cmp]) {
                int* weight_list=graph->weights[i];//get row of weights
                count+=weight_list[j];
            }
        }
    }

    if (count <= upperBound) {
        printf("Is almost bipartite.\n");
        return true;
    } else {
        printf("Not almost bipartite.\n");
        return false;
    }
}



void printGraph(Graph* graph) {
    for(int i=0; i<graph->V; i++) {
        printf("%d: ",i);
        for(int j=0; j<graph->adjSize[i]; j++) {
            printf("%d,W(%d), ",graph->adj[i][j],graph->weights[i][j]);
        }
        printf("\n");
    }
}



int main() {
    // Create a graph given in the above example
    int V = 9; // Number of vertices
    Graph* graph = createGraph(V);
    addEdge(graph, 0, 1,3);
    addEdge(graph, 1, 2,1);
    addEdge(graph, 2, 3,4);
    addEdge(graph, 3, 4,7);
    addEdge(graph, 4, 5,1);
    addEdge(graph, 5, 0,9);
    addEdge(graph, 0, 6,2);
    addEdge(graph, 1, 6,2);
    addEdge(graph, 5, 6,1);
    addEdge(graph, 6, 7,9);
    addEdge(graph, 6, 8,5);
    addEdge(graph, 7, 8,1);
    addEdge(graph, 7, 4,2);
    addEdge(graph, 4, 8,1);


    addEdge(graph, 4, 0,12);
    printGraph(graph);


    int* graphColSize = (int*)malloc(V * sizeof(int));
    for (int i = 0; i < V; i++) {
        graphColSize[i] = graph->adjSize[i];
    }

    // Check if the graph is bipartite
    bool result = isBipartite(graph->adj, V, graphColSize);
    bool almstbipartite= isAlmostBipartite(graph,6);


    // Clean up
    freeGraph(graph);
    free(graphColSize);

    return 0;
}