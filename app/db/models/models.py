from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Rol(Base):
    __tablename__ = "rol"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)

class Tipo(Base):
    __tablename__ = "tipo"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, index=True)

class Empleado(Base):
    __tablename__ = "empleado"

    id = Column(String, primary_key=True, index=True)  # dui/jvpqf
    nombre = Column(String, index=True)
    rol_id = Column(Integer, ForeignKey('rol.id'))
    rol = relationship("Rol")

class Sucursal(Base):
    __tablename__ = "sucursal"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)

class Producto(Base):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)
    precio_unitario = Column(Float)

class SucursalEmpleado(Base):
    __tablename__ = "sucursal_empleado"

    sucursal_id = Column(Integer, ForeignKey('sucursal.id'), primary_key=True)
    empleado_id = Column(String, ForeignKey('empleado.id'), primary_key=True)

class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey('sucursal.id'))
    tipo_id = Column(Integer, ForeignKey('tipo.id'))
    producto_id = Column(Integer, ForeignKey('producto.id'))
    cantidad = Column(Integer)

class Orden(Base):
    __tablename__ = "orden"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey('sucursal.id'), primary_key=True)
    producto_id = Column(Integer, ForeignKey('producto.id'), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    fechaRealizada = Column(Date)
    estado = Column(String)

class Transferencia(Base):
    __tablename__ = "transferencia"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey('sucursal.id'), primary_key=True)
    producto_id = Column(Integer, ForeignKey('producto.id'), primary_key=True)
    inventario_origen = Column(Integer, ForeignKey('tipo.id'), primary_key=True)
    inventario_destino = Column(Integer, ForeignKey('tipo.id'), primary_key=True)
    cantidad = Column(Integer)
    fechaRealizada = Column(Date)