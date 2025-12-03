import networkx as nx
from database.dao import DAO
import random
from collections import deque


class Model:
    def __init__(self):
        self.G = nx.Graph()

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO
        lista_connessioni = DAO.read_connessioni(year)
        set_id_rifugi = set()
        for connessione in lista_connessioni:
            set_id_rifugi.add(connessione.id_rifugio1)
            set_id_rifugi.add(connessione.id_rifugio2)
        dizio_rifugi = DAO.read_rifugi(set_id_rifugi)

        #costruzione del grafo
        self.G.add_nodes_from(dizio_rifugi.values())
        for connessione in lista_connessioni:
            self.G.add_edge(dizio_rifugi[connessione.id_rifugio1], dizio_rifugi[connessione.id_rifugio2])

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO
        return list(self.G.nodes())

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO
        return self.G.degree(node)

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        return nx.number_connected_components(self.G)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO
        metodo = random.randint(1, 4)
        if metodo == 1:
            print('using nx.dfs_tree()...')
            T = nx.dfs_tree(self.G, start)
            T.remove_node(start)
            return T.nodes()

        elif metodo == 2:
            print('using nx.bfs_tree()...')
            T = nx.bfs_tree(self.G, start)
            T.remove_node(start)
            return T.nodes()

        elif metodo == 3:
            print('using recursive algorithm...')
            visitati = set()
            visitati.add(start)
            self.algoritmo_ricorsivo(start, visitati)
            visitati.discard(start)
            return visitati

        elif metodo == 4:
            print('using iterative algorithm...')
            return self.algoritmo_iterativo(start)


    def algoritmo_ricorsivo(self, start, visitati):
        for nodo in self.G.neighbors(start):
            if nodo not in visitati:
                visitati.add(nodo)
                self.algoritmo_ricorsivo(nodo, visitati)

    def algoritmo_iterativo(self, start):
        visitati = set()
        da_visitare = deque([start])
        while da_visitare:
            nodo = da_visitare.popleft()
            if nodo not in visitati:
                visitati.add(nodo)
                for vicino in self.G.neighbors(nodo):
                    da_visitare.append(vicino)
        visitati.discard(start)
        return visitati