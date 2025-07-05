from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def  get_all_edges():
        cnx = DBConnect.get_connection()

        result = []

        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM connessione")
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        cnx.close()

        return result


    @staticmethod
    def get_all_edges_pesati():
        cnx = DBConnect.get_connection()
        result = []
        cursor =cnx.cursor(dictionary=True)

        query= """select c.id_stazP, c.id_stazA, count(*) as wight
                   from connessione as c
                   group by c.id_stazP, c.id_stazA
                   order by count(*) desc"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["id_stazP"],row["id_stazA"], row["wight"]))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getEdgesVelocita():
        cnx = DBConnect.get_connection()
        result = []
        cursor = cnx.cursor(dictionary=True)

        query = """select c.id_stazP as id_stazP, c.id_stazA as id_stazA, max(l.velocita) as velocita
                    from connessione as c, linea l
                    where c.id_linea =l.id_linea
                    group by c.id_stazP, c.id_stazA
                    order by id_stazP asc, id_stazA asc"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["velocita"]))

        cursor.close()
        cnx.close()
        return result



