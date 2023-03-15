import copy
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


def grafica_arbol_con_steiner(puntos_originales, puntos_steiner, title):
    tam_fuente = 10
    plt.rcParams["font.family"] = "caladea"
    aristas_color = "#49817A"
    ptos_originales_color = "#DA536E"
    steiner_color = "#00C9B8"
    steiner_original = steiner.Steiner(puntos_originales.copy())
    steiner_original.calcula_arbol_euclidiano_minimo()
    steiner_original.calcula_peso_total_arbol()
    steiner_steiner = steiner.Steiner(puntos_steiner.copy())
    steiner_steiner.calcula_arbol_euclidiano_minimo()
    steiner_act = steiner.Steiner(puntos_originales.copy() + puntos_steiner.copy())
    steiner_act.calcula_arbol_euclidiano_minimo()
    arbol_act = steiner_act.arbol
    aristas_act = [(u, v) for (u, v, d) in arbol_act.edges(data=True)]
    vertices_originales = {v: [v[0], v[1]] for v in steiner_original.arbol.nodes}
    vertices_steiner = {v: [v[0], v[1]] for v in steiner_steiner.arbol.nodes}
    vertices_act = {v: [v[0], v[1]] for v in arbol_act.nodes}
    print("peso", steiner_original.peso)
    plt.title(title, fontsize=tam_fuente)
    nx.draw_networkx_nodes(steiner_original.arbol, vertices_originales, node_size=30, node_color=ptos_originales_color)
    nx.draw_networkx_nodes(steiner_steiner.arbol, vertices_steiner, node_size=30, node_color=steiner_color)
    nx.draw_networkx_edges(arbol_act, vertices_act, edgelist=aristas_act, width=2, edge_color=aristas_color)

    plt.show()

def ejecuta_PSO(nombre_archivo):
    archivo = open(nombre_archivo)
    datos = json.load(archivo)
    iteracion_max = datos['iteración_max']
    cantidad_enjambres = datos['cantidad_enjambres']
    tam_poblacion = datos['tam_poblacion']
    ejecuciones = datos["ejecuciones"]
    puntos_encontrados_json = datos['puntos_encontrados']
    puntos_problema = datos['puntos_originales']
    s_original = steiner.Steiner(copy.copy(puntos_problema))
    s_original.calcula_arbol_euclidiano_minimo()
    s_original.calcula_peso_total_arbol()
    peso_minimo = s_original.peso
    puntos_steiner = copy.copy(s_original.puntos)
    st = steiner.Steiner(puntos_problema.copy())
    for i in range(ejecuciones):
        st.set_steiner(puntos_problema.copy())
        st.calcula_arbol_euclidiano_minimo()
        st.calcula_peso_total_arbol()
        st.optimizacion_particulas_steiner(iteracion_max,
                                           cantidad_enjambres,
                                           tam_poblacion,
                                           len(puntos_encontrados_json))
        if st.peso < peso_minimo:
            peso_minimo = copy.copy(st.peso)
            puntos_steiner = st.puntos.copy()
            print("MEJORA VALOR MINIMO ", puntos_steiner, peso_minimo)
        st.borra_steiner()
    nombre_sin_extension = nombre_archivo[0:nombre_archivo.rindex('.')]
    nuevo_archivo = nombre_sin_extension + "_resultados.json"
    datos = {'peso_original': s_original.peso,
             'peso_mejorado': peso_minimo,
             'porcentaje_mejora': 100 - (peso_minimo * 100 / s_original.peso),
             'puntos_encontrados': puntos_steiner}
    with open(nuevo_archivo, 'w') as outfile:
        outfile.write(json.dumps(datos, indent=2))

if __name__ == '__main__':
    # nombre_archivo = input()
    archivo = open('../Ejemplos/ejemplo-decroos.json')
    datos = json.load(archivo)
    # ejecuta_algoritmo_con_grafica(30, 10, 15, [(-4, 0), (0, 6), (4, 0)])
    iteracion_max = datos['iteración_max']
    cantidad_enjambres = datos['cantidad_enjambres']
    tam_poblacion = datos['tam_poblacion']
    ejecuciones = datos["ejecuciones"]
    puntos_encontrados_json = datos['puntos_encontrados']
    puntos_problema = datos['puntos_originales']
    s_original = steiner.Steiner(copy.copy(puntos_problema))
    s_original.calcula_arbol_euclidiano_minimo()
    s_original.calcula_peso_total_arbol()
    peso_minimo = s_original.peso
    puntos_steiner = copy.copy(s_original.puntos)
    # st = steiner.Steiner(puntos_problema.copy())

    # puntos_steiner = [[20307.81814400283, 3804.0630296756885]]

    # resultados_bib = "Arbol steiner en bibliografía"
   # arbol_mio = "Arbol obtenido"
    # arbol_no_s = "Arbol original"
   # grafica_arbol_con_steiner(puntos_problema, puntos_steiner, arbol_mio)    # Para graficar
    ejecuta_PSO("../Ejemplos/ejemplo-sinfuente.json")
    #s = steiner.Steiner(puntos_steiner + datos["puntos_encontrados"])
    #s.calcula_arbol_euclidiano_minimo()
    #s.calcula_peso_total_arbol()
    #print("Inicio ------> Peso original ", s.peso, " puntos ", s.puntos) # Para graficar inicial


