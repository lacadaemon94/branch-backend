# app/crud/orden.py

from sqlalchemy.orm import Session
from db.models.models import Sucursal as SQLSucursal
from db.models.models import Empleado as SQLEmpleado
from db.models.models import SucursalEmpleado as SQLSucursalEmpleado

def get_all_sucursal_details(db: Session):
    sucursales = db.query(SQLSucursal).all()
    sucursales_list = []
    for sucursal in sucursales:
        sucursal = db.query(SQLSucursal).filter_by(id=sucursal.id).first()
        
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
            "id": sucursal.id,
            "nombre": sucursal.nombre,
            "descripcion": sucursal.descripcion,
            "empleados": empleados
        }
        sucursales_list.append(result)
    return sucursales_list
