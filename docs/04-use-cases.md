# StockWise - Use Cases

## 1. Actores del sistema

### Administrador
Usuario con permisos completos sobre la plataforma.

### Vendedor
Usuario encargado de registrar ventas y consultar productos disponibles.

### Operador de inventario
Usuario encargado de registrar entradas, salidas y ajustes de inventario.

---

## 2. Casos de uso principales

### CU-001: Iniciar sesión

**Actor principal:** Administrador, Vendedor, Operador de inventario

**Descripción:**  
Permite que un usuario registrado acceda al sistema mediante correo y contraseña.

**Flujo principal:**
1. El usuario ingresa correo y contraseña.
2. El sistema valida las credenciales.
3. El sistema verifica que el usuario esté activo.
4. El sistema genera un token de acceso.
5. El usuario accede a la plataforma.

**Flujos alternos:**
- Si las credenciales son incorrectas, el sistema muestra un error.
- Si el usuario está inactivo, el sistema bloquea el acceso.

---

### CU-002: Gestionar productos

**Actor principal:** Administrador, Operador de inventario

**Descripción:**  
Permite crear, editar, consultar e inactivar productos.

**Flujo principal:**
1. El usuario accede al módulo de productos.
2. El sistema muestra el listado de productos.
3. El usuario registra o edita la información del producto.
4. El sistema valida los datos.
5. El sistema guarda los cambios.

**Flujos alternos:**
- Si el código del producto ya existe, el sistema muestra un error.
- Si la categoría está inactiva, el sistema no permite asociarla.
- Si los datos son inválidos, el sistema informa los campos requeridos.

---

### CU-003: Registrar entrada de inventario

**Actor principal:** Administrador, Operador de inventario

**Descripción:**  
Permite registrar el ingreso de unidades a un producto existente.

**Flujo principal:**
1. El usuario selecciona un producto.
2. El usuario ingresa la cantidad.
3. El usuario registra el motivo de la entrada.
4. El sistema valida la cantidad.
5. El sistema aumenta el stock del producto.
6. El sistema registra el movimiento.

**Flujos alternos:**
- Si la cantidad es menor o igual a cero, el sistema muestra un error.
- Si el producto está inactivo, el sistema no permite registrar la entrada.

---

### CU-004: Registrar venta

**Actor principal:** Vendedor, Administrador

**Descripción:**  
Permite registrar una venta y descontar automáticamente el inventario.

**Flujo principal:**
1. El usuario selecciona uno o varios productos.
2. El usuario ingresa las cantidades.
3. El sistema valida disponibilidad de stock.
4. El sistema calcula el total de la venta.
5. El sistema registra la venta.
6. El sistema descuenta el stock.
7. El sistema registra los movimientos de salida.

**Flujos alternos:**
- Si no hay stock suficiente, el sistema bloquea la venta.
- Si un producto está inactivo, el sistema no permite venderlo.

---

### CU-005: Consultar productos con stock bajo

**Actor principal:** Usuario autorizado

**Descripción:**  
Permite identificar productos cuyo stock actual es menor o igual al nivel mínimo configurado.

**Flujo principal:**

1. El usuario accede a la información de stock bajo.
2. El sistema consulta la información actual de los productos.
3. El sistema compara `current_stock` con `minimum_stock`.
4. El sistema identifica los productos que cumplen la condición `current_stock <= minimum_stock`.
5. El sistema muestra la información actualizada al usuario.

**Flujos alternos:**

- Si ningún producto cumple la condición de stock bajo, el sistema muestra el resultado sin productos en alerta.
- Los cambios producidos por movimientos de inventario o ventas se reflejan en la información de stock bajo.

---

### CU-006: Consultar dashboard

**Actor principal:** Usuario autorizado

**Descripción:**  
Permite consultar indicadores principales del negocio.

**Flujo principal:**
1. El usuario accede al dashboard.
2. El sistema calcula indicadores principales.
3. El sistema muestra productos registrados, stock bajo, ventas recientes e ingresos acumulados.

---

### CU-007: Gestionar usuarios

**Actor principal:** Administrador

**Descripción:**  
Permite al administrador consultar, crear, editar, activar y desactivar usuarios del sistema.

**Flujo principal:**
1. El administrador accede al módulo de usuarios.
2. El sistema muestra el listado de usuarios registrados.
3. El administrador selecciona la acción que desea realizar.
4. Para crear un usuario, ingresa nombre completo, correo electrónico, contraseña y rol.
5. Para editar un usuario, modifica su nombre, correo electrónico o rol.
6. El sistema valida la información ingresada.
7. El sistema guarda los cambios.
8. El listado de usuarios se actualiza con la información registrada.

**Flujos alternos:**
- Si el correo electrónico ya está registrado, el sistema rechaza la operación.
- Si los datos ingresados son inválidos, el sistema muestra el error correspondiente.
- El administrador puede desactivar un usuario activo.
- El administrador puede activar un usuario inactivo.
- Un usuario inactivo no puede iniciar sesión.
- Si un usuario que no es administrador intenta acceder al módulo, el sistema deniega el acceso.

---

### CU-008: Gestionar categorías

**Actor principal:** Administrador, Operador de inventario

**Descripción:**  
Permite consultar, crear, editar, activar y desactivar categorías utilizadas para clasificar productos.

**Flujo principal:**
1. El usuario accede al módulo de categorías.
2. El sistema muestra las categorías registradas.
3. El usuario crea una nueva categoría o selecciona una existente para editarla.
4. El usuario ingresa o modifica el nombre y la descripción.
5. El sistema valida la información.
6. El sistema guarda los cambios.
7. El listado de categorías se actualiza.

**Flujos alternos:**
- Si los datos ingresados son inválidos, el sistema muestra un error.
- El usuario puede desactivar una categoría activa.
- El usuario puede activar una categoría inactiva.
- La desactivación conserva el registro de la categoría.

---

### CU-009: Registrar salida o ajuste de inventario

**Actor principal:** Administrador, Operador de inventario

**Descripción:**  
Permite registrar movimientos que disminuyen o ajustan las existencias de un producto.

**Flujo principal:**
1. El usuario accede al módulo de inventario.
2. El usuario selecciona un producto.
3. El usuario selecciona el tipo de movimiento.
4. El usuario ingresa la cantidad y la información requerida para el movimiento.
5. El sistema valida los datos.
6. El sistema actualiza el stock del producto.
7. El sistema registra el movimiento en el historial.

**Flujos alternos:**
- Si la cantidad es inválida, el sistema rechaza el movimiento.
- Si el movimiento produce una condición de stock no permitida, el sistema rechaza la operación.
- Si el producto no es válido para la operación, el sistema muestra el error correspondiente.

---

### CU-010: Consultar historial de inventario

**Actor principal:** Administrador, Operador de inventario

**Descripción:**  
Permite consultar los movimientos registrados sobre el inventario.

**Flujo principal:**
1. El usuario accede al módulo de inventario.
2. El sistema obtiene los movimientos registrados.
3. El sistema muestra el producto asociado, tipo de movimiento, cantidad y demás información disponible.
4. El usuario consulta el historial de movimientos.

**Flujos alternos:**
- Si no existen movimientos registrados, el sistema muestra el historial vacío.
- Si ocurre un error al consultar la información, el sistema informa que no fue posible cargar los movimientos.

---

### CU-011: Consultar ventas

**Actor principal:** Administrador, Vendedor

**Descripción:**  
Permite consultar las ventas registradas y visualizar el detalle de cada transacción.

**Flujo principal:**
1. El usuario accede al módulo de ventas.
2. El sistema muestra el historial de ventas.
3. El usuario selecciona una venta.
4. El sistema muestra el detalle de la transacción.
5. El sistema presenta los productos, cantidades, información histórica, total y estado de la venta.

**Flujos alternos:**
- Si no existen ventas registradas, el sistema muestra el listado vacío.
- Si la venta solicitada no existe, el sistema informa el error correspondiente.

---

### CU-012: Cancelar venta

**Actor principal:** Administrador

**Descripción:**  
Permite cancelar una venta registrada conservando su información histórica y restaurando el inventario correspondiente.

**Precondición:**  
La venta debe existir y encontrarse en un estado que permita su cancelación.

**Flujo principal:**
1. El administrador consulta el módulo de ventas.
2. El administrador selecciona una venta.
3. El administrador solicita cancelar la venta.
4. El sistema solicita confirmación.
5. El administrador confirma la operación.
6. El sistema cambia el estado de la venta.
7. El sistema restaura al inventario las cantidades correspondientes.
8. La venta permanece disponible en el historial con su nuevo estado.

**Flujos alternos:**
- Si la venta no existe, el sistema rechaza la operación.
- Si la venta ya fue cancelada, el sistema no permite cancelarla nuevamente.
- Si el usuario no tiene rol de administrador, el sistema deniega la operación.

---

## 3. Matriz de trazabilidad de casos de uso

| Caso de uso | Funcionalidad | Actor principal |
|---|---|---|
| CU-001 | Iniciar sesión | Administrador, Vendedor, Operador de inventario |
| CU-002 | Gestionar productos | Administrador, Operador de inventario |
| CU-003 | Registrar entrada de inventario | Administrador, Operador de inventario |
| CU-004 | Registrar venta | Vendedor, Administrador |
| CU-005 | Consultar productos con stock bajo | Usuario autorizado |
| CU-006 | Consultar dashboard | Usuario autorizado |
| CU-007 | Gestionar usuarios | Administrador |
| CU-008 | Gestionar categorías | Administrador, Operador de inventario |
| CU-009 | Registrar salida o ajuste de inventario | Administrador, Operador de inventario |
| CU-010 | Consultar historial de inventario | Administrador, Operador de inventario |
| CU-011 | Consultar ventas | Administrador, Vendedor |
| CU-012 | Cancelar venta | Administrador |

