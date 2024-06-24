import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None



    def load_interface(self):
        # title
        self._title = ft.Text("simulazione esame 24/01/2024", color="blue", size=24)
        self._page.controls.append(self._title)

        #row1
        self.ddAnno = ft.Dropdown(label="Anno")
        self.btnCreaGrafo = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([ft.Container(self.ddAnno, width=300),
                       ft.Container(self.btnCreaGrafo, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)
        self._controller.fillDDAnno()

        # row2
        self.ddDirector = ft.Dropdown(label="Director")
        self.btnRegistiAdiacenti = ft.ElevatedButton(text="Registi adiacenti", on_click=self._controller.handleRegistiAdiacenti, disabled=True)
        row2 = ft.Row([ft.Container(self.ddDirector, width=300),
                       ft.Container(self.btnRegistiAdiacenti, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # row3
        self.attoriCondivisi = ft.TextField(label="# Attori condivisi")
        self.btnRegistiAffini = ft.ElevatedButton(text="Cerca registi affini",
                                                     on_click=self._controller.handleRegistiAffini, disabled=True)
        row3 = ft.Row([ft.Container(self.attoriCondivisi, width=300),
                       ft.Container(self.btnRegistiAffini, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        self.txtResult = ft.ListView(auto_scroll=True)
        row4 = ft.Row([ft.Container(self.txtResult)])
        self._page.controls.append(row4)



        self._page.update()
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
