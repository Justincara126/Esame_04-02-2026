import flet as ft
from database.dao import DAO


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self.dao=DAO

    def handle_crea_grafo(self, e):
        ruolo=self._view.dd_ruolo.value
        self._view.btn_classifica.disabled = False
        self._view.btn_cerca_percorso.disabled = False
        if ruolo:
            print(ruolo)
            nodi,a=self._model.build_graph(ruolo)
            self._view.btn_classifica.disabled = False
            self._view.btn_cerca_percorso.disabled = False
            self._view.dd_iniziale.disabled = False
            self._view.list_risultato.controls.append(ft.Text(f'il grafo ha {nodi} nodi {a} archi'))
            self._view.dd_iniziale.options.clear()
            for artist in self._model.g.nodes:
                print(artist)
                self._view.dd_iniziale.options.append(ft.dropdown.Option(key=self._model.dizionario[artist].artist_id, text=self._model.dizionario[artist].name))

        self._view.update()

    def handle_classifica(self, e):
        coppie=self._model.classifica()
        self._view.list_risultato.clean()
        print(coppie)
        self._view.list_risultato.controls.append(ft.Text(f'ordine artisti:'))
        for i in coppie:
            self._view.list_risultato.controls.append(ft.Text(f'{self._model.dizionario[i[0]]}    {i[1]+1}'))
        self._view.update()

    def popola_dropdown_ruolo(self):
        lista_ruoli=self._model.get_ruoli()
        for i in lista_ruoli:
            self._view.dd_ruolo.options.append(ft.dropdown.Option(key=i,text=i))
        self._view.update()

    def percorso(self,e):
        try:
            n= int(self._view.input_L.value)
            print(n)
            if n < 3 or n>len(self._model.g.nodes):
                return self._view.show_alert('maggiore di 3 e minore del numero totale di nodi')
            else:
                c=self._view.dd_iniziale.value
                percorso,peso=self._model.percorso(n,c)
                for i in percorso:
                    print(i)
                print(peso)
        except ValueError or TypeError:
            return self._view.show_alert('inserire un numero')
        self._view.update()

















