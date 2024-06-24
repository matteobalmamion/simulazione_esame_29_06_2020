import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDAnno(self):
        anni = [2004, 2005, 2006]
        anniDD = list(map(lambda x: ft.dropdown.Option(x), anni))
        self._view.ddAnno.options = anniDD
        self._view.update_page()

    def fillDDDirector(self):
        registi = list(self._model.graph.nodes)
        registiDD = list(map(lambda x: ft.dropdown.Option(key=x.id, text=x.first_name+" "+x.last_name), registi))
        self._view.ddDirector.options = registiDD
        self._view.update_page()


    def handleCreaGrafo(self, e):
        self.anno = self._view.ddAnno.value
        if self.anno is None:
                self._view.create_alert("Anno non inserito")
                self._view.txtResult.clean()
                self._view.update_page()
                return
        self._model.buildGraph(self.anno)
        self.fillDDDirector()
        self._view.btnRegistiAdiacenti.disabled = False
        self._view.btnRegistiAffini.disabled = False
        n, e = self._model.graphDetails()
        self._view.txtResult.controls.append(ft.Text(f"Il grafo ha {n} nodi e {e} archi"))
        self._view.update_page()

    def handleRegistiAdiacenti(self, e):
        self.regista = int(self._view.ddDirector.value)
        if self.anno is None:
                self._view.create_alert("Regista non inserito")
                self._view.update_page()
                return
        result = self._model.cercaRegistiAdiacenti(self.regista)
        self._view.txtResult.controls.append(ft.Text(f"Registi adiacenti a: {self._model.idMap[self.regista].id}-{self._model.idMap[self.regista].first_name} {self._model.idMap[self.regista].last_name}"))
        for i in result:
            self._view.txtResult.controls.append(ft.Text(f"{i.id}-{i.first_name} {i.last_name} - # attori condivisi: {result[i]}"))
        self._view.update_page()

    def handleRegistiAffini(self, e):
        self.attoriCondivisi = self._view.attoriCondivisi.value
        if self.anno is "":
                self._view.create_alert("Numero di attori condivisi non inserito")
                self._view.update_page()
                return
        try:
            attInt = int(self.attoriCondivisi)
        except ValueError:
            self._view.create_alert("Numero di attori condivisi inserito non numerico")
            self._view.update_page()
            return

        self.regista = int(self._view.ddDirector.value)
        if self.anno is None:
            self._view.create_alert("Regista non inserito")
            self._view.update_page()
            return

        self._model.calcolaPercorso(self.regista, attInt)




