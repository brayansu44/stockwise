# StockWise - Business Requirements

## 1. Contexto del negocio

StockWise está orientado a pequeñas y medianas empresas que necesitan controlar su inventario, registrar ventas y obtener información básica para la toma de decisiones.

El sistema busca apoyar negocios que actualmente gestionan sus productos mediante hojas de cálculo, registros manuales o herramientas poco integradas.

## 2. Problema principal

Los negocios pequeños suelen presentar dificultades para mantener actualizado su inventario, conocer productos con bajo stock, registrar movimientos de entrada y salida, y consultar reportes claros sobre sus ventas.

Esto puede generar pérdida de información, errores operativos, sobrecostos, agotamiento de productos y baja trazabilidad.

## 3. Usuarios del sistema

### Administrador

Usuario encargado de configurar el sistema, gestionar usuarios, productos, categorías, inventario y consultar reportes generales.

### Vendedor

Usuario encargado de registrar ventas y consultar productos disponibles.

### Operador de inventario

Usuario encargado de registrar entradas, salidas y ajustes de inventario.

## 4. Necesidades principales

- Gestionar productos y categorías.
- Registrar entradas y salidas de inventario.
- Registrar ventas.
- Actualizar stock automáticamente.
- Generar alertas de stock bajo.
- Consultar reportes operativos.
- Controlar acceso mediante roles.
- Mantener trazabilidad básica de las operaciones.

## 5. Reglas de negocio iniciales

- Un producto debe pertenecer a una categoría.
- Un producto debe tener un stock mínimo definido.
- No se puede registrar una venta si no hay stock suficiente.
- Cada venta debe descontar automáticamente el stock.
- Cada entrada de inventario debe aumentar el stock.
- El sistema debe generar una alerta cuando el stock actual sea menor o igual al stock mínimo.
- Solo el administrador puede gestionar usuarios.
- Solo usuarios autenticados pueden acceder al sistema.

## 6. Alcance de la versión 1.0

La versión 1.0 incluirá:

- Autenticación de usuarios.
- Gestión de roles básicos.
- Gestión de categorías.
- Gestión de productos.
- Registro de entradas de inventario.
- Registro de ventas.
- Alertas de stock bajo.
- Dashboard inicial.
- API documentada con Swagger.

## 7. Fuera del alcance de la versión 1.0

No se incluirá inicialmente:

- Facturación electrónica real.
- Pasarela de pagos real.
- Integración contable.
- Múltiples sedes.
- Aplicación móvil.
- Inteligencia artificial avanzada.
- Microservicios completos desde el inicio.