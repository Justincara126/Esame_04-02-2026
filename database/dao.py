from database.DB_connect import DBConnect
from model.artist import Artist


class DAO:

    @staticmethod
    def get_authorship():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """ SELECT * 
                    FROM authorship"""
        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        print(result)
        return result

    @staticmethod
    def get_ruoli():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT (role) as i FROM authorship"""
        cursor.execute(query)

        for row in cursor:
            result.append(row['i'])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_artists(role):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.artist_id,a.name FROM authorship p,artists a
                where a.artist_id = p.artist_id and p.role = %s
                group by a.artist_id, a.name"""
        cursor.execute(query, (role,))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        print(result)
        return result
    @staticmethod
    def get_approvati(ruolo,dizionario):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.artist_id as id,count(*) as peso FROM authorship p,artists a,objects o
                where a.artist_id = p.artist_id and p.role = %s and o.object_id=p.object_id
            and o.curator_approved=1
                group by a.artist_id"""
        cursor.execute(query, (ruolo,))

        for row in cursor:
            dizionario[row['id']].peso=row['peso']
            print(dizionario[row['id']])


        cursor.close()
        conn.close()
        return dizionario
