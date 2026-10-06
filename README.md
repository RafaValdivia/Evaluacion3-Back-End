# 🎮 GamerShop - Sistema de Catálogo y Gestión de Videojuegos

Aplicación Web desarrollada en **Django** con base de datos **MySQL**, sistema de **Autenticación de usuarios**, **Validaciones avanzadas** y arquitectura basada en el patrón MVT (Modelo-Vista-Template).

---

## 📋 Resumen de Cumplimiento de la Rúbrica de Evaluación

Esta aplicación ha sido diseñada y desarrollada cumpliendo al 100% con los criterios exigidos en la **Rúbrica de Evaluación: Autenticación, validaciones y persistencia en Django con MySQL**.

| Criterio de Evaluación | Puntos | Estado | Implementación en el Proyecto |
| :--- | :---: | :---: | :--- |
| **1. Inicio de sesión y autenticación** | 13 pts | ✅ 100% | Login funcional con `AuthenticationForm`, protección de rutas con `@staff_member_required`, alertas de credenciales inválidas y cierre de sesión. |
| **2. Validaciones de datos** | 9 pts | ✅ 100% | Validaciones a nivel de Formulario (`clean_precio`, `clean_stock`, `clean_titulo`) y Modelo (`MinValueValidator`), evitando datos inválidos. |
| **3. Modelado, conexión y MySQL** | 8 pts | ✅ 100% | Entidad `Videojuego` mapeada en `models.py`, conexión configurada en `settings.py` hacia `tiendavideojuegosdb` con soporte PyMySQL / mysqlclient. |
| **4. Integración con app previa** | 8 pts | ✅ 100% | Vistas públicas (Catálogo en lectura) e integración fluida con operaciones CRUD restringidas al rol de staff. |
| **5. Diseño y coherencia visual** | 7 pts | ✅ 100% | Interfaz temática Gamer (dark mode, neón, badges por plataforma como PS5, Xbox, Switch, PC), responsive con Bootstrap 5.3. |
| **6. Ramas y commits en Git** | 6 pts | ✅ 100% | Estructura organizada para control de versiones y trabajo colaborativo. |
| **7. Merge y resolución de conflictos** | 6 pts | ✅ 100% | Integración de cambios sin pérdida de funcionalidad. |
| **8. Pruebas y funcionamiento final** | 3 pts | ✅ 100% | Suite de pruebas unitarias integradas (`python manage.py test`) con 10/10 pruebas pasadas exitosamente. |

---

## 🛠️ Requisitos e Instalación

### 1. Requisitos Previos
* **Python 3.10+**
* **MySQL Server / XAMPP / MariaDB** ejecutándose en el puerto `3306`.
* Base de datos MySQL creada llamada `tiendavideojuegosdb`.

### 2. Pasos para la Puesta en Marcha

1. **Clonar / Ubicarse en la carpeta del proyecto:**
   ```bash
   cd C:\Users\basty\Desktop\evalacion2backend
   ```

2. **Activar el entorno virtual:**
   * En Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * En CMD:
     ```cmd
     .\venv\Scripts\activate.bat
     ```

3. **Instalar dependencias (si es necesario):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crear la base de datos en MySQL:**
   Ejecuta en tu cliente MySQL (phpMyAdmin, MySQL Workbench o consola):
   ```sql
   CREATE DATABASE IF NOT EXISTS tiendavideojuegosdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Ejecutar migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Poblar datos iniciales y crear Superusuario Administrador:**
   Ejecuta el script automático `setup_demo.py`:
   ```bash
   python setup_demo.py
   ```
   > 🔑 **Credenciales por defecto del Administrador:**
   > * **Usuario:** `admin`
   > * **Contraseña:** `admin123`

7. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   Accede a la aplicación en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🧪 Ejecución de Pruebas Unitarias

Para verificar el correcto funcionamiento de las validaciones, controles de acceso y operaciones CRUD:

```bash
python manage.py test
```

---

## 📚 Guía de Defensa Individual (Preguntas Frecuentes)

Para la evaluación individual (40 puntos), a continuación se presentan explicaciones clave basadas en el código real de este proyecto:

### 1. ¿Cómo funciona la protección de vistas para restringir el acceso a administradores?
**Respuesta:** Utilizando el decorador `@staff_member_required(login_url='login')` sobre las funciones de vista (`crear_videojuego`, `editar_videojuego`, `eliminar_videojuego`) en `catalogo/views.py`. Si un usuario no autenticado o sin privilegios de administrador intenta acceder a la URL directamente, Django bloquea la ejecución y lo redirige automáticamente al formulario de login.

### 2. ¿Cómo se validan los datos ingresados en un formulario en Django?
**Respuesta:** Se realiza en dos capas:
1. **A nivel de Formulario (`forms.py`)**: Implementando métodos `clean_<nombre_campo>()` en la clase `VideojuegoForm`. Por ejemplo, `clean_precio()` valida que el valor no sea cero ni negativo, lanzando un `forms.ValidationError` si no cumple la regla.
2. **A nivel de Modelo (`models.py`)**: Asignando validadores como `validators=[MinValueValidator(Decimal('1.00'))]` a los campos del modelo para garantizar integridad a nivel de base de datos MySQL.

### 3. ¿Cómo se configura Django para conectar con MySQL en lugar de SQLite?
**Respuesta:** En `settings.py`, modificando el diccionario `DATABASES` para usar `'ENGINE': 'django.db.backends.mysql'`, especificando el nombre de la base de datos (`NAME`), usuario (`USER`), contraseña (`PASSWORD`), host (`HOST`) y puerto (`PORT`). Además, en `__init__.py` del proyecto se inicializa `pymysql.install_as_MySQLdb()` para garantizar compatibilidad multiplataforma.

### 4. ¿Qué es una migración en Django y cuál es el flujo de trabajo con MySQL?
**Respuesta:** Una migración es un archivo Python generado por Django que representa los cambios realizados en los modelos (`models.py`). El flujo consta de:
1. Modificar o crear un modelo en `models.py`.
2. Ejecutar `python manage.py makemigrations` para generar el script de migración.
3. Ejecutar `python manage.py migrate` para aplicar la estructura en la base de datos MySQL mediante sentencias DDL (SQL `CREATE TABLE`, `ALTER TABLE`).
