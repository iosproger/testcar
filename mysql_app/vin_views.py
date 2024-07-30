from typing import List
from fastapi import APIRouter, Depends, HTTPException, Form
from mysql_app import crud, schemas
from mysql_app.connectdb import get_connection

router = APIRouter(prefix='/vin', tags=["vin"])

@router.post("", response_model=schemas.Vin)
async def create_vin(name: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    response = crud.post_vin(cursor, connection, schemas.VinCreate(name=name))
    cursor.close()
    connection.close()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.get("/", response_model=List[schemas.Vin])
async def get_vins(skip: int = 0, limit: int = 10):
    connection = get_connection()
    cursor = connection.cursor()
    vins = crud.get_vins(cursor, skip=skip, limit=limit)
    cursor.close()
    connection.close()
    if "error" in vins:
        raise HTTPException(status_code=400, detail=vins["error"])
    return vins

@router.get("/{vin_id}", response_model=schemas.Vin)
async def get_vin(vin_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    db_vin = crud.get_vin(cursor, vin_id=vin_id)
    cursor.close()
    connection.close()
    if "error" in db_vin:
        raise HTTPException(status_code=404, detail=db_vin["error"])
    return db_vin

@router.put("/{vin_id}", response_model=schemas.Vin)
async def update_vin(vin_id: int, name: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    db_vin = crud.get_vin(cursor, vin_id=vin_id)
    if "error" in db_vin:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail=db_vin["error"])
    response = crud.update_vin(cursor, connection, vin_id=vin_id, vin=schemas.VinCreate(name=name))
    cursor.close()
    connection.close()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.delete("/{vin_id}", response_model=dict)
async def delete_vin(vin_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    db_vin = crud.get_vin(cursor, vin_id=vin_id)
    if "error" in db_vin:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail=db_vin["error"])
    response = crud.delete_vin(cursor, connection, vin_id=vin_id)
    cursor.close()
    connection.close()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
