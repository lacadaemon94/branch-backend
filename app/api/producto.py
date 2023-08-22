from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from crud import producto as crud_producto
from db.models.models import Producto, Inventario
from schemas import Producto, ProductoCreate, TransferenciaCreate, TransferenciaResponse, InventarioListRequest, Inventario, ProductoDelete

router = APIRouter()

@router.get("/productos/show", response_model=List[Producto])
def read_productos(db: Session = Depends(get_db)):
    productos = crud_producto.get_productos(db)
    return productos

@router.get("/productos/{producto_id}", response_model=Producto)
def read_producto(producto_id: str, db: Session = Depends(get_db)):
    db_producto = crud_producto.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    return db_producto

@router.post("/productos/add", response_model=Producto)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crud_producto.create_producto(db=db, producto=producto)

@router.post("/productos/delete", response_model=Producto)
def delete_producto(producto: ProductoDelete, db: Session = Depends(get_db)):
    return crud_producto.delete_producto(db=db, producto=producto)

@router.post("/inventario/transfer", response_model=TransferenciaResponse)
def transferir_producto(transferencia: TransferenciaCreate, db: Session = Depends(get_db)):
    # Insert into transferencia table
    new_transferencia = crud_producto.create_transferencia(db=db, transferencia=transferencia)

    # Fetch the updated values from the inventario table for origen and destino
    inventario_origen = crud_producto.get_inventario_by_tipo_producto(db, transferencia.sucursal_id, transferencia.producto_id, transferencia.inventario_origen)
    inventario_destino = crud_producto.get_inventario_by_tipo_producto(db, transferencia.sucursal_id, transferencia.producto_id, transferencia.inventario_destino)

     # Check if inventario_origen is None and set cantidad_origen accordingly
    cantidad_origen = 0 if inventario_origen is None else inventario_origen.cantidad


    # Return the new values
    return TransferenciaResponse(
        sucursal_id=transferencia.sucursal_id,
        producto_id=transferencia.producto_id,
        inventario_origen=transferencia.inventario_origen,
        cantidad_origen=cantidad_origen,
        inventario_destino=transferencia.inventario_destino,
        cantidad_destino=inventario_destino.cantidad
    )

@router.post("/inventario/list", response_model=List[Inventario])
def listar_inventario(request: InventarioListRequest, db: Session = Depends(get_db)):
    # Fetch all inventario entries for the given sucursal_id
    inventarios = crud_producto.get_inventario_by_sucursal(db, request.sucursal_id)

    return inventarios
