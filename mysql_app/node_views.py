from typing import List
from fastapi import APIRouter, Depends, HTTPException, Form
from mysql_app import crud, schemas
from mysql_app.connectdb import get_connection

router = APIRouter(prefix='/node', tags=["node"])

@router.post("", response_model=schemas.Node)
async def create_node(name: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    response = crud.post_nodes(cursor, connection, schemas.NodeCreate(name=name))
    response2 = crud.post_loc(cursor,connection,schemas.LocCreate(node_name=name,longitude="0",latitude="0"))
    cursor.close()
    connection.close()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.get("/", response_model=List[schemas.Node])
async def get_nodes(skip: int = 0, limit: int = 10):
    connection = get_connection()
    cursor = connection.cursor()
    nodes = crud.get_nodes(cursor, skip=skip, limit=limit)
    cursor.close()
    connection.close()
    if "error" in nodes:
        raise HTTPException(status_code=400, detail=nodes["error"])
    return nodes

@router.get("/{node_id}", response_model=schemas.Node)
async def get_node(node_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    db_node = crud.get_node(cursor, node_id=node_id)
    cursor.close()
    connection.close()
    if "error" in db_node:
        raise HTTPException(status_code=404, detail=db_node["error"])
    return db_node

@router.put("/{node_id}", response_model=schemas.Node)
async def update_node(node_id: int, name: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    db_node = crud.get_node(cursor, node_id=node_id)
    if "error" in db_node:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail=db_node["error"])
    response = crud.update_node(cursor, connection, node_id=node_id, node=schemas.NodeCreate(name=name))
    cursor.close()
    connection.close()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.delete("/{node_id}", response_model=dict)
async def delete_node(node_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    db_node = crud.get_node(cursor, node_id=node_id)
    if "error" in db_node:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail=db_node["error"])
    response = crud.delete_node(cursor, connection, node_id=node_id)
    cursor.close()
    connection.close()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
