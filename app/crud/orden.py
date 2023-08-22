# app/crud/orden.py

from sqlalchemy.orm import Session
from db.models.models import Orden as SQLOrden
from db.models.models import Sucursal as SQLSucursal
from db.models.models import Empleado as SQLEmpleado
from db.models.models import SucursalEmpleado as SQLSucursalEmpleado

def create_orden(db: Session, orden: SQLOrden):
    # Check if an entry with the same producto_id, sucursal_id already exists
    existing_orden = db.query(SQLOrden).filter(
        SQLOrden.producto_id == orden.producto_id,
        SQLOrden.sucursal_id == orden.sucursal_id
    ).first()

    if existing_orden:
        # If an entry exists, update the cantidad
        existing_orden.cantidad += orden.cantidad
        db.commit()
        return existing_orden
    else:
        # If no entry exists, insert a new one
        db_orden = SQLOrden(**orden.dict())
        db.add(db_orden)
        db.commit()
        db.refresh(db_orden)
        return db_orden

def get_all_ordenes_with_sucursal_details(db: Session):
    ordenes = db.query(SQLOrden).all()
    orden_list = []
    for orden in ordenes:
        sucursal = db.query(SQLSucursal).filter_by(id=orden.sucursal_id).first()
        
        # Fetch all SucursalEmpleado entries for the given sucursal_id
        sucursal_empleados = db.query(SQLSucursalEmpleado).filter_by(sucursal_id=sucursal.id).all()

        # For each SucursalEmpleado entry, fetch the corresponding Empleado details
        empleados = []
        for se in sucursal_empleados:
            empleado = db.query(SQLEmpleado).filter_by(id=se.empleado_id).first()
            if empleado:
                empleados.append({
                    "empleado": {
                        "id": empleado.id,
                        "nombre": empleado.nombre,
                        "rol_id": empleado.rol_id
                    }
                })


        # Construct the response object
        result = {
            "id": orden.id,
            "sucursal_id": orden.sucursal_id,
            "producto_id": orden.producto_id,
            "fechaRealizada": orden.fechaRealizada,
            "cantidad": orden.cantidad,
            "estado": orden.estado,
            "sucursal": {
                "id": sucursal.id,
                "nombre": sucursal.nombre,
                "descripcion": sucursal.descripcion,
                "empleados": empleados
            }
        }
        orden_list.append(result)
    return orden_list
