import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._fermataPartenza = None
        self._fermataArrivo = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):
        self._model.buildGraphPesatoVelocita()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"sono stati trovati {self._model.get_num_nodes()} nodi "))
        self._view.lst_result.controls.append(ft.Text(f"sono stati trovati {self._model.get_num_edges()} edges"))
        self._view._btnCalcola.disabled = False
        self._view.update_page()

    def handleCercaRaggiungibili(self,e):
        if self._fermataPartenza is None:
            self._view.controls.create_alert("Errore", "Selezionare una stazione di partenza")
            return
        else:
            raggiungibili = self._model.getBFSNodesfromEdges(self._fermataPartenza)
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text(f"di seguito la lista di fermate raggiungibili partendo da {self._fermataPartenza}"))
            for nodo in raggiungibili:
                self._view.lst_result.controls.append(ft.Text(f"{nodo}"))
            self._view.update_page()

    def handleCercaShortestPath(self,e):
        if self._fermataPartenza is None or self._fermataArrivo is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Errore: selezionare sia la stazione di partenza che quella di arrivo.", color="red"))
            self._view.update_page()
            return
        tottime, path  = self._model.getShortestPath(self._fermataPartenza,self._fermataArrivo)
        if path ==[]:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Non esiste un percorso tra le due fermate selezionate.", color="red"))
            self._view.update_page()
            return
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"il percorso trovato ha lunghezza {tottime} e i seguenti nodi:", color="green"))
        for nodo in path:
            self._view.lst_result.controls.append(ft.Text(f"{nodo}"))
        self._view.update_page()





    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data
