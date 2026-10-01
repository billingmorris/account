# Guía de Desinstalación y Actualización

## 🗑️ Desinstalación Completa

### Opción 1: Desinstalación vía Interfaz Odoo

**Paso 1: Desinstalar el módulo**
1. Ve a **Aplicaciones → Aplicaciones**
2. Busca "Account Global Tax"
3. Haz click para abrir
4. Click en el botón **"Desinstalar"**
5. Confirma cuando se te pida

**Paso 2: Limpiar datos (Opcional)**
Si deseas eliminar también los campos y datos:
1. Ve a **Configuración → Modelos**
2. Busca "Account Move", "Sale Order", "Purchase Order"
3. En cada uno, revisa la pestaña **Campos**
4. Busca "global_tax_ids" y verifica
5. (Nota: Los campos se limpian automáticamente en la mayoría de casos)

### Opción 2: Desinstalación Manual

```bash
# 1. Detén el servidor Odoo
sudo systemctl stop odoo

# 2. Elimina la carpeta del módulo
rm -rf /opt/odoo/addons/account_global_tax/

# 3. Limpia datos de la base de datos (CUIDADO - DESTRUCTIVO)
# Conéctate a PostgreSQL y ejecuta:
psql -U odoo -d tu_base_de_datos

# En PostgreSQL:
DROP TABLE IF EXISTS account_move_global_tax_rel;
DROP TABLE IF EXISTS sale_order_global_tax_rel;
DROP TABLE IF EXISTS purchase_order_global_tax_rel;
DROP TABLE IF EXISTS wizard_tax_rel;
DROP TABLE IF EXISTS global_tax_wizard;

# 4. Reinicia Odoo sin actualizar
sudo -u odoo /opt/odoo/odoo-bin -d tu_base_de_datos
```

## ⚠️ Advertencias Importantes

### Antes de Desinstalar
- ✅ Realiza una copia de seguridad de tu base de datos
- ✅ Verifica que no hay impuestos globales aplicados a documentos activos
- ✅ Avisa a los usuarios que el módulo será desinstalado

### Datos que se Perderán
- ❌ Los campos "global_tax_ids" de los documentos
- ❌ Los registros de configuración del wizard
- ❌ Las relaciones entre documentos e impuestos

### Datos que NO se Perderán
- ✅ Los documentos (facturas, órdenes) se mantienen
- ✅ Los impuestos siguen existiendo
- ✅ El historial en chatter se mantiene (excepto registros posteriores a desinstalación)

## 🔄 Actualizar a Versión Más Reciente

### Actualización Automática (Recomendado)

**Paso 1: Descargar nueva versión**
```bash
# Obtén la nueva versión del módulo
wget https://...../account_global_tax_v16.0.5.0.0.tar.gz
tar -xzf account_global_tax_v16.0.5.0.0.tar.gz
```

**Paso 2: Actualizar el módulo**
```bash
# Detén Odoo
sudo systemctl stop odoo

# Reemplaza la carpeta
rm -rf /opt/odoo/addons/account_global_tax/
cp -r account_global_tax /opt/odoo/addons/

# Reinicia con actualización
sudo -u odoo /opt/odoo/odoo-bin -d tu_base_de_datos -u account_global_tax --logfile=/var/log/odoo/odoo-server.log &
```

**Paso 3: Verificar actualización**
1. Accede a Odoo como administrador
2. Ve a **Aplicaciones → Aplicaciones**
3. Busca "Account Global Tax"
4. Verifica que la versión haya cambiado

### Verificación Post-Actualización

```bash
# Ver la versión instalada
grep "'version'" /opt/odoo/addons/account_global_tax/__manifest__.py

# Revisar logs
tail -f /var/log/odoo/odoo-server.log | grep account_global_tax
```

## 🔧 Migración Entre Versiones

### De v16.0.3.x → v16.0.4.x

**Sin cambios en datos:**
- Los campos se mantienen igual
- Las relaciones se preservan
- No hay pérdida de datos

**Pasos:**
1. Actualiza según "Actualización Automática"
2. No requiere reimplementación
3. Puedes continuar usando como antes

### De v16.0.2.x → v16.0.3.x

**Cambios menores:**
- Mejoras en UI del wizard
- Optimizaciones de rendimiento
- Sin cambios en estructura de datos

**Pasos:**
1. Actualiza según "Actualización Automática"
2. Recarga la página del navegador
3. Verifica el nuevo diseño del wizard

## 📊 Rollback (Revertir a Versión Anterior)

Si encuentras problemas con una nueva versión:

```bash
# 1. Detén Odoo
sudo systemctl stop odoo

# 2. Restaura la carpeta anterior
rm -rf /opt/odoo/addons/account_global_tax/
cp -r account_global_tax_OLD /opt/odoo/addons/account_global_tax/

# 3. Reinicia con actualización de la versión anterior
sudo -u odoo /opt/odoo/odoo-bin -d tu_base_de_datos -u account_global_tax
```

## 📋 Checklist de Desinstalación

### Antes
- ✅ Copia de seguridad de BD
- ✅ Notificación a usuarios
- ✅ Descarga de datos importantes
- ✅ Documentación de cambios

### Durante
- ✅ Detener Odoo
- ✅ Eliminar módulo
- ✅ Reiniciar servidor

### Después
- ✅ Verificar que Odoo funciona
- ✅ Confirmar que los documentos existen
- ✅ Revisar logs para errores
- ✅ Notificar a usuarios

## 🆘 Problemas Comunes

### "Error: Cannot uninstall module"
**Solución:**
```
1. Ve a Configuración → Modelos
2. Busca modelos del módulo
3. Verifica que no haya dependencias
4. Reintenta desinstalar
```

### "Error: Table does not exist"
**Solución:**
```
1. El módulo ya fue eliminado de la BD
2. Esto es normal en migraciones
3. Continúa con la reinstalación si es necesario
```

### "Warning: Unfinished records"
**Solución:**
```
1. Algunos cambios pendientes en la BD
2. Ejecuta una "Actualización" del módulo
3. Espera a que complete
4. Reintenta
```

## 🔐 Consideraciones de Seguridad

### Antes de Eliminar
- Asegúrate de que solo administradores acceden
- Verifica que no hay procesos en ejecución
- Realiza backup de logs importantes

### Datos Sensibles
- Los impuestos aplicados se pierden
- Las relaciones de documentos se eliminan
- El chatter conserva registros históricos

## 📞 Soporte en Problemas

Si encuentras problemas durante desinstalación:

1. **Revisa los logs:**
   ```bash
   tail -n 100 /var/log/odoo/odoo-server.log
   ```

2. **Verifica la BD:**
   ```bash
   psql -U odoo -d tu_base_de_datos -l
   ```

3. **Contacta soporte** si persisten los problemas

---

**Versión:** 16.0.4.0.0
**Fecha:** 2026-10-01
**Licencia:** AGPL-3
