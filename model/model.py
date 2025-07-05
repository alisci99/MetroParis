import networkx as nx
from database.DAO import DAO
import geopy.distance


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate= {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def buildGraph(self):
        self._grafo.add_nodes_from(self._fermate)
        self.add_edges3()

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()

    def buildGraphPesatoVelocita(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesatiVelocita()


    def add_edges3(self):
        edges = DAO.get_all_edges()
        for edge in edges:
            u = self._idMapFermate[edge.id_stazP]
            v = self._idMapFermate[edge.id_stazA]
            self._grafo.add_edge(u,v)

    def addEdgesPesati(self):
        self._grafo.clear_edges()
        edges = DAO.get_all_edges_pesati()
        for e in edges:
            self._grafo.add_edge(
                self._idMapFermate[e[0]],
                self._idMapFermate[e[1]],
                weight=e[2]
            )
    def addEdgesPesatiVelocita(self):
        self._grafo.clear_edges()
        allEdges = DAO.getEdgesVelocita()
        for e in allEdges:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = getTraversalTime(u, v, e[2])
            self._grafo.add_edge(u, v, weight=peso)


    def getBFSNodesfromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        result =[]
        for u,v in archi:
            result.append(v)
        return result

    def getShortestPath(self, source, target):
        return nx.single_source_dijkstra(self._grafo, source, target)



    @property
    def fermate(self):
        return self._fermate

    def get_num_nodes(self):
        return len(self._grafo.nodes)

    def get_num_edges(self):
        return len(self._grafo.edges)

def getTraversalTime(u, v, vel):
    dist = geopy.distance.distance((u.coordX, u.coordY),
                                   (v.coordX, v.coordY)).km  # in km
    time = dist / vel * 60  # in minuti
    return time