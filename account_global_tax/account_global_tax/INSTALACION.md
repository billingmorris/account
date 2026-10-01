# Guía de Instalación - Account Global Tax v16.0.4.0.0

## 📋 Requisitos

- Odoo 16.0 Community Edition
- Módulos base: `base`, `account`, `sale`, `purchase`
- Acceso de administrador

## 🔧 Instalación Paso a Paso

### Método 1: Instalación Manual (Recomendado)

**Paso 1: Preparar el archivo**
```bash
# Extrae el archivo tar.gz
tar -xzf account_global_tax_v16.tar.gz

# Verifica la estructura
ls -la account_global_tax/
```

**Paso 2: Copiar a la carpeta de addons**
```bash
# Copia el módulo a la carpeta de addons de Odoo
cp -r account_global_tax /path/to/odoo/addons/

# Ejemplo si Odoo está en /opt/odoo
cp -r account_global_tax /opt/odoo/addons/
```

**Paso 3: Reiniciar Odoo con actualización**
```bash
# Detén el servidor Odoo
sudo systemctl stop odoo

# Reinicia con actualización del módulo
sudo -u odoo /opt/odoo/odoo-bin -d tu_base_de_datos -u account_global_tax --logfile=/var/log/odoo/odoo-server.log &

# O si usas un script personalizado
./restart_odoo.sh tu_base_de_datos
```

**Paso 4: Verificar instalación**
- Accede a Odoo con credenciales de administrador
- Ve a Aplicaciones → Actualizar lista de aplicaciones
- Busca "Account Global Tax"
- Si aparece con estado "Instalado" ✅, la instalación fue exitosa

### Método 2: Instalación vía Interfaz Odoo

**Paso 1: Acceder como administrador**
- Inicia sesión en Odoo con usuario administrador

**Paso 2: Ir a Aplicaciones**
- Menú → Aplicaciones → Aplicaciones

**Paso 3: Actualizar lista**
- Click en el botón "Actualizar lista de aplicaciones"
- Espera a que se complete la actualización

**Paso 4: Buscar e instalar**
- En la barra de búsqueda, escribe "Account Global Tax"
- Haz click en el módulo para abrirlo
- Click en el botón "Instalar"
- Espera a que se complete (puede tomar 30-60 segundos)

**Paso 5: Verificar**
- El estado debe cambiar a "Instalado" (color verde)

## ✅ Verificar Instalación

### Desde la interfaz Odoo:

1. **Módulo instalado:**
   - Aplicaciones → Aplicaciones
   - Busca "Account Global Tax"
   - Estado: Instalado ✅

2. **Botón disponible:**
   - Ve a Contabilidad → Facturas de Cliente
   - Abre cualquier factura
   - Deberías ver un botón "Impuestos Globales" en la barra

3. **Permisos:**
   - Configuración → Usuarios → (tu usuario)
   - Verifica que esté en el grupo "Usuarios"

### Desde la terminal:

```bash
# Ver módulos instalados
./odoo-bin -d tu_base_de_datos --list-modules | grep global_tax

# Ver logs de instalación
tail -f /var/log/odoo/odoo-server.log
```

## 🐛 Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'account_global_tax'"
**Solución:**
- Verifica que el módulo esté en la carpeta de addons
- Reinicia el servidor Odoo
- Actualiza la lista de módulos en Odoo

### Problema: "No puedes ingresar a los registros 'Global Tax Configuration Wizard'"
**Solución:**
```
1. Ve a Configuración → Modelos
2. Busca "global.tax.wizard"
3. Verifica los permisos ACL
4. Asegúrate de que tu usuario esté en base.group_user
```

### Problema: El botón "Impuestos Globales" no aparece
**Solución:**
1. Recarga la página (Ctrl+F5)
2. Limpia la caché del navegador
3. Verifica que el módulo esté instalado
4. Reinicia el servidor Odoo

### Problema: Error "Select at least one sales tax first"
**Solución:**
- Selecciona al menos un impuesto en el wizard
- Verifica que el impuesto sea del tipo correcto (venta/compra)

### Problema: Los impuestos no se aplican después de hacer click
**Solución:**
1. Verifica los permisos del usuario
2. Revisa los logs del servidor: `tail -f /var/log/odoo/odoo-server.log`
3. Comprueba que las líneas del documento tengan productos

## 📊 Verificación de Base de Datos

Para verificar que las tablas fueron creadas correctamente:

```bash
# Conéctate a PostgreSQL
psql -U odoo -d tu_base_de_datos

# Verifica las tablas relacionales
\dt account_move_global_tax_rel
\dt sale_order_global_tax_rel
\dt purchase_order_global_tax_rel
\dt wizard_tax_rel

# Verifica la tabla del wizard
\dt global_tax_wizard
```

## 🔄 Actualizar el Módulo

Si necesitas actualizar a una versión más reciente:

```bash
# Detén Odoo
sudo systemctl stop odoo

# Reemplaza la carpeta del módulo
rm -rf /opt/odoo/addons/account_global_tax/
cp -r account_global_tax /opt/odoo/addons/

# Reinicia con actualización
sudo -u odoo /opt/odoo/odoo-bin -d tu_base_de_datos -u account_global_tax
```

## ⚙️ Configuración Post-Instalación

### 1. Verificar impuestos disponibles
- Ve a Contabilidad → Configuración → Impuestos
- Asegúrate de tener impuestos creados con tipo "Venta" y "Compra"

### 2. Asignar permisos
- Configuración → Usuarios
- Para cada usuario que vaya a usar el módulo:
  - Asegúrate de que esté en el grupo "Usuarios" (base.group_user)

### 3. (Opcional) Crear grupos personalizados
```xml
<!-- En tu propio módulo o archivo XML -->
<record id="group_account_global_tax_manager" model="res.groups">
    <field name="name">Global Tax Manager</field>
</record>
```

## 📞 Contacto y Soporte

Si encuentras problemas:
1. Revisa los logs del servidor
2. Verifica los requisitos del sistema
3. Contacta al administrador de Odoo

---

**Versión:** 16.0.4.0.0
**Fecha:** 2026-10-01
**Licencia:** AGPL-3
