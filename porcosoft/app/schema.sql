-- =======================================
-- Tabla: Animales
-- Descripción: Almacén central para cada animal en la granja.
-- Contiene datos de identificación, estado y a qué lote pertenece.
-- =======================================
-- =======================================
-- Tabla: Animales (Versión Mejorada)
-- =======================================
CREATE TABLE Animales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    arete_id TEXT UNIQUE NOT NULL,
    nombre TEXT,                        -- NUEVO: Nombre o alias del animal
    raza TEXT,
    color TEXT,                         -- NUEVO: Color o características físicas
    sexo TEXT NOT NULL CHECK(sexo IN ('Macho', 'Hembra')),
    fecha_nacimiento DATE,
    peso_nacimiento_kg REAL,            -- NUEVO: Peso al nacer en kg
    fecha_destete DATE,                 -- NUEVO: Fecha de destete
    peso_destete_kg REAL,               -- NUEVO: Peso al momento del destete en kg
    origen TEXT DEFAULT 'Nacido en granja', -- NUEVO: 'Nacido en granja' o 'Comprado'
    lote_id INTEGER,
    es_reproductor BOOLEAN DEFAULT 0,
    estado TEXT NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Vendido', 'Muerto')),
    fecha_salida DATE,                  -- NUEVO: Fecha de venta o muerte del animal
    notas TEXT,
    FOREIGN KEY (lote_id) REFERENCES Lotes(id)
);

-- =======================================
-- Tabla: Lotes
-- Descripción: Agrupa animales para gestión de engorde.
-- =======================================
CREATE TABLE Lotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_lote TEXT UNIQUE NOT NULL,
    fecha_creacion DATE DEFAULT (CURRENT_DATE),
    descripcion TEXT
);

-- =======================================
-- Tabla: Eventos_Reproductivos
-- Descripción: Registra todos los eventos clave del ciclo reproductivo
-- de un animal marcado como 'es_reproductor = 1'.
-- =======================================
CREATE TABLE Eventos_Reproductivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER NOT NULL,
    tipo_evento TEXT NOT NULL CHECK(tipo_evento IN ('Celo', 'Servicio', 'Parto', 'Destete')),
    fecha_evento DATE NOT NULL,
    resultado TEXT, -- Ej: 'Positivo', '12 nacidos vivos', 'Destetados 11'
    notas TEXT,
    FOREIGN KEY (animal_id) REFERENCES Animales(id)
);

-- =======================================
-- Tabla: Sanidad
-- Descripción: Registra todos los tratamientos y vacunas aplicadas.
-- =======================================
CREATE TABLE Sanidad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER, -- Puede ser nulo si se aplica a un lote entero
    lote_id INTEGER, -- Puede ser nulo si se aplica a un solo animal
    fecha_tratamiento DATE NOT NULL,
    producto TEXT NOT NULL,
    tipo_tratamiento TEXT, -- Ej: 'Vacuna', 'Desparasitante'
    dosis TEXT,
    periodo_resguardo_dias INTEGER DEFAULT 0,
    notas TEXT,
    FOREIGN KEY (animal_id) REFERENCES Animales(id),
    FOREIGN KEY (lote_id) REFERENCES Lotes(id)
);

-- =======================================
-- Tabla: Alimentacion
-- Descripción: Registra el consumo de alimento por lote.
-- =======================================
CREATE TABLE Alimentacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lote_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    tipo_alimento TEXT NOT NULL,
    cantidad_kg REAL NOT NULL,
    costo_total REAL,
    FOREIGN KEY (lote_id) REFERENCES Lotes(id)
);

-- =======================================
-- Tabla: Reportes
-- Descripción: Almacena metadatos sobre reportes generados.
-- NO almacena el archivo, solo la RUTA donde se guarda.
-- =======================================
CREATE TABLE Reportes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_reporte TEXT NOT NULL,
    fecha_generacion DATETIME DEFAULT (CURRENT_TIMESTAMP),
    parametros TEXT, -- Ej: 'Lote 5, Rango de fechas...'
    ruta_archivo TEXT NOT NULL -- Ruta al archivo PDF/Excel guardado en el servidor
);

-- =======================================
-- Tabla: Configuraciones
-- Descripción: Guarda configuraciones generales del sistema.
-- =======================================
CREATE TABLE Configuraciones (
    clave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);