# StockWise - Project Overview

## 1. Descripción general

StockWise es una plataforma web para la gestión inteligente de inventario, ventas, alertas y reportes operativos, orientada a pequeños negocios que necesitan controlar sus productos, registrar movimientos y tomar mejores decisiones sobre su operación.

El proyecto será desarrollado con una arquitectura modular, utilizando Python, FastAPI, PostgreSQL y React, incorporando buenas prácticas de desarrollo como autenticación, validación de datos, consumo de APIs externas, pruebas automatizadas, contenedores Docker y documentación técnica.

## 2. Problema que resuelve

Muchos pequeños negocios gestionan su inventario de forma manual, en hojas de cálculo o mediante procesos poco organizados. Esto puede generar errores en el control de stock, pérdida de información, dificultad para conocer productos con baja disponibilidad y poca visibilidad sobre las ventas.

StockWise busca centralizar esta información en una plataforma web, permitiendo tener mayor control, trazabilidad y análisis sobre el inventario y las ventas.

## 3. Objetivo general

Desarrollar una plataforma web para gestionar inventario, ventas, alertas y reportes operativos de pequeños negocios, aplicando una arquitectura modular y tecnologías modernas de desarrollo web.

## 4. Objetivos específicos

- Implementar autenticación y gestión de usuarios.
- Registrar productos, categorías y movimientos de inventario.
- Gestionar ventas y actualización automática del stock.
- Generar alertas de stock bajo.
- Construir reportes operativos y dashboard.
- Consumir APIs externas para agregar funcionalidades reales.
- Documentar la arquitectura, decisiones técnicas y modelo de datos.
- Preparar el proyecto para una futura evolución hacia microservicios.

## 5. Alcance inicial

La primera versión del sistema incluirá:

- Login de usuarios.
- Gestión de productos.
- Gestión de categorías.
- Entradas y salidas de inventario.
- Registro de ventas.
- Alertas de stock bajo.
- Dashboard inicial.
- API documentada con Swagger.

## 6. Alcance futuro

En fases posteriores se contempla:

- Microservicio de notificaciones.
- Microservicio de reportes.
- Integración con API externa de tasa de cambio.
- Exportación de reportes en PDF/Excel.
- CI/CD con GitHub Actions.
- Despliegue en la nube.
- Integración básica de inteligencia para sugerencias de compra.