-- Creación de la tabla de notificaciones para JCC Tarjeta Digital
CREATE TABLE IF NOT EXISTS tn_tarjetavirtual_notificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    canal VARCHAR(100) NOT NULL,
    audiencia VARCHAR(100) NOT NULL,
    destinatarios INT NOT NULL,
    fecha VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    creado_por VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Limpiar tabla antes de insertar
TRUNCATE TABLE tn_tarjetavirtual_notificaciones;

-- Insertar los 5 registros de prueba iniciales
INSERT INTO tn_tarjetavirtual_notificaciones (titulo, canal, audiencia, destinatarios, fecha, estado, creado_por, mensaje) VALUES
('Mantenimiento programado', 'Push', 'Todos', 12458, '2025-07-16 07:30 a. m.', 'Entregada', 'María Gómez', 'El sistema estará en mantenimiento el domingo 25 de mayo de 8:00 p. m. a 11:00 p. m. por actualización de servidores.'),
('Nueva versión de la aplicación', 'Alerta estándar', 'Contadores', 9820, '2025-07-15 04:15 p. m.', 'Entregada', 'Sebastian Cuencar', 'Se ha liberado la versión 1.2.0 de la aplicación móvil con mejoras en la visualización de la tarjeta profesional.'),
('Actualización de datos de sociedades', 'Notificación interna', 'Sociedades', 640, '2025-07-15 10:20 a. m.', 'Entregada', 'Laura Martinez', 'Recuerde actualizar los datos de representación legal de su sociedad antes del 31 de julio.'),
('Renovación próxima a vencer', 'Push', 'Contadores', 310, '2025-07-14 08:00 a. m.', 'Programada', 'Sebastian Cuencar', 'Tu tarjeta profesional está próxima a vencer. Inicia el trámite de renovación en línea para evitar sanciones.'),
('Intermitencia del servicio', 'Alerta estándar', 'Todos', 12458, '2025-07-13 03:40 p. m.', 'Fallida', 'Andrés Torres', 'Estamos experimentando problemas técnicos con el nodo de validación de firma digital. Trabajamos en solucionarlo.');

-- 2026-07-31
-- Creación de la tabla de trámites para JCC CRUD
CREATE TABLE IF NOT EXISTS tn_tarjetavirtual_tramites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    costo DECIMAL(12,2) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar algunos trámites de prueba iniciales
INSERT INTO tn_tarjetavirtual_tramites (nombre, tipo, costo, estado, descripcion) VALUES
('Inscripción de Tarjeta Profesional - Contador', 'Contador Público', 375000.00, 'Activo', 'Trámite requerido para los graduados de Contaduría Pública que deseen obtener su tarjeta profesional por primera vez.'),
('Inscripción de Registro - Sociedad', 'Sociedad', 920000.00, 'Activo', 'Trámite de registro y habilitación legal para sociedades prestadoras de servicios contables en Colombia.'),
('Certificado de Vigencia y Antecedentes Disciplinarios', 'Contador Público', 45000.00, 'Activo', 'Expedición del certificado oficial que valida la vigencia de la tarjeta profesional y reporta si existen sanciones disciplinarias activas.');

-- 2026-08-03
-- Creación de la tabla de tarjetas virtuales para JCC
CREATE TABLE IF NOT EXISTS tn_tarjetavirtual_tarjetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_tarjeta VARCHAR(50) NOT NULL, -- 'contadores' o 'sociedades'
    codigo VARCHAR(100) NOT NULL,
    expediente INT NOT NULL,
    solicitante VARCHAR(255) NOT NULL, -- Nombre de contador o Razón Social
    documento VARCHAR(100) NOT NULL,   -- CC o NIT
    matricula VARCHAR(100) NOT NULL,   -- Tarjeta profesional o N.° registro
    correo VARCHAR(255) DEFAULT NULL,
    representante VARCHAR(255) DEFAULT NULL, -- Solo para sociedades
    tarjeta VARCHAR(50) NOT NULL,      -- Estado de la tarjeta (Activa, Emitida, Suspendida, Cancelada, etc.)
    fecha DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Precargar registros de prueba (semillas/seeds) para Contadores y Sociedades
INSERT INTO tn_tarjetavirtual_tarjetas (id, tipo_tarjeta, codigo, expediente, solicitante, documento, matricula, correo, representante, tarjeta, fecha) VALUES
(618, 'contadores', 'TJM-20260709162254-441227', 427524, 'Sebastian Cuencar Cardona', 'CC 1035441227', 'TP 441227-T', 'scuencar@nexura.com', NULL, 'Activa', '2026-07-09'),
(616, 'contadores', 'TJM-20260708094946-441229', 427525, 'Laura Martínez Gómez', 'CC 1035441229', 'TP 441229-T', 'scuencar@nexura.com', NULL, 'Activa', '2026-07-08'),
(701, 'sociedades', 'TJS-202607120001', 427530, 'Cuencar Consultores S.A.S.', '901.456.789-1', 'SC-001458', 'carga7_11950@example.test', 'Sebastian Cuencar Cardona', 'Activa', '2026-07-12'),
(702, 'sociedades', 'TJS-202607110002', 427531, 'Auditores del Valle Ltda.', '900.325.741-8', 'SC-001459', 'carga7_11950@example.test', 'Laura Martínez Gómez', 'Emitida', '2026-07-11')
ON DUPLICATE KEY UPDATE id=VALUES(id);

-- 2026-08-06
-- Creación de la tabla de historial de estados para tarjetas virtuales
CREATE TABLE IF NOT EXISTS tn_tarjetavirtual_estados_historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tarjeta_id INT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    descripcion TEXT DEFAULT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    realizado_por VARCHAR(100) DEFAULT 'Sistema',
    FOREIGN KEY (tarjeta_id) REFERENCES tn_tarjetavirtual_tarjetas(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Creación de la tabla de historial de lecturas / auditoría de código QR
CREATE TABLE IF NOT EXISTS tn_tarjetavirtual_lecturas_historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tarjeta_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    endpoint VARCHAR(255) NOT NULL,
    metodo VARCHAR(10) NOT NULL,
    codigo_http INT NOT NULL,
    ip VARCHAR(45) NOT NULL,
    FOREIGN KEY (tarjeta_id) REFERENCES tn_tarjetavirtual_tarjetas(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Limpiar antes de insertar para evitar duplicados en reinicios locales
TRUNCATE TABLE tn_tarjetavirtual_estados_historial;
TRUNCATE TABLE tn_tarjetavirtual_lecturas_historial;

-- Insertar historial de estados inicial
INSERT INTO tn_tarjetavirtual_estados_historial (tarjeta_id, estado, descripcion, fecha, realizado_por) VALUES
(618, 'Creada', 'Creación inicial del registro de matrícula.', '2026-07-09 09:00:00', 'Sistema'),
(618, 'Emitida', 'Tarjeta digital emitida formalmente.', '2026-07-09 10:00:00', 'Sebastian Cuencar'),
(618, 'Activa', 'Tarjeta activada por el titular.', '2026-07-09 16:22:54', 'Sebastian Cuencar'),
(701, 'Creada', 'Creación inicial del registro de la sociedad.', '2026-07-12 08:30:00', 'Sistema'),
(701, 'Activa', 'Sociedad activa con tarjeta digital.', '2026-07-12 10:00:00', 'Laura Martínez');

-- Insertar historial de lecturas QR inicial
INSERT INTO tn_tarjetavirtual_lecturas_historial (tarjeta_id, fecha, endpoint, metodo, codigo_http, ip) VALUES
(618, '2026-07-10 14:30:22', '/api/tarjetas/verificar', 'GET', 200, '186.29.112.5'),
(618, '2026-07-11 09:15:47', '/api/tarjetas/verificar', 'GET', 200, '190.7.114.23'),
(701, '2026-07-13 11:20:10', '/api/tarjetas/verificar', 'GET', 200, '181.49.82.17');

-- Creación de la tabla de configuración del validador QR
CREATE TABLE IF NOT EXISTS tn_tarjetavirtual_validador_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL UNIQUE,
    val_foto TINYINT NOT NULL DEFAULT 1,
    val_nombres TINYINT NOT NULL DEFAULT 1,
    val_matricula TINYINT NOT NULL DEFAULT 1,
    val_numero_identificacion TINYINT NOT NULL DEFAULT 0,
    val_codigo_tarjeta TINYINT NOT NULL DEFAULT 1,
    val_estado TINYINT NOT NULL DEFAULT 1,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Limpiar antes de insertar para evitar duplicados en reinicios locales
TRUNCATE TABLE tn_tarjetavirtual_validador_config;

-- Insertar configuración por defecto para el cliente 20002
INSERT INTO tn_tarjetavirtual_validador_config (client_id, val_foto, val_nombres, val_matricula, val_numero_identificacion, val_codigo_tarjeta, val_estado) VALUES
(20002, 1, 1, 1, 0, 1, 1);

-- Creación de la tabla de certificados emitidos
CREATE TABLE IF NOT EXISTS tn_tarjetavirtual_certificados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    expediente INT NOT NULL,
    titular VARCHAR(150) NOT NULL,
    documento VARCHAR(50) NOT NULL,
    matricula VARCHAR(50) NOT NULL,
    correo VARCHAR(150) DEFAULT NULL,
    archivo_pdf VARCHAR(255) DEFAULT 'Certificado de vigencia y antecedentes.pdf',
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Limpiar antes de insertar para evitar duplicados en reinicios locales
TRUNCATE TABLE tn_tarjetavirtual_certificados;

-- Insertar certificados semilla basados en los datos estáticos de la plantilla
INSERT INTO tn_tarjetavirtual_certificados (client_id, expediente, titular, documento, matricula, correo, archivo_pdf) VALUES
(20002, 427524, 'Sebastian Cuencar Cardona', 'CC 1035441227', 'TP 441227-T', 'scuencar@nexura.com', 'Certificado de vigencia y antecedentes.pdf'),
(20002, 427525, 'Laura Martínez Gómez', 'CC 1035441229', 'TP 441229-T', 'laura.martinez@example.com', 'Certificado de vigencia y antecedentes.pdf'),
(20002, 427526, 'Andrés Felipe Ruiz', 'CC 1035441228', 'TP 441228-T', 'andres.ruiz@example.com', 'Certificado de vigencia y antecedentes.pdf'),
(20002, 427530, 'Cuencar Consultores S.A.S.', 'NIT 901.456.789-1', 'SC-001458', 'contacto@cuencarconsultores.com', 'Certificado de vigencia y antecedentes.pdf'),
(20002, 427531, 'Auditores del Valle Ltda.', 'NIT 900.325.741-8', 'SC-001459', 'contacto@auditoresdelvalle.com', 'Certificado de vigencia y antecedentes.pdf');

