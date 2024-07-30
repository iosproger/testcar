from fastapi import APIRouter, Form,HTTPException
from typing import List
from mysql_app import schemas,crud
from mysql_app.connectdb import get_connection

router = APIRouter(prefix='/loc', tags=["location"])

@router.post("", response_model=schemas.Location)
async def create_loc(node_name: str = Form(...), latitude: str = Form(...), longitude: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        response = crud.post_loc(cursor, connection, schemas.LocCreate(node_name=node_name, latitude=latitude, longitude=longitude))
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        return response
    finally:
        cursor.close()
        connection.close()

@router.put("/n/{loc_name}", response_model=dict)
async def update_loc(loc_name: str, latitude: str = Form(...), longitude: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    response = crud.update_loc_by_name(cursor, connection,  loc=schemas.LocCreate(node_name=loc_name, latitude=latitude, longitude=longitude))
    cursor.close()
    connection.close()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@router.put("/{loc_id}", response_model=schemas.Location)
async def update_loc(loc_id: int, latitude: str = Form(...), longitude: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    db_loc = crud.get_loc(cursor, loc_id=loc_id)
    if "error" in db_loc:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail=db_loc["error"])
    cursor = connection.cursor()
    response = crud.update_loc(cursor, connection, loc_id=loc_id, loc=schemas.LocCreate(node_name=db_loc["node_name"], latitude=latitude, longitude=longitude))
    cursor.close()
    connection.close()
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response


@router.get("/", response_model=List[schemas.Location])
async def get_binds(skip: int = 0, limit: int = 10):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        binds = crud.get_locs(cursor, skip=skip, limit=limit)
        if "error" in binds:
            raise HTTPException(status_code=400, detail=binds["error"])
        return binds
    finally:
        cursor.close()
        connection.close()

@router.get("/{loc_id}", response_model=schemas.Location)
async def get_bind(loc_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        db_bind = crud.get_loc(cursor,loc_id=loc_id)
        if "error" in db_bind:
            raise HTTPException(status_code=404, detail=db_bind["error"])
        return db_bind
    finally:
        cursor.close()
        connection.close()

@router.delete("/{loc_id}", response_model=dict)
async def delete_bind(loc_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        db_bind = crud.get_loc(cursor, loc_id=loc_id)
        if "error" in db_bind:
            raise HTTPException(status_code=404, detail=db_bind["error"])

        cursor = connection.cursor()
        response = crud.delete_loc(cursor, connection, loc_id=loc_id)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        return response
    finally:
        cursor.close()
        connection.close()