from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def read_connessioni(year: int):
        """
        Legge dal database la tabella connessione e restituisce una lista delle connessioni con anno minore o uguale
        a quello passato come argomento.
        :param year: Anno per il filtro
        :return: Lista di oggetti Connessione
        """
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM connessione WHERE anno <= %s", (year,))
        lista_connessioni = []
        for row in cursor:
            lista_connessioni.append(Connessione(**row))
        cursor.close()
        cnx.close()
        return lista_connessioni

    @staticmethod
    def read_rifugi(set_id_rifugi: set):
        """
        Legge dal database tutti i rifugi con id presente nell'insieme passato come argomento.
        :param set_id_rifugi: Set di interi
        :return: Dizionario di oggetti Rifugio la cui chiave è l'id
        """
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = f'SELECT * FROM rifugio WHERE id IN ({", ".join(["%s"] * len(set_id_rifugi))})'
        cursor.execute(query, tuple(set_id_rifugi))
        dizio_rifugi = {}
        for row in cursor:
            dizio_rifugi[row['id']] = Rifugio(**row)
        cursor.close()
        cnx.close()
        return dizio_rifugi


if __name__ == '__main__':
    set_id = {1, 2, 3}
    anno = 1960
    print(DAO.read_rifugi(set_id))
    print(DAO.read_connessioni(anno))