import matplotlib.pyplot as plt
import networkx as nx
import src.steiner as steiner
import matplotlib.font_manager


def ejecuta_algoritmo_con_grafica(iteracion_max, cantidad_enjambres, tam_poblacion, puntos_iniciales):
    fuente = 'caladea'
    tam_fuente = 10
    plt.rcParams["font.family"] = "caladea"
    s = steiner.Steiner(puntos_iniciales)
    s.calcula_arbol_euclidiano_minimo()
    s.calcula_peso_total_arbol()
    arbol_original = s.arbol
    aristas_originales = [(u, v) for (u, v, d) in arbol_original.edges(data=True)]
    vertices_dict = {v: [v[0], v[1]] for v in arbol_original.nodes}
    plt.subplot(121)
    plt.title("Arbol original", fontsize=tam_fuente)
    nx.draw_networkx_nodes(arbol_original, vertices_dict, node_size=350, node_color="#DA536E")
    nx.draw_networkx_edges(arbol_original, vertices_dict, edgelist=aristas_originales, width=2, edge_color="#511F29")
    nx.draw_networkx_labels(arbol_original, vertices_dict, font_size=tam_fuente, font_family=fuente)
    etiquetas_arbol_original = {key: float(f'{value:.2f}') for key, value in
                                nx.get_edge_attributes(arbol_original, "weight").items()}
    nx.draw_networkx_edge_labels(arbol_original, vertices_dict, etiquetas_arbol_original,
                                 font_size=tam_fuente, font_family=fuente)

    puntos_steiner = s.optimizacion_particulas_steiner(iteracion_max, cantidad_enjambres, tam_poblacion)
    grafica_steiner = nx.Graph()
    for punto_i in puntos_steiner[0]:
        grafica_steiner.add_node(tuple(punto_i))
    arbol_steiner = nx.minimum_spanning_tree(G_steiner)
    aristas_arbol_steiner = [(u, v) for (u, v, d) in arbol_steiner.edges(data=True)]
    vertices_steiner_dict = {v: [v[0], v[1]] for v in arbol_steiner.nodes}
    plt.subplot(122)
    plt.title("Arbol con puntos Steiner", fontsize=tam_fuente)
    nx.draw_networkx_nodes(arbol_steiner, vertices_steiner_dict, node_size=350, node_color="#DA536E")
    nx.draw_networkx_edges(arbol_steiner, vertices_steiner_dict, edgelist=aristas_arbol_steiner, width=2,
                           edge_color="#511F29")
    nx.draw_networkx_labels(arbol_steiner, vertices_steiner_dict, font_size=tam_fuente, font_family=fuente)
    etiquetas_arbol_steiner = {key: float(f'{value:.2f}') for key, value in
                               nx.get_edge_attributes(arbol_steiner, "weight").items()}
    nx.draw_networkx_edge_labels(arbol_steiner, vertices_steiner_dict, etiquetas_arbol_steiner,
                                 font_size=tam_fuente, font_family=fuente)
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fuente = 'caladea'
    tam_fuente = 10
    plt.rcParams["font.family"] = "caladea"
    s = steiner.Steiner([(-4, 0), (0, 6), (4, 0)])
    s.calcula_arbol_euclidiano_minimo()
    s.calcula_peso_total_arbol()
    # pos = nx.draw_spectral(s.arbol, node_color="#DA536E", edge_color="#511F29")

    G = s.arbol
    elarge = [(u, v) for (u, v, d) in s.arbol.edges(data=True)]
    # pos = nx.draw_spectral(G, seed=7)  # positions for all nodes - seed for reproducibility

    pos = {v: [v[0], v[1]] for v in s.arbol.nodes}
    plt.subplot(121)
    plt.title("Gráfica original", fontsize=tam_fuente)
    # nodes

    nx.draw_networkx_nodes(G, pos, node_size=350, node_color="#DA536E")

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2, edge_color="#511F29")

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=tam_fuente, font_family=fuente)
    # edge weight labels
    edge_labels = {key: float(f'{value:.2f}') for key, value in
                   nx.get_edge_attributes(G, "weight").items()}

    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=tam_fuente, font_family=fuente)

    nuevos_puntos = s.optimizacion_particulas_steiner(30, 10, 15)
    G_steiner = nx.Graph()
    for p_i in nuevos_puntos[0]:
        G_steiner.add_node(tuple(p_i))
    g_steiner_arbol = nx.minimum_spanning_tree(G_steiner)
    aristas_steiner = [(u, v) for (u, v, d) in g_steiner_arbol.edges(data=True) if d["weight"] > 0]
    steiner_pos = {}
    for p_i in g_steiner_arbol.nodes:
        steiner_pos[p_i] = p_i
    plt.subplot(122)
    plt.title("Gráfica con puntos steiner", fontsize=tam_fuente)
    # nodes
    nx.draw_networkx_nodes(g_steiner_arbol, steiner_pos, node_size=350, node_color="#DA136E")

    # edges
    nx.draw_networkx_edges(g_steiner_arbol, steiner_pos, edgelist=aristas_steiner, width=2, edge_color="#511D29")

    # node labels
    nx.draw_networkx_labels(g_steiner_arbol, steiner_pos, font_size=tam_fuente, font_family=fuente)
    # edge weight labels
    edge_labels_s = nx.get_edge_attributes(g_steiner_arbol, "weight")
    nx.draw_networkx_edge_labels(g_steiner_arbol, steiner_pos, edge_labels_s, font_size=tam_fuente, font_family=fuente)

    plt.show()
