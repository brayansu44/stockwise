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

### CU-005: Generar alerta de stock bajo

**Actor principal:** Sistema

**Descripción:**  
Permite generar una alerta automática cuando un producto alcanza o baja de su stock mínimo.

**Flujo principal:**
1. El sistema actualiza el stock de un producto.
2. El sistema compara el stock actual con el stock mínimo.
3. Si el stock actual es menor o igual al mínimo, genera una alerta.
4. La alerta queda disponible para consulta.

**Flujos alternos:**
- Si ya existe una alerta pendiente para el producto, el sistema no debe duplicarla.

---

### CU-006: Consultar dashboard

**Actor principal:** Administrador

**Descripción:**  
Permite consultar indicadores principales del negocio.

**Flujo principal:**
1. El usuario accede al dashboard.
2. El sistema calcula indicadores principales.
3. El sistema muestra productos registrados, stock bajo, ventas recientes e ingresos acumulados.