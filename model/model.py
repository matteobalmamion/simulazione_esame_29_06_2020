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
        return self.solBest
    def ricorsione(self, parziale, nAttori, regista):
        vicini = list(self.graph.neighbors(regista))
        viciniAmmissibili = self.getViciniAmmissibili(vicini, nAttori, parziale, regista)
        if len(viciniAmmissibili) == 0:
            if len(parziale) == 1:
                return
            if len(parziale) > len(self.solBest):
                self.solBest = copy.deepcopy(parziale)
        for v in viciniAmmissibili:
            if self.vincoli(parziale, v, regista, nAttori):
                parziale.append(v)
                self.ricorsione(parziale, nAttori, v)
                parziale.pop()
        # if len(parziale) > len(self.solBest):
        #     self.solBest = copy.deepcopy(parziale)
        #     #print(self.solBest)


    def getViciniAmmissibili(self, vicini, nMax, parziale, nodo):
        neigh = []
        boolean = False
        for v in vicini:
            for i in range(len(parziale)-1):
                if {parziale[-1], v} == {parziale[i], parziale[i+1]}:
                    boolean = True
            if not boolean and self.calcolaLunghezza(parziale, nodo, v) <= nMax:
                neigh.append(v)
        return neigh

    def vincoli(self, parziale, v, nodo, nMax):
        # for i in range(len(parziale) - 1):
        #     if {nodo, v} == {parziale[i], parziale[i+1]}:
        #         return False

        if self.calcolaLunghezza(parziale, nodo, v) > nMax:
            return False

        return True

    def calcolaLunghezza(self, parziale, n, v):
        tot = self.graph[n][v]["weight"]
        for p in range(len(parziale)-1):
            tot+= self.graph[parziale[p]][parziale[p+1]]["weight"]
        return tot



    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)