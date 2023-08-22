# Guía de Configuración y Ejecución para Branch Backend
## Prerrequisitos
- Docker y Docker Compose instalados.
- Python.
- pip.
- fastapi
- sqlalchemy

## Configuración
1. Clonar el Repositorio:
```bash
git clone https://github.com/lacadaemon94/branch-backend
cd branch-backend
```
2. Instalar Dependencias
```bash
pip install -r requirements.txt
```
3. Configurar `Session.py` e `init_db.py`
```python
DATABASE_URL = "postgresql+psycopg2://postgres:[TU_PASSWORD_DE_SUPABASE(BD)]@db.[TU_URL_DE_SUPABASE)]:6543/postgres"  # Replace with your actual database URL
```
3. Activar Environment de Python
```bash
source venv/bin/activate
python -m venv venv
```
4. Aplicar la Migracion:
```bash
python init_db.py
deactivate
``` 
7. Copiar SQL Scripts en folder `sql_scripts` y correrlos en el SQL Editor de Supabase
```sql
-- Trigger Function for Orden Table on every INSERT to aggreagate cantidad on existing orden with status ingresado
CREATE OR REPLACE FUNCTION handle_orden_insert()
RETURNS TRIGGER AS $$
BEGIN
  -- Check if an entry with the same producto_id, sucursal_id already exists and status is 'ingresado'
  IF EXISTS (SELECT 1 FROM orden WHERE producto_id = NEW.producto_id AND sucursal_id = NEW.sucursal_id AND estado = NEW.estado) THEN
      -- Aggregate the cantidad
      UPDATE orden
      SET cantidad = cantidad + NEW.cantidad
      WHERE producto_id = NEW.producto_id AND sucursal_id = NEW.sucursal_id;
      
      -- Prevent the original INSERT from proceeding
      RETURN NULL;
  ELSE
      -- Allow the original INSERT to proceed
      RETURN NEW;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_aggregate_orden_on_insert
BEFORE INSERT ON orden
FOR EACH ROW
EXECUTE FUNCTION handle_orden_insert();

-- Trigger Function for Transferencia Table on every INSERT to INSERT UPDATE OR DELETE ON inventario based on conditions met
CREATE OR REPLACE FUNCTION handle_transferencia_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Deduct the cantidad from the inventario_origen
    UPDATE inventario
    SET cantidad = cantidad - NEW.cantidad
    WHERE producto_id = NEW.producto_id AND sucursal_id = NEW.sucursal_id AND tipo_id = NEW.inventario_origen;

    -- Delete the entry if the quantity reaches 0
    DELETE FROM inventario
    WHERE producto_id = NEW.producto_id AND sucursal_id = NEW.sucursal_id AND tipo_id = NEW.inventario_origen AND cantidad <= 0;

    -- Check if an entry with the same producto_id, sucursal_id, and inventario_destino already exists
    IF EXISTS (SELECT 1 FROM inventario WHERE producto_id = NEW.producto_id AND sucursal_id = NEW.sucursal_id AND tipo_id = NEW.inventario_destino) THEN
        -- Aggregate the cantidad
        UPDATE inventario
        SET cantidad = cantidad + NEW.cantidad
        WHERE producto_id = NEW.producto_id AND sucursal_id = NEW.sucursal_id AND tipo_id = NEW.inventario_destino;
    ELSE
        -- Insert a new entry
        INSERT INTO inventario (producto_id, sucursal_id, tipo_id, cantidad)
        VALUES (NEW.producto_id, NEW.sucursal_id, NEW.inventario_destino, NEW.cantidad);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_handle_transferencia_insert
AFTER INSERT ON transferencia
FOR EACH ROW
EXECUTE FUNCTION handle_transferencia_insert();

-- Trigger Function for Inventario Table on every INSERT to aggregate if existing entry with same sucursal, tipo and producto
CREATE OR REPLACE FUNCTION aggregate_inventario_on_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if an entry with the same sucursal_id, tipo_id, and producto_id already exists
    IF EXISTS (SELECT 1 FROM inventario WHERE sucursal_id = NEW.sucursal_id AND tipo_id = NEW.tipo_id AND producto_id = NEW.producto_id) THEN
        -- Aggregate the cantidad
        UPDATE inventario
        SET cantidad = cantidad + NEW.cantidad
        WHERE sucursal_id = NEW.sucursal_id AND tipo_id = NEW.tipo_id AND producto_id = NEW.producto_id;
        
        -- Prevent the original insert since we've updated the existing row
        RETURN NULL;
    ELSE
        -- Allow the insert to proceed as normal
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_aggregate_inventario_on_insert
BEFORE INSERT ON inventario
FOR EACH ROW
EXECUTE FUNCTION aggregate_inventario_on_insert();

-- Inserting data for Tipo
INSERT INTO tipo (id, tipo) VALUES
(1, 'bodega'),
(2, 'venta'),
(3, 'devolucion');

-- Inserting data for Rol
INSERT INTO rol (id, tipo) VALUES
(1, 'regente'),
(2, 'dependiente');

-- Inerting data for producto
INSERT INTO producto (nombre, descripcion, precio_unitario) VALUES
('Benadryl', 'Allergy relief.', 8.99),
('Aleve', 'Pain reliever and fever reducer.', 12.99),
('DayQuil', 'Cough, cold, and flu relief.', 10.99),
('Prescription Strength Tylenol', 'Pain reliever and fever reducer.', 8.99),
('Prescription Strength Zyrtec', 'Allergy relief.', 5.99),
('Tylenol', 'Pain reliever and fever reducer.', 7.99),
('Advil', 'Pain reliever and fever reducer.', 8.99);

-- Inserting data for sucursal
INSERT INTO sucursal (nombre, descripcion) VALUES
('Walgreens', 'A large drugstore chain with a wide selection of products, including prescription drugs, over-the-counter medications, health and beauty products, and food and snacks.'),
('CVS Pharmacy', 'Another large drugstore chain with a similar selection of products to Walgreens.'),
('Rite Aid', 'A smaller drugstore chain with a more limited selection of products.'),
('Target Strength Tylenol', 'A department store that also sells a variety of drugstore products.'),
('Walmart Strength Zyrtec', 'Another department store that also sells a variety of drugstore products.');

-- Inserting data for Empleado
INSERT INTO empleado (id, nombre, rol_id) VALUES
('12345678a', 'Jose Perez', 1),
('cc1234567d', 'David Guzman', 1),
('dd1234567e', 'Lorena Morena', 1),
('f1234567g', 'Lisa Doe', 1),
('h1234567i', 'Daniel Martinez', 1),
('b1234567c', 'Elizabeth Williams', 2),
('z1234567a', 'David Davis', 2),
('x1234567y', 'Charles Thompson', 2),
('v1234567w', 'Sarah Martin', 2),
('t1234567u', 'William Johnson', 2),
('r1234567s', 'Emily Anderson', 2),
('p1234567q', 'James White', 2),
('n1234567o', 'Mary Green', 2),
('l1234567m', 'Susan Jones', 2),
('ee1234567f', 'Peter Smith', 2);

-- Inserting data for sucursal_empleado
INSERT INTO sucursal_empleado (sucursal_id, empleado_id) VALUES
('1', '12345678a'),
('1', 'b1234567c'),
('1', 'z1234567a'),
('2', 'cc1234567d'),
('2', 'x1234567y'),
('3', 'dd1234567e'),
('3', 'v1234567w'),
('4', 'f1234567g'),
('4', 't1234567u'),
('4', 'r1234567s'),
('5', 'h1234567i'),
('5', 'p1234567q'),
('5', 'n1234567o'),
('1', 'l1234567m'),
('1', 'ee1234567f');

-- Inserting data for inventario
INSERT INTO inventario (sucursal_id, tipo_id, producto_id, cantidad) VALUES
('1', 1, '1', 5),
('1', 1, '2', 5),
('1', 1, '3', 5),
('1', 2, '2', 5),
('1', 2, '4', 5),
('1', 2, '5', 5),
('1', 3, '1', 5),
('1', 3, '6', 5),
('1', 3, '5', 5),
('2', 1, '1', 5),
('2', 1, '6', 5),
('2', 1, '3', 5),
('2', 2, '2', 5),
('2', 2, '4', 5),
('2', 2, '5', 5),
('2', 3, '1', 5),
('2', 3, '6', 5),
('2', 3, '5', 5),
('3', 1, '1', 5),
('3', 1, '6', 5),
('3', 1, '3', 5),
('3', 2, '2', 5),
('3', 2, '4', 5),
('3', 2, '5', 5),
('3', 3, '1', 5),
('3', 3, '6', 5),
('3', 3, '5', 5),
('4', 1, '1', 5),
('4', 1, '6', 5),
('4', 1, '3', 5),
('4', 2, '2', 5),
('4', 2, '4', 5),
('4', 2, '5', 5),
('4', 3, '1', 5),
('4', 3, '6', 5),
('4', 3, '5', 5),
('5', 1, '1', 5),
('5', 1, '6', 5),
('5', 1, '3', 5),
('5', 2, '2', 5),
('5', 2, '4', 5),
('5', 2, '5', 5),
('5', 3, '1', 5),
('5', 3, '6', 5),
('5', 3, '5', 5);


``` 

8. Docker Compose (servida en localhost:8000)
```bash
docker-compose up
```

## Diagrama E-R
![ER Screenshot](https://iizvajwgbwshetzxkmni.supabase.co/storage/v1/object/public/stuff/Screenshot%202023-08-21%20225836.png)


Las entidades principales son `Empleado`, `Sucursal`, `Producto`, `Inventario`, `Orden` y `Transferencia`.
## Puntos clave del esquema de la base de datos:
- **Empleado**: Representa a los trabajadores del sistema, asociados a un rol específico.
- **Sucursal**: Define las diferentes ubicaciones o tiendas. Los empleados están asignados a sucursales específicas.
- **Producto**: Detalla los artículos disponibles para la venta o transferencia.
- **Inventario**: Muestra la cantidad de productos en una sucursal específica y su tipo.
- **Orden**: Representa las ventas o pedidos realizados en una sucursal, detallando el producto y la cantidad.
- **Transferencia**: Gestiona el movimiento de productos entre sucursales o tipos de inventario.

**Resumen de Triggers y Funciones:**
1. **Función `handle_orden_insert`**:
   - **Objetivo**: Agregar la cantidad a una orden existente con el estado `ingresado` en lugar de insertar una nueva entrada.
   - **Funcionalidad**:
     - Si ya existe una orden con el mismo `producto_id`, `sucursal_id` y estado `ingresado` se suma la cantidad a la entrada existente.
     - Si no existe tal entrada, se permite la inserción original.

2. **Función `handle_transferencia_insert`**:
   - **Objetivo**: Gestionar las inserciones en la tabla `transferencia` y actualizar la tabla `inventario` en consecuencia.
   - **Funcionalidad**:
     - Deduce la cantidad del `inventario_origen`.
     - Si la cantidad en el `inventario_origen` llega a 0, se elimina esa entrada.
     - Si ya existe una entrada en el `inventario_destino`, se suma la cantidad.
     - Si no existe tal entrada, se inserta una nueva con la cantidad transferida.

3. **Función `aggregate_inventario_on_insert`**:
   - **Objetivo**: Agregar la cantidad a una entrada existente en la tabla `inventario` en lugar de insertar una nueva.
   - **Funcionalidad**:
     - Si ya existe una entrada con el mismo `sucursal_id`, `tipo_id` y `producto_id`, se suma la cantidad a la entrada existente.
     - Si no existe tal entrada, se permite la inserción original.s.

# Documentación API

## Tabla de Contenidos

- [CREAR_ORDEN]
- [LISTAR_ORDENES]
- [BORRAR_PRODUCTO]
- [OBTENER_PRODUCTO]
- [LISTAR_INVENTARIO]
- [TRANSFERIR_PRODUCTO_INVENTARIO]
- [LISTAR_INVENTARIO]

---

## CREAR_ORDEN

**URL**: `/orden`

**Method**: `POST`

**Description**: Crear orden de re-stock por sucursal.

### Request

**Body**:

```json
{
  "sucursal_id": 2,
  "producto_id": 2,
  "fechaRealizada": "2023-08-19",
  "cantidad": 10,
  "estado": "ingresado"
}
```

## LISTAR_ORDENES

**URL**: `/orden/list`

**Method**: `GET`

**Description**: Listar todas las ordenes.

### Request


## OBTENER_PRODUCTO

**URL**: `/productos/{id}`

**Method**: `GET`

**Description**: Obtener producto a traves de parametro `id`.

## LISTAR_PRODUCTOS

**URL**: `/productos/show`

**Method**: `GET`

**Description**: Listar todos los productos.

## LISTAR_INVENTARIO

**URL**: `/inventario/list`

**Method**: `GET`

**Description**: Listar todo el inventario.

## TRANSFERIR_PRODUCTO_INVENTARIO

**URL**: `/inventario/transfer`

**Method**: `POST`

**Description**: Transferir producto entre tipo de inventarios.

### Request

**Body**:

```json
{
  "sucursal_id": 1,
  "producto_id": 1,
  "inventario_origen": "3",
  "inventario_destino": "1",
  "cantidad": 5,
  "fechaRealizada": "2023-08-20"
}

```

## LISTAR_SUCURSALES

**URL**: `/sucursal/list`

**Method**: `GET`

**Description**: Listar todas las sucursales.

---
