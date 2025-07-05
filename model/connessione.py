from dataclasses import dataclass

@dataclass
class Connessione:
    id_linea : int
    id_stazP : int
    id_stazA : int
    id_connessione : int