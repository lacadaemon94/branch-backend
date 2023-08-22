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

