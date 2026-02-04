import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.g = nx.DiGraph()
        self.artists = []
        self.dao = DAO()

    def build_graph(self, role: str):
        self.g.clear()
        lista_artisti=self.dao.get_artists(role)
        '''for artist in lista_artisti:
            self.g.add_node(artist)
        print(self.g)'''
        #restituire i nodi collegati
        self.dizionario1={}
        for artist in lista_artisti:
            self.dizionario1[artist.artist_id]=artist
        self.dizionario=self.dao.get_approvati(role,self.dizionario1)
        print(len(self.dizionario))
        for artita1 in self.dizionario:
            for artita2 in self.dizionario:
                if artita1>artita2:
                    art1=self.dizionario[artita1]
                    art2=self.dizionario[artita2]
                    if art1.peso==0 or art2.peso==0:
                        pass
                    else:
                        if art1.peso==art2.peso:
                            self.g.add_node(artita1)
                            self.g.add_node(artita2)
                        elif art1.peso>art2.peso:
                            self.g.add_edge(artita2, artita1,weight=art1.peso-art2.peso)
                        else:
                            self.g.add_edge(artita1,artita2,weight=art2.peso-art1.peso)
        print(self.g)
        return len(self.g.nodes),len(self.g.edges)



    def classifica(self):
        lista=[]
        for nodo in self.g.nodes():
            peso=self.bilancio_pesi(self.g,nodo)
            if peso!=0:
                lista.append([nodo,peso])

        lista.sort(key=lambda x: x[1], reverse=True)
        print(lista)
        return lista

    def bilancio_pesi(self,G, nodo):
        entranti = sum(
            data.get("weight", 0)
            for _, _, data in G.in_edges(nodo, data=True)
        )

        uscenti = sum(
            data.get("weight", 0)
            for _, _, data in G.out_edges(nodo, data=True)
        )

        return uscenti - entranti

    def percorso(self,lunghezza,id):
        print(id)
        nodo=self.dizionario[int(id)]
        self.peso=0
        self.percorso=0
        self.ricorsione([nodo],lunghezza,0)
        return self.percorso,self.peso
    def ricorsione(self,parziale,lunghezza,peso):

        ultimo_nodo=parziale[-1]
        if len(parziale)==lunghezza:

            if  peso>self.peso:
                    print(self.percorso)
                    self.peso=peso

                    self.percorso=parziale.copy()
            return
        else:


            for vicino in list(self.g.successors(ultimo_nodo)):
                if vicino not in parziale:
                    parziale.append(vicino)
                    self.ricorsione(parziale,lunghezza,peso+self.g[ultimo_nodo][vicino]["weight"])
                    parziale.pop()




    def get_ruoli(self):
        return self.dao.get_ruoli()

