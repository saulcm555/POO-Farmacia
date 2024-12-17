    CREATE TABLE IF NOT EXISTS users (
        id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        password TEXT NOT NULL,
        telefono TEXT,
        email TEXT,
        direccion TEXT,
        role TEXT NOT NULL DEFAULT 'cliente',
        CHECK (LOWER(role) IN ('admin', 'cliente'))
    );

    CREATE TABLE IF NOT EXISTS medicamentos (
        codigo TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        proveedor TEXT,
        precio REAL,
        fecha_caducidad TEXT,
        stock INTEGER
    );

    CREATE TABLE IF NOT EXISTS ventas (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_empleado INTEGER,
        fecha TEXT,
        total REAL,
        FOREIGN KEY (id_cliente) REFERENCES users (id_persona),
        FOREIGN KEY (id_empleado) REFERENCES users (id_persona)
    );

    CREATE TABLE IF NOT EXISTS detalles_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER,
        codigo_medicamento TEXT,
        cantidad INTEGER,
        FOREIGN KEY (id_venta) REFERENCES ventas (id_venta),
        FOREIGN KEY (codigo_medicamento) REFERENCES medicamentos (codigo)
    );

    CREATE TABLE IF NOT EXISTS facturas (
        id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
        id_venta INTEGER,
        fecha_emision TEXT,
        FOREIGN KEY (id_venta) REFERENCES ventas (id_venta)
    );
