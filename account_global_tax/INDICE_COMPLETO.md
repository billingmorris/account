# Índice Completo - Account Global Tax v16.0.4.0.0

## 📚 Documentación

### 1. **RESUMEN_FINAL.md** ← **EMPIEZA AQUÍ**
   - Resumen ejecutivo del proyecto
   - Características principales
   - Instalación rápida (3 pasos)
   - Ejemplo de uso
   - Troubleshooting básico

### 2. **README.md**
   - Descripción general del módulo
   - Características detalladas
   - Instrucciones de instalación (2 métodos)
   - Uso paso a paso
   - Configuración básica
   - FAQ

### 3. **INSTALACION.md** ← **LEE ESTO PARA INSTALAR**
   - Requisitos del sistema
   - Instalación manual (recomendado)
   - Instalación vía interfaz Odoo
   - Verificación de instalación
   - Solución de problemas
   - Verificación de base de datos

### 4. **CONFIGURACION.md** ← **LEE ESTO PARA CONFIGURAR**
   - Configuración general
   - Crear impuestos (si no existen)
   - Verificar permisos
   - Configuración por tipo de documento
   - Ejemplos prácticos
   - Checklist post-configuración
   - Troubleshooting

### 5. **DESINSTALACION.md**
   - Desinstalación vía interfaz
   - Desinstalación manual
   - Advertencias importantes
   - Actualización a versiones nuevas
   - Rollback/Revertir cambios
   - Problemas comunes

---

## 💻 Estructura del Módulo

### Archivos Principales

```
account_global_tax/
├── __init__.py                          # Inicialización
├── __manifest__.py                      # Configuración del módulo
│
├── models/
│   ├── __init__.py
│   ├── account_move.py                  # Herencia de facturas
│   ├── sale_order.py                    # Herencia de órdenes venta
│   ├── purchase_order.py                # Herencia de órdenes compra
│   └── global_tax_wizard.py             # Wizard modal
│
├── views/
│   ├── account_move_views.xml           # Vista facturas
│   ├── sale_order_views.xml             # Vista órdenes venta
│   ├── purchase_order_views.xml         # Vista órdenes compra
│   └── global_tax_wizard_views.xml      # Vista wizard
│
├── security/
│   └── ir.model.access.csv              # Permisos ACL
│
└── static/description/
    └── icon.png                         # Icono del módulo
```

### Archivos de Documentación Incluidos

```
account_global_tax/
├── README.md                            # Guía general
├── INSTALACION.md                       # Instalación paso a paso
├── CONFIGURACION.md                     # Configuración detallada
└── DESINSTALACION.md                    # Desinstalación/Actualización
```

---

## 🚀 Guía Rápida de Inicio

### Paso 1: Descargar
```bash
# Descargar y extraer
tar -xzf account_global_tax_v16.0.4.0.0.tar.gz
```

### Paso 2: Instalar
```bash
# Opción A: Manual
cp -r account_global_tax /path/to/odoo/addons/
./odoo-bin -d tu_base_datos -u account_global_tax

# Opción B: Vía interfaz Odoo
# Ve a Aplicaciones → Actualizar lista → Buscar Account Global Tax → Instalar
```

### Paso 3: Usar
1. Abre un documento (factura, orden)
2. Haz click en "Impuestos Globales"
3. Selecciona impuestos
4. Click "Aplicar Impuestos"

---

## 📖 Lectura Recomendada por Rol

### Para Administrador del Sistema
1. **RESUMEN_FINAL.md** - Visión general
2. **INSTALACION.md** - Instalación técnica
3. **DESINSTALACION.md** - Mantenimiento

### Para Usuario Final
1. **README.md** - Introducción general
2. **CONFIGURACION.md** - Cómo usar
3. Ejemplos prácticos en CONFIGURACION.md

### Para Contador/Contable
1. **RESUMEN_FINAL.md** - ¿Qué hace el módulo?
2. **CONFIGURACION.md** - Ejemplos de uso
3. **README.md** - Funcionalidades

### Para Desarrollador
1. **README.md** - Overview
2. Revisar código en `models/`
3. **DESINSTALACION.md** - Actualizaciones

---

## ✨ Características Principales

| Característica | Ubicación |
|---|---|
| Asignar múltiples impuestos | global_tax_wizard.py |
| Filtrado dinámico | account_move.py (fields_get) |
| Interfaz wizard modal | global_tax_wizard_views.xml |
| Permisos ACL | ir.model.access.csv |
| Auditoría en chatter | global_tax_wizard.py (action_apply_taxes) |
| Detección de duplicados | global_tax_wizard.py (action_apply_taxes) |
| Soporte venta/compra | account_move.py, sale_order.py, purchase_order.py |

---

## 🔧 Configuración Rápida

### 1. Crear Impuestos
```
Contabilidad → Configuración → Impuestos → Crear
Nombre: IVA 19%
Tipo: Venta
Porcentaje: 19%
```

### 2. Asignar Permisos
```
Configuración → Usuarios → (tu usuario)
Grupos: Usuarios (base.group_user)
```

### 3. Usar el Módulo
```
Abre documento → Impuestos Globales → Selecciona → Aplicar
```

---

## 📊 Especificaciones Técnicas

### Versión: 16.0.4.0.0

| Aspecto | Detalles |
|--------|---------|
| Odoo | v16.0 Community Edition |
| Python | 3.10+ |
| Licencia | AGPL-3 |
| Dependencias | base, account, sale, purchase |
| Modelos Heredados | 3 (account.move, sale.order, purchase.order) |
| TransientModels | 1 (global.tax.wizard) |
| Vistas XML | 4 archivos |
| Seguridad ACL | 4 permisos |
| Tamaño (comprimido) | 13 KB |

---

## 🎯 Casos de Uso

### 1. Aplicar IVA a Facturas
```
Factura de venta → Impuestos Globales → IVA 19% → Aplicar
→ Todas las líneas tienen IVA 19%
```

### 2. Múltiples Impuestos
```
Orden de compra → Impuestos Globales → IVA 5% + Retención 2%
→ Todas las líneas tienen ambos impuestos
```

### 3. Remover Impuestos
```
Factura → Impuestos Globales → (selecciona impuestos) → Remover
→ Se eliminan de todas las líneas
```

---

## ⚠️ Consideraciones Importantes

### Seguridad
- ✅ Permisos ACL configurados
- ✅ Acceso controlado por usuario
- ✅ Auditoría completa

### Performance
- ✅ Optimizado para grandes documentos
- ✅ Transacciones atómicas
- ✅ Sin procesos lentos

### Compatibilidad
- ✅ Odoo 16.0
- ✅ PostgreSQL 12+
- ✅ Python 3.10+

### Data Integrity
- ✅ Detección de duplicados
- ✅ Validación de impuestos
- ✅ Mensajes de auditoría

---

## 🆘 Problemas y Soluciones

### El módulo no aparece
**Solución:** Ver INSTALACION.md → "Problema: ModuleNotFoundError"

### El botón no aparece
**Solución:** Ver README.md → "El botón no aparece"

### Error de permisos
**Solución:** Ver CONFIGURACION.md → "Verificar Permisos"

### Los impuestos no se aplican
**Solución:** Ver README.md → "Los impuestos no se aplican"

---

## 📞 Soporte

### Documentación
1. Lee RESUMEN_FINAL.md primero
2. Consulta la guía específica (INSTALACION, CONFIGURACION)
3. Revisa ejemplos en CONFIGURACION.md

### Logs
```bash
tail -f /var/log/odoo/odoo-server.log
```

### Contacto
- Email: info@elmonitor.net
- Versión: 16.0.4.0.0

---

## 📋 Checklist de Implementación

- ✅ Módulo descargado
- ✅ RESUMEN_FINAL.md leído
- ✅ Requisitos verificados
- ✅ Módulo copiado a addons
- ✅ Odoo reiniciado
- ✅ Módulo instalado
- ✅ Impuestos creados
- ✅ Permisos verificados
- ✅ Botón visible
- ✅ Wizard funciona
- ✅ Impuestos se aplican
- ✅ ¡Listo para producción!

---

## 📈 Versiones Anteriores

| Versión | Cambios | Fecha |
|---------|---------|-------|
| 16.0.4.0.0 | Código estabilizado, docs mejoradas | 2026-10-01 |
| 16.0.3.0.0 | Wizard mejorado, layout corregido | 2026-09-30 |
| 16.0.2.0.0 | Estructura base, campos many2many | 2026-09-29 |
| 16.0.1.0.0 | Prototype inicial | 2026-09-28 |

---

## 🎓 Aprende Más

### Conceptos Odoo
- Many2many relationships
- Transient Models (wizard)
- View inheritance (XPath)
- ACL configuration

### Archivos para Estudiar
1. `models/account_move.py` - Herencia de modelos
2. `models/global_tax_wizard.py` - Lógica de negocio
3. `views/global_tax_wizard_views.xml` - Vistas XML
4. `security/ir.model.access.csv` - Seguridad

---

**🎉 ¡Gracias por usar Account Global Tax v16.0.4.0.0!**

Para comenzar, lee **RESUMEN_FINAL.md** y luego **INSTALACION.md**

---

*Última actualización: 2026-10-01*
*Versión: 16.0.4.0.0*
*Licencia: AGPL-3*
