from typing import List
from fastapi import APIRouter, HTTPException, Form
from mysql_app import crud, schemas
from mysql_app.connectdb import get_connection

router = APIRouter(prefix='/mobile', tags=["mobile"])

@router.post("/bind", response_model=schemas.Bind)
async def create_bind(node_name: str = Form(...), vin_name: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Create bind
        node = crud.get_node_by_name(cursor=cursor,node_name=node_name)
        if "error" in node:
            raise HTTPException(status_code=400, detail=["error in no found node"])

        vin = crud.get_vin_by_name(cursor=cursor, vin_name=vin_name)
        if "error" in vin:
            raise HTTPException(status_code=400, detail=["error in vin"])
        elif "name" in vin:
            raise HTTPException(status_code=400, detail=[f"name found: {vin_name}"])

        checkInBindoFnode = crud.get_bind_of_node_by_name(cursor=cursor,node_name=node_name)
        if "error" in checkInBindoFnode:
            raise HTTPException(status_code=400, detail=["error in vin"])
        elif "name" in checkInBindoFnode:
            raise HTTPException(status_code=400, detail=[f"node found in bind"])

        # vin create
        create_vin = crud.post_vin(cursor=cursor, connection=connection, vin=schemas.VinCreate(name=vin_name))
        if "error" in create_vin:
            raise HTTPException(status_code=400, detail=cursor["error"])

        response = crud.post_bind(cursor, connection, schemas.BindCreate(node_name=node_name, vin_name=vin_name))
        if "error" in response:
            crud.delete_vin(cursor=cursor,connection=connection,vin_id=create_vin["vin_id"])
            raise HTTPException(status_code=400, detail=response["error"])
        return response
    finally:
        cursor.close()
        connection.close()

@router.get("/loc/{node_name}", response_model=dict)
async def get_location_by_name(node_name: str):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        response = crud.get_loc_by_name(cursor, node_name)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        return response
    finally:
        cursor.close()
        connection.close()

@router.delete("/del/{vin_name}", response_model=dict)
async def delete_vin(vin_name: str):
    connection = get_connection()
    cursor = connection.cursor()
    response = crud.delete_vin_by_name(cursor=cursor,connection=connection,vin_name=vin_name)
    if "error" in response:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail=response["error"])
    return response


