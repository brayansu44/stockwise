# StockWise - User Stories

## Epic 1: Autenticación y usuarios

### HU-001: Iniciar sesión

Como usuario registrado, quiero iniciar sesión en la plataforma para acceder a las funcionalidades según mi rol.

#### Criterios de aceptación

- El usuario debe ingresar correo y contraseña.
- El sistema debe validar las credenciales.
- Si las credenciales son correctas, el sistema debe generar un token de acceso.
- Si las credenciales son incorrectas, el sistema debe mostrar un mensaje de error.
- Solo usuarios activos pueden iniciar sesión.

---

### HU-002: Gestionar usuarios

Como administrador, quiero crear, editar, activar e inactivar usuarios para controlar quién puede acceder al sistema.

#### Criterios de aceptación

- Solo el administrador puede gestionar usuarios.
- Se debe registrar nombre, correo, contraseña y rol.
- El correo debe ser único.
- Un usuario puede estar activo o inactivo.
- Un usuario inactivo no puede iniciar sesión.

---

## Epic 2: Productos e inventario

### HU-003: Gestionar categorías

Como administrador u operador de inventario, quiero crear, editar y consultar categorías para organizar los productos.

#### Criterios de aceptación

- Una categoría debe tener nombre.
- El nombre de la categoría debe ser único.
- Una categoría puede estar activa o inactiva.
- No se deben eliminar categorías con productos asociados.

---

### HU-004: Gestionar productos

Como administrador u operador de inventario, quiero crear, editar y consultar productos para mantener actualizado el catálogo del negocio.

#### Criterios de aceptación

- Un producto debe tener nombre, código, categoría, precio, stock actual y stock mínimo.
- El código del producto debe ser único.
- El precio no puede ser negativo.
- El stock actual no puede ser negativo.
- El producto debe pertenecer a una categoría activa.

---

### HU-005: Registrar entrada de inventario

Como operador de inventario, quiero registrar entradas de productos para aumentar el stock disponible.

#### Criterios de aceptación

- Se debe seleccionar un producto existente.
- La cantidad debe ser mayor a cero.
- Al registrar la entrada, el stock del producto debe aumentar.
- Debe quedar trazabilidad del movimiento.

---

### HU-006: Registrar venta

Como vendedor, quiero registrar ventas para descontar automáticamente productos del inventario.

#### Criterios de aceptación

- Se debe seleccionar uno o varios productos.
- La cantidad vendida debe ser mayor a cero.
- No se puede vender más cantidad que el stock disponible.
- Al registrar la venta, el stock debe disminuir automáticamente.
- La venta debe guardar fecha, usuario y total.

---

## Epic 3: Alertas y reportes

### HU-007: Generar alerta de stock bajo

Como operador de inventario, quiero que el sistema genere alertas cuando un producto tenga stock bajo para tomar acciones a tiempo.

#### Criterios de aceptación

- El sistema debe comparar stock actual contra stock mínimo.
- Si el stock actual es menor o igual al stock mínimo, debe generarse una alerta.
- La alerta debe estar asociada a un producto.
- Una alerta puede marcarse como atendida.

---

### HU-008: Consultar dashboard

Como administrador, quiero consultar un dashboard con indicadores principales para conocer el estado general del negocio.

#### Criterios de aceptación

- El dashboard debe mostrar total de productos.
- Debe mostrar productos con stock bajo.
- Debe mostrar ventas recientes.
- Debe mostrar ingresos acumulados.