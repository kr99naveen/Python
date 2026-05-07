import sqlite3
from app.api.schemas.shipment import BaseShipment, ReadShipment, UpdateShipment

class Database:
    def __init__(self):
        # make the connection
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        # get the cursor
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipments (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT   
            )
        """)

    
    def create(self, shipment : BaseShipment)->int:
        self.cur.execute("SELECT MAX(id) FROM shipments")
        result = self.cur.fetchone()
        print("#"*20,result)
        new_id = 12701
        if result[0] is not None:
            new_id = result[0]+1
        self.cur.execute("""
            INSERT INTO shipments
            VALUES (:id, :content, :weight, :status)
        """,
            {
                "id" : new_id,
                 **shipment.model_dump(),
                 "status" : "placed"
            }
        )
        self.conn.commit()
        return new_id

    def get(self, id : int)->ReadShipment | None:
        self.cur.execute("""
            SELECT * FROM shipments
            WHERE id=:id
        """,{
            "id" : id
        })
        result = self.cur.fetchone()
        keys = ["id", "content", "weight", "status"]
        return dict(zip(keys, result))if result else None
    
    def getAll(self)->list[ReadShipment] | None:
        self.cur.execute("""
            SELECT * FROM shipments
        """)
        result = self.cur.fetchall()
        keys = ["id", "content", "weight", "status"]
        return [dict(zip(keys, row)) for row in result] if result else None

    def update(self,id:int,shipment:UpdateShipment)->ReadShipment|None:
        print("#"*50)
        data = self.get(id)
        if data is None:
            return None
        self.cur.execute("""
            UPDATE shipments
            SET status=:status
            WHERE id=:id
        """,{
            "id" : id,
            **shipment.model_dump()
        })
        self.conn.commit()
        return self.get(id)

    def delete(self, id:int)->int|None:
        data = self.get(id)
        if data is None:
            return None
        self.cur.execute("""
            DELETE FROM shipments
            WHERE id=:id
        """,{
            "id":id
        })
        self.conn.commit()
        return id
    
    def close(self):
        self.conn.close()



#####CREATE TABLE

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS  shipments(
#         id INTEGER,
#         content TEXT,
#         weight REAL,
#         status TEXT
#     )
# """)

#####INSERT DATA
# cursor.execute("""
#     INSERT INTO shipments
#     VALUES (12703,'TV', 12, 'placed')
# """)


#####FETCH DATA
# this will get the reference to first object(cursor),
# cursor.execute("""
#     SELECT * FROM shipments 
# """)

# # this will fetch all the rows
# data = cursor.fetchall()
# # data = cursor.fetchmany(2)
# print(data)


# #####UPDATE DATA
# cursor.execute("""
#     UPDATE shipments SET status = 'in_transit'
#     WHERE id=12701
# """)

# connection.commit()

# # close the connection when we are done
# connection.close()