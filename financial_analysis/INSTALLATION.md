# Guía de Instalación - Financial Analysis Module v16.0.1.0.0

## Requisitos Previos

### Sistema
- **SO**: Linux (Ubuntu 20.04+ recomendado) o CentOS 7+
- **Python**: 3.8+
- **PostgreSQL**: 12+ (recomendado 14)
- **Memoria RAM**: Mínimo 2GB
- **Espacio disco**: Mínimo 500MB disponibles

### Odoo
- **Versión**: Odoo 16 Community Edition
- **Estado**: Instalado y funcionando
- **Módulos base requeridos**:
  - `base`
  - `account` (Contabilidad)
  - `sale` (Ventas)
  - `purchase` (Compras)

## Verificar Requisitos

```bash
# Verificar versión de Odoo
odoo --version

# Verificar Python
python3 --version

# Verificar PostgreSQL
psql --version

# Conectar a base de datos Odoo
psql -U odoo -d <nombre_base_datos> -c "SELECT version();"
```

## Instalación Paso a Paso

### Opción A: Desde Interfaz Web (Más Fácil)

#### 1. Descargar Módulo

Obtener archivo `financial_analysis_odoo16_v1.0.tar.gz`

#### 2. Extraer en Directorio de Addons

```bash
# Ubicar directorio custom/addons de Odoo
cd /odoo16/custom/addons/

# Extraer archivo
tar -xzf financial_analysis_odoo16_v1.0.tar.gz

# Verificar que se creó carpeta
ls -la | grep financial_analysis
```

#### 3. Reiniciar Odoo

```bash
# Reiniciar servicio Odoo
sudo systemctl restart odoo

# Verificar que está ejecutándose
sudo systemctl status odoo
```

#### 4. Instalar Módulo desde Odoo

1. **Ir a**: Aplicaciones → Aplicaciones (menú superior derecho)
2. **Buscar**: "Financial Analysis"
3. **Clic**: Botón "Instalar"
4. **Confirmar**: Aceptar instalación
5. **Esperar**: Sistema actualiza base de datos

#### 5. Verificar Instalación

Después de instalar, debe aparecer en el menú:
- **Contabilidad → Análisis Financiero**

Si no aparece:
1. Ir a Aplicaciones
2. Clic en "Actualizar Lista de Aplicaciones"
3. Buscar nuevamente "Financial Analysis"

### Opción B: Desde Línea de Comandos

#### 1. Descargar y Extraer

```bash
# Ir a directorio de addons
cd /odoo16/custom/addons/

# Descargar (si está en git)
git clone <repository-url> financial_analysis

# O extraer desde tar.gz
tar -xzf financial_analysis_odoo16_v1.0.tar.gz

# Verificar
ls -la financial_analysis/
```

#### 2. Establecer Permisos Correctos

```bash
# El usuario odoo debe poder leer/escribir
sudo chown -R odoo:odoo financial_analysis/
chmod -R 750 financial_analysis/
```

#### 3. Reiniciar Odoo

```bash
sudo systemctl restart odoo
```

#### 4. Instalar Módulo

```bash
# Método con Odoo CLI
python3 /path/to/odoo/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d <database_name> \
  -i financial_analysis \
  --stop-after-init

# Verificar logs
tail -f /var/log/odoo/odoo-server.log
```

### Opción C: Instalación en Desarrollo

Para desarrolladores que quieren contribuir:

```bash
# Clonar repositorio
cd ~/projects/odoo16/addons
git clone <repository-url> financial_analysis
cd financial_analysis

# Crear rama de desarrollo
git checkout -b feature/my-feature

# Instalar dependencias (si aplica)
pip install -r requirements.txt

# Validar código
pylint financial_analysis/models/
```

## Configuración Post-Instalación

### 1. Verificar Permisos de Acceso

```bash
# Conectar a base de datos
psql -U odoo -d <database_name>

# Verificar tablas creadas
SELECT * FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'financial_%';

# Ver registros de ACL
SELECT * FROM ir_model_access 
WHERE model_id LIKE '%financial%';
```

### 2. Configurar Acceso de Usuarios

En Odoo, asignar grupos de seguridad:

1. **Ir a**: Configuración → Usuarios y Empresas → Usuarios
2. **Seleccionar usuario**
3. **Pestaña "Accesos"**
4. **Agregar grupo**: "Contabilidad / Usuario" mínimo
5. **Guardar**

### 3. Configurar Plan de Cuentas (IMPORTANTE)

El módulo requiere que las cuentas tengan códigos que siga esta estructura:

```
1xxx - Activos
  11xx - Circulantes (Caja 1101, Bancos 1105, CxC 1110, etc.)
  12xx - Fijos Tangibles
  13xx - Fijos Intangibles

2xxx - Pasivos
  21xx - Circulantes (Cxp 2110, Bancos 2115, etc.)
  22xx - Largo Plazo
  23xx - Diferidos

3xxx - Patrimonio
  31xx - Capital
  32xx - Utilidades

4xxx - Ingresos
  40xx - Ventas
  41xx - Servicios
  42xx - Otros

5xxx - Gastos Operacionales
  51xx - Administración
  52xx - Ventas

61xx - Costo de Ventas
```

**Verificar estructura:**

1. **Ir a**: Contabilidad → Configuración → Plan de Cuentas
2. **Revisar** que las cuentas tengan códigos 1xxx, 2xxx, etc.
3. **Si no**: Actualizar códigos de cuentas
4. **Guardar**

### 4. Crear Asientos Contables de Prueba (Opcional)

Para probar con datos:

```bash
# Script de prueba (opcional)
python3 -m odoo -c /etc/odoo/odoo.conf \
  -d <database_name> \
  --load-language=es_ES \
  -i financial_analysis
```

## Pruebas Post-Instalación

### Test 1: Acceder al Módulo

1. **Login** en Odoo con usuario contabilidad
2. **Ir a**: Contabilidad → Análisis Financiero
3. **Verificar**: Aparece menú con opciones:
   - Análisis Rápido
   - Todos los Análisis
   - Dashboard
   - Indicadores
   - Diagnósticos
   - Recomendaciones
   - Presupuesto vs Realidad

### Test 2: Crear Análisis Rápido

1. **Clic**: "Análisis Rápido"
2. **Completar**:
   - Tipo: Mensual
   - Período: Actual
   - Empresa: [Seleccionar]
3. **Clic**: "Crear y Analizar"
4. **Verificar**: Se crea análisis con datos

### Test 3: Revisar Indicadores

1. **En el formulario del análisis**, ir a pestaña "Indicadores Financieros"
2. **Verificar**: Debe mostrar lista de indicadores con valores
3. **Ejemplos**: Net Margin, ROE, Current Ratio, etc.

### Test 4: Ver Diagnósticos

1. **Pestaña**: "Diagnósticos"
2. **Verificar**: Mostrar diagnósticos automáticos si hay datos
3. **Nota**: Si no hay diagnósticos, es porque los indicadores están en niveles saludables

## Solución de Problemas

### Problema: "Módulo no aparece después de instalar"

**Solución:**
```bash
# 1. Actualizar lista de aplicaciones
# - Ir a Aplicaciones
# - Clic menú lateral: Actualizar Lista
# - Esperar 30 segundos

# 2. Si sigue sin aparecer, limpiar cache
psql -U odoo -d <database_name> -c "
  DELETE FROM ir_module_module WHERE name='financial_analysis';
  DELETE FROM ir_model WHERE model LIKE 'financial.%';
"

# 3. Reinstalar módulo
python3 /path/to/odoo/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d <database_name> \
  -i financial_analysis \
  --stop-after-init
```

### Problema: "Error de permisos" al instalar

**Solución:**
```bash
# Verificar propietario de directorio
ls -la /odoo16/custom/addons/financial_analysis/

# Si no es 'odoo', cambiar:
sudo chown -R odoo:odoo /odoo16/custom/addons/financial_analysis/
sudo chmod -R 755 /odoo16/custom/addons/financial_analysis/

# Reiniciar Odoo
sudo systemctl restart odoo
```

### Problema: "No hay datos" en análisis

**Causas posibles:**

1. **No hay asientos contables**:
   - Crear órdenes de venta
   - Confirmar órdenes
   - Generar facturas
   - Validar asientos contables

2. **Asientos no publicados**:
   ```bash
   psql -U odoo -d <database_name> -c "
     SELECT state FROM account_move WHERE id LIMIT 5;
   "
   ```
   Si dice 'draft', publicar en Odoo.

3. **Plan de cuentas incorrecto**:
   - Verificar que las cuentas tengan códigos 1xxx, 2xxx, etc.
   - Revisar estructura de cuentas

**Test de diagnóstico:**
```bash
# Conexión a BD
psql -U odoo -d <database_name>

# Contar asientos
SELECT COUNT(*) FROM account_move WHERE state='posted';

# Ver cuentas
SELECT code, name FROM account_account LIMIT 10;

# Ver saldos
SELECT code, debit, credit FROM account_move_line LIMIT 10;
```

### Problema: "Error de base de datos" durante instalación

**Solución:**
```bash
# 1. Verificar integridad de BD
psql -U odoo -d <database_name> -c "SELECT 1;"

# 2. Ver logs detallados
sudo tail -n 100 /var/log/odoo/odoo-server.log

# 3. Si hay bloqueos, reiniciar servicio
sudo systemctl stop odoo
sudo systemctl start odoo

# 4. Reintentar instalación
python3 /path/to/odoo/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d <database_name> \
  -i financial_analysis \
  --stop-after-init
```

### Problema: "Análisis se demora mucho"

**Optimizaciones:**
```bash
# 1. Indexar tablas de contabilidad
psql -U odoo -d <database_name> -c "
  CREATE INDEX idx_move_date ON account_move(date);
  CREATE INDEX idx_move_company ON account_move(company_id);
  CREATE INDEX idx_line_account ON account_move_line(account_id);
  ANALYZE;
"

# 2. Usar período más corto
# - En vez de año completo, usar mes/trimestre

# 3. Ejecutar en horario de bajo uso
# - Evitar análisis durante jornada laboral
```

## Actualización del Módulo

### De v1.0 → v1.1 (cuando esté disponible)

```bash
# 1. Respaldar base de datos
pg_dump -U odoo -d <database_name> > backup_before_v1.1.sql

# 2. Descargar nueva versión
cd /tmp
wget <url_v1.1>
tar -xzf financial_analysis_odoo16_v1.1.tar.gz

# 3. Reemplazar archivos
sudo cp -r financial_analysis /odoo16/custom/addons/
sudo chown -R odoo:odoo /odoo16/custom/addons/financial_analysis/

# 4. Reiniciar y actualizar
sudo systemctl restart odoo

# En Odoo:
# - Ir a Aplicaciones
# - Buscar "Financial Analysis"
# - Clic en el módulo
# - Clic "Actualizar"

# 5. Verificar
# - Ir a Análisis Financiero
# - Crear análisis nuevo
# - Verificar que funciona
```

## Desinstalación

Si necesitas desinstalar el módulo:

```bash
# OPCIÓN 1: Desde Odoo
# 1. Ir a Aplicaciones
# 2. Buscar "Financial Analysis"
# 3. Clic en módulo
# 4. Clic "Desinstalar"
# 5. Confirmar

# OPCIÓN 2: Desde línea de comandos
python3 /path/to/odoo/odoo-bin \
  -c /etc/odoo/odoo.conf \
  -d <database_name> \
  -r financial_analysis \
  --stop-after-init

# OPCIÓN 3: Borrar archivos
sudo rm -rf /odoo16/custom/addons/financial_analysis/
sudo systemctl restart odoo
```

## Validación de Instalación Exitosa

Ejecutar este checklist:

- [ ] Módulo aparece en Aplicaciones
- [ ] Menú "Análisis Financiero" visible en Contabilidad
- [ ] Puedo acceder a "Análisis Rápido"
- [ ] Puedo crear nuevo análisis
- [ ] Indicadores se calculan correctamente
- [ ] Diagnósticos aparecen (si hay datos)
- [ ] Recomendaciones se generan
- [ ] Dashboard muestra gráficos
- [ ] Reporte PDF se puede generar
- [ ] Puedo asignar recomendaciones

## Soporte

Si tienes problemas durante la instalación:

1. **Verificar logs**:
   ```bash
   sudo tail -n 200 /var/log/odoo/odoo-server.log | grep -i financial
   ```

2. **Revisar base de datos**:
   ```bash
   psql -U odoo -d <database_name> -c "\dt financial*"
   ```

3. **Contactar soporte**:
   - Email: info@elmonitor.net
   - Incluir: Versión Odoo, logs, error exacto

## Próximos Pasos

Después de instalar:

1. **Crear primer análisis**: Menú → Análisis Rápido
2. **Leer resultados**: Entender indicadores y diagnósticos
3. **Implementar recomendaciones**: Ejecutar acciones sugeridas
4. **Monitorear cambios**: Crear análisis periódicos
5. **Personalizar**: Ajustar configuración según necesidades

---

**Para preguntas o problemas:** info@elmonitor.net
