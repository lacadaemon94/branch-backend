# app/api/orden.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from crud import sucursal as crud_orden
from schemas import SucursalModel
from typing import List

router = APIRouter()

@router.get("/sucursal/list", response_model=List[SucursalModel])
def listar_sucursales(db: Session = Depends(get_db)):
    # Fetch all sucursal entries and their associated sucursal details
    sucursales = crud_orden.get_all_sucursal_details(db)

    return sucursales