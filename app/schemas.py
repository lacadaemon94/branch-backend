# app/schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProductoBase(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio_unitario: float

class ProductoRequest(BaseModel):
    nombre: str
    descripcion: str
    precio_unitario: float

class ProductoId(BaseModel):
    id: int

class ProductoCreate(ProductoRequest):
    pass

class ProductoDelete(ProductoId):
    pass

class Producto(ProductoBase):
    class Config:
        orm_mode = True

class EmpleadoBase(BaseModel):
    id: str
    nombre: str
    rol_id: int

class SucursalEmpleadoBase(BaseModel):
    empleado: EmpleadoBase

class SucursalDetail(BaseModel):
    id: int
    nombre: str
    descripcion: str
    empleados: List[SucursalEmpleadoBase]

class SucursalModel(SucursalDetail):
    pass

class OrdenBase(BaseModel):
    sucursal_id: int
    producto_id: int
    fechaRealizada: date
    cantidad: int
    estado: str

class OrdenResponse(BaseModel):
    id: int
    sucursal_id: int
    producto_id: int
    fechaRealizada: date
    cantidad: int
    estado: str

class OrdenList(BaseModel):
    id: int
    sucursal_id: int
    producto_id: int
    fechaRealizada: date
    cantidad: int
    estado: str
    sucursal: Optional[SucursalDetail]

class OrdenListResponse(BaseModel):
    ordenes: List[OrdenList]

class OrdenCreate(OrdenBase):
    pass

class OrdenBaseResponse(OrdenResponse):
    pass

class Orden(OrdenBase, OrdenList):
    class Config:
        orm_mode = True

class TransferenciaBase(BaseModel):
    id: int
    sucursal_id: int
    producto_id: int
    inventario_origen: int
    inventario_destino: int
    cantidad: int
    fechaRealizada: date

class TransferenciaRequest(BaseModel):
    sucursal_id: int
    producto_id: int
    inventario_origen: int
    inventario_destino: int
    cantidad: int
    fechaRealizada: date

class TransferenciaCreate(TransferenciaRequest):
    pass

class Transferencia(TransferenciaBase):
    class Config:
        orm_mode: True

class TransferenciaResponse(BaseModel):
    sucursal_id: int
    producto_id: int
    inventario_origen: int
    cantidad_origen: int
    inventario_destino: int
    cantidad_destino: int

class InventarioBase(BaseModel):
    id: int
    sucursal_id: int
    tipo_id: int
    producto_id: int
    cantidad: int

class InventarioModel(InventarioBase):
    pass

class Inventario(InventarioBase):
    class Config:
        orm_mode = True

class InventarioListRequest(BaseModel):
    sucursal_id: int