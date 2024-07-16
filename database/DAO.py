from database.DB_connect import DBConnect
from model.director import Director


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDirectorsYear(year):
        conn=DBConnect.get_connection()
        result=[]
        query="""select  distinct d.id, d.first_name ,d.last_name 
from movies_directors md  ,directors d ,movies m 
where d.id =md.director_id and m.id =md.movie_id and m.`year` =%s """
        cursor=conn.cursor(dictionary=True)
        cursor.execute(query,(year,))
        for row in cursor:
            result.append(Director(row["id"],row["first_name"],row["last_name"]))
        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getEdges(year):
            conn = DBConnect.get_connection()
            result = []
            query = """select md2.director_id as m0, md0.director_id as m2, count(r0.actor_id) as n
from movies m0, movies m2 , movies_directors md0, movies_directors md2, roles r0, roles r2 
where m2.`year` =m0.`year` and  m0.`year`=%s and m2.id =md2.movie_id and m0.id =md0.movie_id
and r2.actor_id =r0.actor_id and r2.movie_id =m2.id and r0.movie_id=m0.id and md2.director_id != md0.director_id
group by md2.director_id , md0.director_id """
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (year,))
            for row in cursor:
                result.append((row["m0"],row["m2"],row["n"]))
            cursor.close()
            conn.close()

            return result

