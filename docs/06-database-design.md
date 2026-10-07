# StockWise - Database Design

## 1. Descripción general

La base de datos de StockWise utiliza PostgreSQL y almacena la información necesaria para gestionar usuarios, categorías, productos, movimientos de inventario, ventas y sus respectivos detalles.

El acceso a los datos se realiza mediante SQLAlchemy y la evolución del esquema se gestiona mediante migraciones con Alembic.

La versión 1.0 utiliza las siguientes tablas principales:

- users
- categories
- products
- inventory_movements
- sales
- sale_items

Los roles de usuario se almacenan directamente en la tabla `users` y no requieren una tabla independiente.

La condición de stock bajo se determina a partir de los valores `current_stock` y `minimum_stock` de cada producto, por lo que no existe una tabla independiente de alertas de stock.

---

## 2. Entidades principales

### User

Representa a los usuarios que pueden autenticarse y utilizar la plataforma.

**Tabla:** `users`

Campos:

- `id` — Identificador único del usuario.
- `name` — Nombre del usuario.
- `email` — Correo electrónico único utilizado para autenticación.
- `hashed_password` — Contraseña almacenada mediante hash.
- `role` — Rol asignado al usuario.
- `is_active` — Indica si el usuario puede utilizar el sistema.

Roles utilizados por la aplicación:

- `admin`
- `seller`
- `inventory_operator`

Reglas principales:

- El correo electrónico debe ser único.
- La contraseña nunca se almacena en texto plano.
- Los usuarios inactivos no pueden autenticarse.
- El rol determina las operaciones autorizadas para cada usuario.

---

### Category

Representa una categoría utilizada para clasificar productos.

**Tabla:** `categories`

Campos:

- `id` — Identificador único de la categoría.
- `name` — Nombre único de la categoría.
- `description` — Descripción opcional.
- `is_active` — Indica si la categoría se encuentra activa.

Reglas principales:

- El nombre de la categoría debe ser único.
- Las categorías pueden activarse o desactivarse.

---

### Product

Representa los productos administrados por StockWise.

**Tabla:** `products`

Campos:

- `id` — Identificador único del producto.
- `name` — Nombre del producto.
- `code` — Código único del producto.
- `description` — Descripción opcional.
- `price` — Precio del producto con precisión decimal.
- `current_stock` — Cantidad disponible actualmente.
- `minimum_stock` — Nivel mínimo utilizado para identificar productos con stock bajo.
- `category_id` — Categoría a la que pertenece el producto.
- `is_active` — Indica si el producto se encuentra activo.

Relaciones:

- `category_id` referencia `categories.id`.

Reglas principales:

- Cada producto pertenece a una categoría.
- El código del producto debe ser único.
- El inventario actual se modifica mediante operaciones de inventario y ventas.
- Un producto se considera con stock bajo cuando su stock actual es menor o igual a su stock mínimo.

---

### InventoryMovement

Representa los movimientos que modifican o registran cambios sobre el inventario.

**Tabla:** `inventory_movements`

Campos:

- `id` — Identificador único del movimiento.
- `product_id` — Producto relacionado con el movimiento.
- `sale_id` — Venta relacionada con el movimiento, cuando aplica.
- `movement_type` — Tipo de movimiento registrado.
- `quantity` — Cantidad involucrada.
- `reason` — Motivo opcional del movimiento.
- `created_at` — Fecha y hora de creación del movimiento.

Relaciones:

- `product_id` referencia `products.id`.
- `sale_id` referencia `sales.id` y puede ser nulo.

El campo `sale_id` permite relacionar movimientos de inventario con operaciones de venta cuando corresponde, manteniendo trazabilidad entre ambos procesos.

---

### Sale

Representa una venta registrada en el sistema.

**Tabla:** `sales`

Campos:

- `id` — Identificador único de la venta.
- `seller_id` — Usuario responsable de registrar la venta.
- `status` — Estado actual de la venta.
- `created_at` — Fecha y hora de creación.

Relaciones:

- `seller_id` referencia `users.id`.
- Una venta puede contener múltiples registros en `sale_items`.
- Una venta puede estar relacionada con movimientos de inventario.

La venta permanece almacenada aunque posteriormente sea cancelada, permitiendo conservar su trazabilidad histórica.

---

### SaleItem

Representa cada producto incluido dentro de una venta.

**Tabla:** `sale_items`

Campos:

- `id` — Identificador único del detalle.
- `sale_id` — Venta a la que pertenece.
- `product_id` — Producto vendido.
- `quantity` — Cantidad vendida.
- `unit_price` — Precio unitario registrado para la venta.

Relaciones:

- `sale_id` referencia `sales.id`.
- `product_id` referencia `products.id`.

El precio unitario se almacena en el detalle de venta para preservar el valor utilizado al momento de registrar la operación, independientemente de cambios posteriores en el precio actual del producto.

---

## 3. Relaciones principales

Las relaciones principales del modelo de datos son:

- Una categoría puede tener múltiples productos.
- Cada producto pertenece a una categoría.
- Un producto puede tener múltiples movimientos de inventario.
- Un movimiento de inventario pertenece a un producto.
- Un usuario puede registrar múltiples ventas.
- Cada venta pertenece al usuario que la registró mediante `seller_id`.
- Una venta puede contener múltiples detalles de venta.
- Cada detalle pertenece a una venta.
- Un producto puede aparecer en múltiples detalles de venta.
- Un movimiento de inventario puede estar relacionado con una venta mediante `sale_id`.

De forma simplificada:

`Category 1 ─── N Product`

`Product 1 ─── N InventoryMovement`

`User 1 ─── N Sale`

`Sale 1 ─── N SaleItem`

`Product 1 ─── N SaleItem`

`Sale 1 ─── N InventoryMovement`

---

## 4. Reglas de integridad

La aplicación y la base de datos deben preservar las siguientes reglas:

- El correo electrónico de cada usuario debe ser único.
- El código de cada producto debe ser único.
- El nombre de cada categoría debe ser único.
- Cada producto debe estar asociado a una categoría existente.
- Cada movimiento de inventario debe estar asociado a un producto existente.
- Cada venta debe estar asociada al usuario que la registró.
- Cada detalle de venta debe pertenecer a una venta y estar asociado a un producto.
- Una venta no puede completarse cuando no existe stock suficiente.
- Registrar una venta debe reducir el inventario correspondiente.
- Cancelar una venta elegible debe restaurar el inventario correspondiente.
- La cancelación de una venta no debe eliminar su registro histórico.
- Las operaciones de inventario deben mantener la consistencia del stock.

---

## 5. Decisiones de diseño

### Roles sin tabla independiente

La versión 1.0 no utiliza una tabla `roles`. El rol se almacena directamente en `users.role`.

Esta solución mantiene simple el modelo actual y permite aplicar autorización basada en roles sin introducir una entidad adicional.

### Stock bajo calculado

La versión 1.0 no utiliza una tabla `stock_alerts`.

El estado de stock bajo puede determinarse comparando:

`current_stock <= minimum_stock`

Esto evita persistir información que puede derivarse directamente del estado actual del producto.

### Trazabilidad de ventas

Las ventas se mantienen como registros históricos y utilizan un campo de estado en lugar de eliminarse cuando son canceladas.

Los movimientos de inventario pueden incluir una referencia opcional a la venta mediante `sale_id`, permitiendo relacionar los cambios de stock con la operación que los originó.

### Valores monetarios

Los precios se almacenan utilizando tipos numéricos de precisión decimal para evitar los problemas de precisión asociados con valores de punto flotante.

---

## 6. Migraciones

Los cambios en el esquema de base de datos se gestionan mediante Alembic.

Las migraciones permiten:

- Crear y modificar tablas de forma controlada.
- Mantener el esquema sincronizado con los modelos SQLAlchemy.
- Conservar un historial de cambios estructurales.
- Evolucionar la base de datos a medida que se incorporan nuevas funcionalidades.

Las modificaciones futuras del modelo de datos deben realizarse mediante nuevas migraciones en lugar de modificar manualmente el esquema de producción.