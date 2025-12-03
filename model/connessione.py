import datetime
from dataclasses import dataclass


@dataclass
class Connessione:
    id : int
    id_rifugio1 : int
    id_rifugio2 : int
    distanza : float
    difficolta : str
    durata : datetime.timedelta
    anno : int

    def __eq__(self, other):
        return isinstance(other, Connessione) and self.id == other.id

    def __repr__(self):
        return f"Percorso numero: {self.id}"

    def __str__(self):
        return f"Percorso numero: {self.id}"

    def __hash__(self):
        return hash(self.id)