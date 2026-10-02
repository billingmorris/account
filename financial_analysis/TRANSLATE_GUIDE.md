# Guía de Traducciones - Financial Analysis Module

## ⚠️ IMPORTANTE: Cómo Cargar las Traducciones al Español

Las traducciones en Odoo 16 deben cargarse explícitamente. Hay varias opciones:

### Opción 1: Reinstalar el módulo con traducciones (RECOMENDADO)

Ejecuta esto desde la línea de comandos de tu servidor Odoo:

```bash
# Desactiva el módulo
./manage.py service.stop
cd /path/to/odoo

# Reinstala el módulo con traducciones
./odoo-bin -d nombre_db -c odoo.conf --i18n-import=./addons/financial_analysis/i18n/es_ES.po --i18n-overwrite -m financial_analysis --load-language=es_ES

# Inicia nuevamente
./manage.py service.start
```

O ejecuta desde la consola de Odoo:

```python
# En la consola de Odoo (manage shell o bin/bash -c "python manage shell")
from odoo import SUPERUSER_ID
from odoo.tools import trans_load

trans_load(cr, '/path/to/financial_analysis/i18n/es_ES.po', 'es_ES', module_name='financial_analysis')
cr.commit()
```

### Opción 2: Desde la interfaz de Odoo (Manual)

1. **Ir a:** Configuración → Traducciones → Cargar/Actualizar Traducciones
2. **Buscar:** Español (es_ES)
3. **Seleccionar:** financial_analysis
4. **Hacer clic:** "Cargar"
5. **Esperar:** A que termine la carga
6. **Recargar:** La página (F5 o Ctrl+R)

### Opción 3: Usando el comando de Odoo

```bash
cd /ruta/a/odoo
./odoo-bin -d tu_base_datos -c etc/odoo.conf --i18n-import=/ruta/a/financial_analysis/i18n/es_ES.po --load-language=es_ES
```

## Verificar que las traducciones se cargaron

1. Cambia tu usuario a idioma **Español (es_ES)**
2. Recarga la página
3. Verifica que los menús y campos aparezcan en español

## Archivos de traducción incluidos

- **es_ES.po**: Archivo de traducción fuente (editable)
- **es_ES.mo**: Archivo compilado (usado por Odoo)

## Contenido de las traducciones

Las traducciones incluyen:
- ✅ Menús y botones
- ✅ Campos de formularios  
- ✅ Opciones de análisis (Mensual, Trimestral, Semestral, Anual)
- ✅ Estados (Borrador, Completado, Revisado)
- ✅ Categorías de indicadores
- ✅ Mensajes del wizard

## Si las traducciones aún no aparecen

1. Limpia la caché de Odoo
2. Reinicia el servidor
3. Recarga el navegador completamente (Ctrl+Shift+R)

## Alternativa: Editar las cadenas manualmente

Si prefieres traducir manualmente desde Odoo:

1. Ir a: Configuración → Traducciones → Términos
2. Buscar las cadenas en inglés
3. Agregar las traducciones al español

---

**Nota**: Las traducciones se guardan en la base de datos una vez cargadas. No necesitas repetir este proceso.
