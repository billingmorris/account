# Guía de Configuración - Account Global Tax v16.0.4.0.0

## 🎯 Configuración General

### 1. Crear Impuestos (si no existen)

Para que el módulo funcione, necesitas tener impuestos creados en Odoo.

**Pasos:**
1. Ve a **Contabilidad → Configuración → Impuestos**
2. Haz click en **Crear**
3. Completa los campos:
   - **Nombre:** Ej. "IVA 19%" o "Impuesto a Ventas"
   - **Tipo de Impuesto:** 
     - Selecciona **Venta** para impuestos de cliente
     - Selecciona **Compra** para impuestos de proveedor
   - **Impuesto:** % o cantidad
4. **Guardar**

### 2. Verificar Permisos

**Para administrador:**
- Acceso completo automático

**Para otros usuarios:**
1. Ve a **Configuración → Usuarios**
2. Selecciona el usuario
3. En **Grupos**, asegúrate de que esté en:
   - ✅ Usuarios (base.group_user)
4. **Guardar**

### 3. Verificar Grupos de Acceso

1. Ve a **Configuración → Modelos**
2. Busca los siguientes modelos:
   - account.move
   - sale.order
   - purchase.order
   - global.tax.wizard

3. Para cada uno, ve a la pestaña **ACL**:
   - Verifica que base.group_user tenga permisos de lectura y escritura

## 🔧 Configuración por Tipo de Documento

### Facturas (account.move)

**Filtrado automático:**
- Facturas de **venta** (out_invoice) → Solo impuestos de tipo "Venta"
- Facturas de **compra** (in_invoice) → Solo impuestos de tipo "Compra"
- Notas de crédito de **venta** (out_refund) → Solo impuestos de tipo "Venta"
- Notas de crédito de **compra** (in_refund) → Solo impuestos de tipo "Compra"

**Para usar:**
1. Abre una factura
2. Haz click en "Impuestos Globales"
3. Selecciona impuestos disponibles (ya filtrados)
4. Click en "Aplicar Impuestos"

### Órdenes de Venta (sale.order)

**Filtrado automático:**
- Solo muestra impuestos de tipo "Venta"

**Para usar:**
1. Abre una orden de venta
2. Haz click en "Impuestos Globales"
3. Selecciona impuestos
4. Click en "Aplicar Impuestos"

### Órdenes de Compra (purchase.order)

**Filtrado automático:**
- Solo muestra impuestos de tipo "Compra"

**Para usar:**
1. Abre una orden de compra
2. Haz click en "Impuestos Globales"
3. Selecciona impuestos
4. Click en "Aplicar Impuestos"

## 📊 Ejemplo Práctico

### Caso: Aplicar IVA del 19% a una factura de venta

**Preparación:**
1. Asegúrate de que existe un impuesto "IVA 19%" (tipo Venta, 19%)
2. Abre un proyecto de venta o crea uno nuevo
3. Agrega líneas de productos

**Aplicar impuesto global:**
1. En la factura, haz click en **Impuestos Globales**
2. Se abre el wizard
3. En el campo "Seleccionar Impuestos", busca y selecciona "IVA 19%"
4. Deberías ver un tag con el impuesto
5. Click en **Aplicar Impuestos**
6. El sistema aplicará "IVA 19%" a TODAS las líneas

**Verificación:**
- En cada línea de producto, el impuesto "IVA 19%" debería aparecer
- El chatter mostrará: "Se aplicaron 1 impuestos globales a X líneas"

### Caso: Aplicar múltiples impuestos

**Supongamos:**
- Impuesto A: 5% (tipo Venta)
- Impuesto B: 3% (tipo Venta)
- Impuesto C: 2% (tipo Venta)

**Pasos:**
1. Abre una factura de venta
2. Click en "Impuestos Globales"
3. Selecciona los 3 impuestos (A, B, C)
4. Click en "Aplicar Impuestos"
5. Todas las líneas tendrán los 3 impuestos

### Caso: Remover impuestos

**Si aplicas por error:**
1. Click en "Impuestos Globales"
2. Selecciona los impuestos a remover
3. Click en "Remover Impuestos"
4. Los impuestos se eliminarán de TODAS las líneas

## 🚨 Consideraciones Importantes

### Duplicados
- El módulo **detecta automáticamente** si un impuesto ya existe en una línea
- Si el impuesto ya está aplicado, no lo agrega nuevamente

### Impacto en Cálculos
- El módulo solo agrega/remueve impuestos
- Los cálculos de totales se recalculan automáticamente
- Los valores totales de la factura se actualizan

### Auditoría
- Cada cambio se registra en el **Chatter** del documento
- Puedes ver el historial completo de cambios

## 📋 Checklist Post-Configuración

- ✅ Módulo instalado (Aplicaciones → busca "Account Global Tax")
- ✅ Al menos 2 impuestos creados (venta y compra)
- ✅ Usuarios tienen permisos (base.group_user)
- ✅ Botón "Impuestos Globales" visible en documentos
- ✅ Wizard se abre al hacer click
- ✅ Impuestos se filtran correctamente (venta/compra)

## 🔍 Troubleshooting

### Los impuestos no se aplican aunque hago click
**Causas posibles:**
1. No seleccionaste ningún impuesto
2. Permiso insuficiente (verifica ACL)
3. Las líneas del documento no tienen productos

**Solución:**
1. Asegúrate de seleccionar al menos un impuesto
2. Revisa los permisos en Configuración → Modelos
3. Agrega productos a las líneas antes de aplicar

### El wizard muestra muy pocos impuestos
**Esto es normal:**
- El módulo filtra automáticamente
- Para facturas de venta solo muestra impuestos "Venta"
- Para facturas de compra solo muestra impuestos "Compra"

### Los impuestos no están sincronizados
**Solución:**
1. Recarga la página (Ctrl+F5)
2. Cierra y reabre el documento
3. Reinicia la sesión de Odoo

## 🔐 Seguridad

### Permisos Mínimos
Para que un usuario pueda usar el módulo necesita:
- ✅ Acceso a Contabilidad
- ✅ Pertenencia a grupo "Usuarios" (base.group_user)
- ✅ Lectura y escritura en account.move, sale.order, purchase.order

### Auditoría
- Todos los cambios se registran en el Chatter
- El sistema guarda quién hizo el cambio y cuándo
- Puedes auditar toda la actividad en los documentos

---

**Versión:** 16.0.4.0.0
**Fecha:** 2026-10-01
