import json
import matplotlib.pyplot as plt
import networkx as nx
import src.steiner as steiner


def ejecuta_algoritmo_con_grafica(iteracion_max, cantidad_enjambres, tam_poblacion, puntos_iniciales):
    fuente = 'caladea'
    tam_fuente = 10
    plt.rcParams["font.family"] = "caladea"
    edge_color = "#511F29"
    node_color = "#DA536E"
    s = steiner.Steiner(puntos_iniciales)
    s.calcula_arbol_euclidiano_minimo()
    s.calcula_peso_total_arbol()
    arbol_original = s.arbol
    aristas_originales = [(u, v) for (u, v, d) in arbol_original.edges(data=True)]
    vertices_dict = {v: [v[0], v[1]] for v in arbol_original.nodes}
    etiquetas_vertices = {v: [float(f'{v[0]:.2f}'), float(f'{v[1]:.2f}')]
                          for v in arbol_original.nodes}
    plt.subplot(121)
    plt.title("Arbol original", fontsize=tam_fuente)
    nx.draw_networkx_nodes(arbol_original, vertices_dict, node_size=350, node_color=node_color)
    nx.draw_networkx_edges(arbol_original, vertices_dict, edgelist=aristas_originales, width=2, edge_color=edge_color)
    nx.draw_networkx_labels(arbol_original, vertices_dict, font_size=tam_fuente, font_family=fuente,
                            labels=etiquetas_vertices)
    etiquetas_arbol_original = {key: float(f'{value:.2f}') for key, value in
                                nx.get_edge_attributes(arbol_original, "weight").items()}
    nx.draw_networkx_edge_labels(arbol_original, vertices_dict, etiquetas_arbol_original,
                                 font_size=tam_fuente, font_family=fuente)

    s.optimizacion_particulas_steiner(iteracion_max, cantidad_enjambres, tam_poblacion)
    grafica_steiner = s.arbol
    arbol_steiner = nx.minimum_spanning_tree(grafica_steiner)
    aristas_arbol_steiner = [(u, v) for (u, v, d) in arbol_steiner.edges(data=True)]
    vertices_steiner_dict = {v: [v[0], v[1]] for v in arbol_steiner.nodes}
    etiquetas_vertices = {v: [float(f'{v[0]:.2f}'), float(f'{v[1]:.2f}')]
                          for v in arbol_steiner.nodes}

    plt.subplot(122)
    plt.title("Arbol con puntos Steiner", fontsize=tam_fuente)
    nx.draw_networkx_nodes(arbol_steiner, vertices_steiner_dict, node_size=350, node_color=node_color)
    nx.draw_networkx_edges(arbol_steiner, vertices_steiner_dict, edgelist=aristas_arbol_steiner, width=2,
                           edge_color=edge_color)
    nx.draw_networkx_labels(arbol_steiner, vertices_steiner_dict, font_size=tam_fuente, font_family=fuente,
                            labels=etiquetas_vertices)
    etiquetas_arbol_steiner = {key: float(f'{value:.2f}') for key, value in
                               nx.get_edge_attributes(arbol_steiner, "weight").items()}
    nx.draw_networkx_edge_labels(arbol_steiner, vertices_steiner_dict, etiquetas_arbol_steiner,
                                 font_size=tam_fuente, font_family=fuente)
    plt.show()

def grafica_dos_arboles(arbol_1, arbol_2):
    fuente = 'caladea'
    tam_fuente = 10
    plt.rcParams["font.family"] = "caladea"
    edge_color = "#511F29"
    node_color = "#DA536E"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # nombre_archivo = input()
    archivo = open('../Ejemplos/ejemplo-steiner-brazil.json')
    datos = json.load(archivo)
    # ejecuta_algoritmo_con_grafica(30, 10, 15, [(-4, 0), (0, 6), (4, 0)])
    iteracion_max = datos['iteración_max']
    cantidad_enjambres = datos['cantidad_enjambres']
    tam_poblacion = datos ['tam_poblacion']
    ejecuciones = datos["ejecuciones"]
    ejecuta_algoritmo_con_grafica(iteracion_max, cantidad_enjambres, tam_poblacion, datos['puntos_originales'])