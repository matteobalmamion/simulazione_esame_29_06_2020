from database.DB_connect import DBConnect
from model.director import Director


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDirectors(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
                    from directors d , movies m , movies_directors md 
                    where d.id = md.director_id 
                    and m.id = md.movie_id 
                    and m.`year` = %s"""

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(Director(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select d.id as id1, d2.id as id2, count(distinct a.id) as count
                    from directors d , movies m , movies_directors md, roles r , actors a, directors d2 , movies m2 , movies_directors md2, roles r2 , actors a2
                    where d.id = md.director_id 
                    and m.id = md.movie_id 
                    and a.id = r.actor_id 
                    and r.movie_id = m.id 
                    and m.`year` = %s
                    and d2.id = md2.director_id 
                    and m2.id = md2.movie_id 
                    and a2.id = r2.actor_id 
                    and r2.movie_id = m2.id 
                    and m.`year` = m2.`year` 
                    and a.id = a2.id 
                    and d.id<d2.id 
                    group by d.id, d2.id """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append([row["id1"], row["id2"], row["count"]])

        cursor.close()
        conn.close()
        return result

