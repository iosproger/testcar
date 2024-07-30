from typing import List
from fastapi import APIRouter, HTTPException, Form
from mysql_app import crud, schemas
from mysql_app.connectdb import get_connection

router = APIRouter(prefix='/bind', tags=["bind"])


@router.post("", response_model=schemas.Bind)
async def create_bind(node_name: str = Form(...), vin_name: str = Form(...)):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Create bind
        response = crud.post_bind(cursor, connection, schemas.BindCreate(node_name=node_name, vin_name=vin_name))
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        return response
    finally:
        cursor.close()
        connection.close()


@router.get("/", response_model=List[schemas.Bind])
async def get_binds(skip: int = 0, limit: int = 10):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        binds = crud.get_binds(cursor, skip=skip, limit=limit)
        if "error" in binds:
            raise HTTPException(status_code=400, detail=binds["error"])
        return binds
    finally:
        cursor.close()
        connection.close()


@router.get("/{bind_id}", response_model=schemas.Bind)
async def get_bind(bind_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        db_bind = crud.get_bind(cursor, bind_id=bind_id)
        if "error" in db_bind:
            raise HTTPException(status_code=404, detail=db_bind["error"])
        return db_bind
    finally:
        cursor.close()
        connection.close()


@router.delete("/{bind_id}", response_model=dict)
async def delete_bind(bind_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        db_bind = crud.get_bind(cursor, bind_id=bind_id)
        if "error" in db_bind:
            raise HTTPException(status_code=404, detail=db_bind["error"])

        cursor = connection.cursor()
        response = crud.delete_bind(cursor, connection, bind_id=bind_id)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        return response
    finally:
        cursor.close()
        connection.close()
