# Account Global Tax - Odoo v16

Módulo que permite asignar múltiples impuestos globales a todas las líneas de productos en documentos (facturas, órdenes de compra/venta, cotizaciones) con un solo clic.

## ✨ Características

- **Asignar impuestos globales** a todas las líneas de un documento
- **Soporta múltiples documentos**: facturas de venta/compra, órdenes de venta/compra, cotizaciones
- **Interfaz wizard** modal para seleccionar impuestos
- **Filtrado automático** de impuestos por tipo (venta/compra)
- **Detección de duplicados** - no aplica impuestos repetidos
- **Remover impuestos** con un clic
- **Registros de auditoría** en el chatter del documento
- **Etiquetas en español** en toda la interfaz

## 📦 Instalación

### Opción 1: Instalación Manual
1. Descarga el módulo en una carpeta
2. Colócalo en `addons/` de tu instalación Odoo
3. Reinicia el servidor Odoo: `./odoo-bin -d tu_base_de_datos -u account_global_tax`

### Opción 2: Instalación vía Odoo
1. Ve a Aplicaciones → Actualizar lista de aplicaciones
2. Busca "Account Global Tax"
3. Click en Instalar

## 🚀 Uso

### Paso 1: Abrir un documento
- Ve a Contabilidad → Facturas (o cualquier otro documento)
- Abre una factura, orden de compra o de venta

### Paso 2: Hacer clic en "Impuestos Globales"
- En la barra de botones, verás un botón "Impuestos Globales" con icono de calculadora
- Haz clic para abrir el wizard

### Paso 3: Seleccionar impuestos
- El wizard se abre en modal
- Selecciona uno o más impuestos de la lista
- Los impuestos se filtran automáticamente según el tipo de documento

### Paso 4: Aplicar o Remover
- **Aplicar Impuestos**: Agrega los impuestos a todas las líneas
- **Remover Impuestos**: Elimina los impuestos de todas las líneas
- Los impuestos ya existentes no se duplican

### Paso 5: Confirmación
- El documento registra la acción en el chatter
- Puedes ver el historial de cambios

## 🔧 Configuración

### Permisos
El módulo asigna automáticamente permisos al grupo "Usuarios". Los usuarios pueden:
- Ver y editar documentos con impuestos globales
- Acceder al wizard
- Aplicar/remover impuestos

### Filtrado de impuestos

**Para facturas (account.move):**
- Si es factura de venta → Solo muestra impuestos de venta
- Si es factura de compra → Solo muestra impuestos de compra

**Para órdenes de venta:** Solo muestra impuestos de venta
**Para órdenes de compra:** Solo muestra impuestos de compra

## 📋 Campos Agregados

### global_tax_ids
- **Tipo:** Many2many (account.tax)
- **Descripción:** Impuestos globales seleccionados para aplicar a todas las líneas
- **Disponible en:** account.move, sale.order, purchase.order

### Wizard (global.tax.wizard)
- **global_tax_ids:** Many2many de impuestos a aplicar
- **total_lines:** Contador de líneas en el documento
- **tax_count:** Contador de impuestos seleccionados (computed)
- **document_model:** Modelo del documento activo
- **document_id:** ID del documento activo

## 🐛 Solución de Problemas

### El botón no aparece
- Asegúrate de que el módulo esté instalado
- Recarga la página (Ctrl+F5)
- Verifica que tengas permisos de usuario

### El wizard no se abre
- Comprueba que el servidor Odoo esté corriendo
- Revisa el archivo de log del servidor para errores
- Verifica los permisos en Configuración → Usuarios

### Los impuestos no se aplican
- Asegúrate de seleccionar al menos un impuesto
- Verifica que el impuesto sea del tipo correcto (venta/compra)
- Comprueba que las líneas del documento tengan un producto

### Error de permisos
- Ve a Configuración → Modelos
- Busca "Global Tax Configuration Wizard"
- Asigna permisos al grupo de usuarios

## 📝 Cambios Recientes (v16.0.4.0.0)

- ✅ Estabilización del código
- ✅ Mejora en la detección de documentos
- ✅ Mejor manejo de errores
- ✅ Documentación mejorada

## 📞 Soporte

Para reportar problemas o sugerencias:
- Contacta al administrador de Odoo
- Revisa los logs del servidor

## 📄 Licencia

AGPL-3

## 👨‍💻 Autor

El Monitor

---

**Versión:** 16.0.4.0.0
**Última actualización:** 2026-10-01
