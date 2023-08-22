from sqlalchemy.orm import Session
from db.models.models import Producto as SQLProducto
from db.models.models import Transferencia as SQLTransferencia
from db.models.models import Inventario as SQLInventario
from schemas import TransferenciaCreate

def get_producto(db: Session, producto_id: str):
    return db.query(SQLProducto).filter(SQLProducto.id == producto_id).first()

def get_productos(db: Session):
    return db.query(SQLProducto).all()

def create_producto(db: Session, producto: SQLProducto):
    db_producto = SQLProducto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: str):
    db_producto = db.query(SQLProducto).filter(SQLProducto.id == producto_id).first()
    db.delete(db_producto)
    db.commit()
    return {"producto borrado": db_producto}

def create_transferencia(db: Session, transferencia: TransferenciaCreate):
    db_transferencia = SQLTransferencia(**transferencia.dict())
    db.add(db_transferencia)
    db.commit()
    db.refresh(db_transferencia)
    return db_transferencia

def get_inventario_by_tipo_producto(db: Session, sucursal_id, producto_id: str, tipo_id: int):
    return db.query(SQLInventario).filter(SQLInventario.sucursal_id == sucursal_id, SQLInventario.producto_id == producto_id, SQLInventario.tipo_id == tipo_id).first()

def get_inventario_by_sucursal(db: Session, sucursal_id: str):
    return db.query(SQLInventario).filter(SQLInventario.sucursal_id == sucursal_id).all()

# Add update and delete operations similarly
