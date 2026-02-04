# Tabla: customers

## Identificación
- Nombre: customers
- Esquema: sales
- Tipo: dimensión
- Sistema origen: CRM
- Data owner: Sales team
- Data steward: Data Office

## Descripción funcional
Contiene información de clientes activos e históricos.
Se utiliza para análisis comerciales y segmentación de clientes.

## Nivel de granularidad
- 1 fila = 1 cliente

## Columnas principales
| Columna | Tipo | Descripción |
|--------|------|-------------|
| customer_id | int | Identificador único del cliente |
| country | string | País de residencia del cliente |
| region | string | Región geográfica estándar |
| is_active | boolean | Indica si el cliente está activo |

## Descripción detallada de columnas

### customer_id
Identificador único del cliente en el sistema CRM.  
Se utiliza para realizar joins con tablas de pedidos y facturación.

### country
País de residencia fiscal del cliente.  
Utiliza códigos ISO-2 (ES, FR, JP).  
Se usa para análisis por país.

### region
Región geográfica estándar definida por la empresa.  
Ejemplos: Asia, Europa, América.  
Se deriva a partir del país mediante una tabla de referencia.

### is_active
Indica si el cliente está activo actualmente.  
`true` → cliente activo  
`false` → cliente inactivo

## Filtros comunes
- Clientes activos → `is_active = true`
- Clientes de Asia → `region = 'Asia'`

## Casos de uso habituales
- Segmentación de clientes por región
- Reporting comercial
- Análisis de clientes activos

## Sensibilidad del dato
- Contiene PII: Sí
- Nivel: Medio

## Última actualización
- Fecha: 2025-01-10
