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
        self._years=self._model.getYears()
        for year in self._years:
            self._view.ddAnno.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        year=self._view.ddAnno.value
        nodes=self._model.crea_grafo(year)
        self._view.txtResult.controls.append(ft.Text(self._model.descriviGrafo()))
        self._view.ddDirector.enabled=False
        self._view.btnRegistiAdiacenti.disabled=False
        self._view.btnRegistiAffini.disabled=False
        for node in nodes:
            self._view.ddDirector.options.append(ft.dropdown.Option(text=node, data=node,on_click=self.readDDRegist))
        self._view.update_page()

    def readDDRegist(self,e):
        if e.control.data is None:
            self._selectedRegista=None
        else:
            self._selectedRegista=e.control.data
        print(f"redDDTems called -- {self._selectedRegista}")

    def handleRegistiAdiacenti(self, e):
        self._view.txtResult.clean()
        adiacenti=self._model.getAdiacenti(self._selectedRegista)
        for edge in adiacenti:
            (self._view.txtResult.controls.append(ft.Text(f" {edge[1]}: attori condivisi {edge[2]["weight"]}")))
        self._view.update_page()

    def handleRegistiAffini(self, e):
        try:
            self._nattori=int(self._view.attoriCondivisi.value)
        except ValueError:
            (self._view.txtResult.controls.append(ft.Text(f" Errore, inserire un numero")))
            self._view.update_page()
            return
        path=self._model.cercaRegistiAffini(self._nattori, self._selectedRegista)
        for edge in path:
            self._view.txtResult.controls.append(ft.Text(f"{edge[0]} --> {edge[1]}: {edge[2]}"))
        self._view.update_page()