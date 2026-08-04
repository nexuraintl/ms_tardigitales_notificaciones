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

