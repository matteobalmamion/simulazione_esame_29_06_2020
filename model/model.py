import copy
import random
from math import sqrt
#from geopy.distance import geodesic

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._idMap={}


    def getYears(self):
        return [2004,2005,2006]

    def crea_grafo(self,year):
        self._grafo.clear()
        nodes=DAO.getDirectorsYear(year)
        for node in nodes:
            self._grafo.add_node(node)
            self._idMap[node.id] = node
        edges=DAO.getEdges(year)
        for edge in edges:
            self._grafo.add_edge(self._idMap[edge[0]],self._idMap[edge[1]], weight=edge[2])
        return self._grafo.nodes

    def descriviGrafo(self):
        return f"Nodi: {len(self._grafo.nodes)} Archi: {len(self._grafo.edges)}"

    def getAdiacenti(self,regista):
        neighbors=self._grafo.neighbors(regista)
        neighborsEdges=[]
        for neighbor in neighbors:
            neighborsEdges.append((regista,neighbor,self._grafo[neighbor][regista]))
        return neighborsEdges

    def cercaRegistiAffini(self,nAttori,regista):
        neighbors=self._grafo.neighbors(regista)
        visitati=[regista]
        self._solBest=[]
        self._costBest=0
        for neighbor in neighbors:
            visitati.append(neighbor)
            self._ricorsione(nAttori,visitati)
            visitati.pop()
        path=[]
        for i in range(self._costBest):
            if i == 0:
                continue
            v=self._solBest[i]
            v0=self._solBest[i-1]
            w=self._grafo.get_edge_data(v,v0)
            path.append((v0,v,w))
        return path

    def _ricorsione(self,nAttori,visitati):
        v0=visitati[-1]
        neighborsll = list(self._grafo.neighbors(v0))
        neighbors=[]
        for nei in neighborsll:
            if nei not in visitati:
                neighbors.append(nei)
        if self.sommActor(visitati)>=nAttori or len(neighbors)==0:
            if self._costBest<len(visitati):
                self._costBest=len(visitati)
                self._solBest=copy.deepcopy(visitati)
            return
        for neighbor in neighbors:
            if neighbor not in visitati:
                visitati.append(neighbor)
                self._ricorsione(nAttori,visitati)
                visitati.pop()

    def sommActor(self,visitati):
        sum=0
        for i in range(len(visitati)):
            if i==0:
                continue
            sum+=self._grafo[visitati[i]][visitati[i-1]]["weight"]
        return sum