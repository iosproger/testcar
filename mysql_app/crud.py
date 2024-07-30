from mysql.connector.cursor import MySQLCursor
from . import schemas

# mobile
def delete_vin_by_name(cursor: MySQLCursor, connection, vin_name: str):
    query = "DELETE FROM vins WHERE name = %s"
    values = (vin_name,)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": f"Deleted vin with name {vin_name}"}
    except Exception as e:
        return {"error": str(e)}

def get_loc_by_name(cursor: MySQLCursor, node_name: str):
    query = "SELECT * FROM loc WHERE node_name = %s"
    values = (node_name,)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return {"node_name": result[1], "latitude":result[2], "longitude":result[3]}
        else:
            return {"error": f"No node found with name {node_name}"}
    except Exception as e:
        return {"error": str(e)}
def get_node_by_name(cursor: MySQLCursor, node_name: str):
    query = "SELECT * FROM nodes WHERE name = %s"
    values = (node_name,)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return result[1]
        else:
            return {"error": f"No node found with ID {node_name}"}
    except Exception as e:
        return {"error": str(e)}

def get_vin_by_name(cursor: MySQLCursor, vin_name: str):
    query = "SELECT * FROM vins WHERE name = %s"
    values = (vin_name,)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return {"name": f"name found: {vin_name}"}
        else:
            return {"no": f"No node found with ID {vin_name}"}
    except Exception as e:
        return {"error": str(e)}

def get_bind_of_node_by_name(cursor: MySQLCursor, node_name: str):
    query = "SELECT * FROM binds WHERE node_name = %s"
    values = (node_name,)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return {"name": f"node found in bind"}
        else:
            return {"noname": f"No node found with ID {node_name}"}
    except Exception as e:
        return {"error": str(e)}
# Node
def get_node(cursor: MySQLCursor, node_id: int):
    query = "SELECT * FROM nodes WHERE node_id = %s"
    values = (node_id,)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return {"node_id": result[0], "name": result[1]}
        else:
            return {"error": f"No node found with ID {node_id}"}
    except Exception as e:
        return {"error": str(e)}

def get_nodes(cursor: MySQLCursor, skip: int = 0, limit: int = 100):
    query = "SELECT * FROM nodes LIMIT %s OFFSET %s;"
    values = (limit, skip)
    try:
        cursor.execute(query, values)
        results = cursor.fetchall()
        ret = [{"node_id": row[0], "name": row[1]} for row in results]
        return ret
    except Exception as e:
        return {"error": str(e)}

def post_nodes(cursor: MySQLCursor, connection, node: schemas.NodeCreate):
    query = "INSERT INTO nodes (name) VALUES (%s)"
    values = (node.name,)
    try:
        cursor.execute(query, values)
        connection.commit()
        node_id = cursor.lastrowid
        return {"node_id": node_id, "name": node.name}
    except Exception as e:
        return {"error": str(e)}

def update_node(cursor: MySQLCursor, connection, node_id: int, node: schemas.NodeCreate):
    query = "UPDATE nodes SET name = %s WHERE node_id = %s"
    values = (node.name, node_id)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"node_id": node_id, "name": node.name}
    except Exception as e:
        return {"error": str(e)}

def delete_node(cursor: MySQLCursor, connection, node_id: int):
    query = "DELETE FROM nodes WHERE node_id = %s"
    values = (node_id,)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": f"Deleted node with ID {node_id}"}
    except Exception as e:
        return {"error": str(e)}

# Vin
def get_vin(cursor: MySQLCursor, vin_id: int):
    query = "SELECT * FROM vins WHERE vin_id = %s"
    values = (vin_id,)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return {"vin_id": result[0], "name": result[1]}
        else:
            return {"error": f"No vin found with ID {vin_id}"}
    except Exception as e:
        return {"error": str(e)}

def get_vins(cursor: MySQLCursor, skip: int = 0, limit: int = 100):
    query = "SELECT * FROM vins LIMIT %s OFFSET %s;"
    values = (limit, skip)
    try:
        cursor.execute(query, values)
        results = cursor.fetchall()
        ret = [{"vin_id": row[0], "name": row[1]} for row in results]
        return ret
    except Exception as e:
        return {"error": str(e)}

def post_vin(cursor: MySQLCursor, connection, vin: schemas.VinCreate):
    query = "INSERT INTO vins (name) VALUES (%s)"
    values = (vin.name,)
    try:
        cursor.execute(query, values)
        connection.commit()
        vin_id = cursor.lastrowid
        return {"vin_id": vin_id, "name": vin.name}
    except Exception as e:
        return {"error": str(e)}

def update_vin(cursor: MySQLCursor, connection, vin_id: int, vin: schemas.VinCreate):
    query = "UPDATE vins SET name = %s WHERE vin_id = %s"
    values = (vin.name, vin_id)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"vin_id": vin_id, "name": vin.name}
    except Exception as e:
        return {"error": str(e)}

def delete_vin(cursor: MySQLCursor, connection, vin_id: int):
    query = "DELETE FROM vins WHERE vin_id = %s"
    values = (vin_id,)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": f"Deleted vin with ID {vin_id}"}
    except Exception as e:
        return {"error": str(e)}

# bind
def get_bind(cursor: MySQLCursor,bind_id:int):
    query = "SELECT * FROM binds WHERE bind_id = %s"
    values = (bind_id,)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return {"bind_id": result[0], "node_name": result[1], "vin_name":result[2]}
        else:
            return {"error": f"No node found with ID {bind_id}"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()

def get_binds(cursor: MySQLCursor, skip: int = 0, limit: int = 100):
    query = "SELECT * FROM binds LIMIT %s OFFSET %s;"
    values = (limit, skip)
    try:
        cursor.execute(query, values)
        results = cursor.fetchall()
        ret = [{"bind_id": row[0], "node_name": row[1], "vin_name":row[2]} for row in results]
        return ret
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()

def post_bind(cursor: MySQLCursor, connection, bind: schemas.BindCreate):
    query = "INSERT INTO binds (node_name,vin_name) VALUES (%s,%s)"
    values = (bind.node_name,bind.vin_name,)
    try:
        cursor.execute(query, values)
        connection.commit()
        bind_id = cursor.lastrowid
        return {"bind_id": bind_id, "node_name": bind.node_name, "vin_name": bind.vin_name}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()

def delete_bind(cursor: MySQLCursor, connection, bind_id: int):
    query = "DELETE FROM binds WHERE bind_id = %s"
    values = (bind_id,)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": f"Deleted bind with ID {bind_id}"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()

# location
def get_loc(cursor: MySQLCursor,loc_id:int):
    query = "SELECT * FROM loc WHERE loc_id = %s"
    values = (loc_id,)
    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            return {"loc_id": result[0], "node_name": result[1], "latitude":result[2], "longitude":result[3]}
        else:
            return {"error": f"No node found with ID {loc_id}"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()

def get_locs(cursor: MySQLCursor, skip: int = 0, limit: int = 100):
    query = "SELECT * FROM loc LIMIT %s OFFSET %s;"
    values = (limit, skip)
    try:
        cursor.execute(query, values)
        results = cursor.fetchall()
        ret = [{"loc_id": row[0], "node_name": row[1], "latitude":row[2], "longitude":row[3]} for row in results]
        return ret
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()

def post_loc(cursor: MySQLCursor, connection, loc: schemas.LocCreate):
    query = "INSERT INTO loc (node_name, latitude, longitude) VALUES (%s, %s, %s)"
    values = (loc.node_name, loc.latitude, loc.longitude)
    try:
        cursor.execute(query, values)
        connection.commit()
        loc_id = cursor.lastrowid
        return {"loc_id": loc_id, "node_name": loc.node_name, "latitude": loc.latitude, "longitude": loc.longitude}
    except Exception as e:
        return {"error": str(e)}

def update_loc_by_name(cursor: MySQLCursor, connection,loc: schemas.LocCreate):
    query = "UPDATE loc SET latitude = %s, longitude = %s WHERE node_name = %s"
    values = (loc.latitude, loc.longitude, loc.node_name)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"node_name": loc.node_name, "latitude": loc.latitude, "longitude": loc.longitude}
    except Exception as e:
        return {"error": str(e)}

def update_loc(cursor: MySQLCursor, connection, loc_id: int, loc: schemas.LocCreate):
    query = "UPDATE loc SET latitude = %s, longitude = %s WHERE loc_id = %s"
    values = (loc.latitude, loc.longitude, loc_id)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"loc_id": loc_id, "node_name": loc.node_name, "latitude": loc.latitude, "longitude": loc.longitude}
    except Exception as e:
        return {"error": str(e)}


def delete_loc(cursor: MySQLCursor, connection, loc_id: int):
    query = "DELETE FROM loc WHERE loc_id = %s"
    values = (loc_id,)
    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": f"Deleted bind with ID {loc_id}"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()