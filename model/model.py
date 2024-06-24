import copy
import random
from math import sqrt
#from geopy.distance import geodesic

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.idMap = {}

    def buildGraph(self, anno):
        self.graph.clear()
        nodes = DAO.getDirectors(anno)
        self.graph.add_nodes_from(nodes)
        for i in nodes:
            self.idMap[i.id] = i
        archi = DAO.getArchi(anno)
        for a in archi:
            self.graph.add_edge(self.idMap[a[0]], self.idMap[a[1]], weight= a[2])

    def cercaRegistiAdiacenti(self, regista):
        reg = self.idMap[regista]
        vicini = self.graph.neighbors(reg)
        dizio = {}
        for v in vicini:
            dizio[v] = self.graph[reg][v]["weight"]
        dizioSorted = sorted(dizio, key=lambda x:dizio[x], reverse=True)
        result = {}
        for i in dizioSorted:
            result[i] = self.graph[reg][i]["weight"]

        return result

    def calcolaPercorso(self, regista, nAttori):
        reg = self.idMap[regista]
        self.solBest = []
        parziale = [reg]
        self.ricorsione(parziale, nAttori, reg)
        print(self.solBest)

    def ricorsione(self, parziale, nAttori, regista):
        vicini = list(self.graph.neighbors(regista))
        if len(vicini) == 0:
            if len(parziale) == 1:
                return
            if len(parziale) > len(self.solBest):
                self.solBest = copy.deepcopy(parziale)
        for v in vicini:
            parziale.append(v)
            if self.vincoli(parziale, v, regista, nAttori):
                self.ricorsione(parziale, nAttori, v)
            parziale.pop()

    def vincoli(self, parziale, v, nodo, nMax):
        for i in range(len(parziale) - 1):
            if {nodo, v} == {parziale[i], parziale[i+1]}:
                return False
        if self.calcolaLunghezza(parziale) > nMax:
            return False
        return True

    def calcolaLunghezza(self, parziale):
        tot = 0
        for p in range(len(parziale)-1):
            tot+= self.graph[parziale[p]][parziale[p+1]]["weight"]
        return tot



    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)