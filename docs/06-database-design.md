# StockWise - Database Design

## 1. Descripción general

La base de datos de StockWise almacenará la información relacionada con usuarios, roles, categorías, productos, movimientos de inventario, ventas, detalle de ventas y alertas de stock bajo.

## 2. Entidades principales

### User

Representa a los usuarios que pueden acceder al sistema.

Campos iniciales:

- id
- full_name
- email
- password_hash
- role_id
- is_active
- created_at
- updated_at

### Role

Representa los roles del sistema.

Campos iniciales:

- id
- name
- description

Roles iniciales:

- ADMIN
- SELLER
- INVENTORY_OPERATOR

### Category

Representa las categorías de productos.

Campos iniciales:

- id
- name
- description
- is_active
- created_at
- updated_at

### Product

Representa los productos registrados en el sistema.

Campos iniciales:

- id
- name
- code
- description
- category_id
- price
- current_stock
- minimum_stock
- is_active
- created_at
- updated_at

### InventoryMovement

Representa entradas y salidas de inventario.

Campos iniciales:

- id
- product_id
- user_id
- movement_type
- quantity
- reason
- created_at

Tipos de movimiento:

- IN
- OUT
- ADJUSTMENT

### Sale

Representa una venta realizada.

Campos iniciales:

- id
- user_id
- total_amount
- created_at

### SaleItem

Representa los productos asociados a una venta.

Campos iniciales:

- id
- sale_id
- product_id
- quantity
- unit_price
- subtotal

### StockAlert

Representa una alerta generada por bajo stock.

Campos iniciales:

- id
- product_id
- message
- status
- created_at
- resolved_at

Estados:

- PENDING
- RESOLVED

## 3. Relaciones principales

- Un usuario pertenece a un rol.
- Un rol puede tener varios usuarios.
- Una categoría puede tener varios productos.
- Un producto pertenece a una categoría.
- Un producto puede tener muchos movimientos de inventario.
- Un usuario puede registrar muchos movimientos.
- Un usuario puede registrar muchas ventas.
- Una venta puede tener muchos detalles de venta.
- Un producto puede estar en muchos detalles de venta.
- Un producto puede tener muchas alertas de stock.

## 4. Reglas de integridad

- El correo del usuario debe ser único.
- El código del producto debe ser único.
- El nombre de la categoría debe ser único.
- El precio del producto no puede ser negativo.
- El stock actual no puede ser negativo.
- La cantidad de un movimiento debe ser mayor a cero.
- Una venta no puede registrarse si no hay stock suficiente.