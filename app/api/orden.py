# app/api/orden.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from crud import orden as crud_orden
from schemas import OrdenCreate, OrdenBaseResponse, OrdenListResponse

router = APIRouter()

@router.post("/orden", response_model=OrdenBaseResponse)
def orden(orden: OrdenCreate, db: Session = Depends(get_db)):
    return crud_orden.create_orden(db=db, orden=orden)

@router.get("/orden/list", response_model=OrdenListResponse)
def listar_ordenes(db: Session = Depends(get_db)):
    # Fetch all orden entries and their associated sucursal details
    ordenes = crud_orden.get_all_ordenes_with_sucursal_details(db)

    return OrdenListResponse(ordenes=ordenes)