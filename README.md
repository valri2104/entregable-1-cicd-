# Entregable 1 – CI/CD: Introducción a Git, GitHub y GitHub Actions

## Integrantes

**Texto usado en `AUTOR`:** `Valeria Cardona Urrea`

| Nombre completo | Usuario de GitHub | Rol |
|---|---|---|
| Valeria Cardona Urrea | [@valri2104](https://github.com/valri2104) | Propietaria del repositorio (entrega individual) |

## Contenido del repositorio

- `.github/workflows/mi_workflow.yml`: workflow de GitHub Actions que imprime un saludo personalizado, la fecha/hora del runner y ejecuta el script de Python.
- `mi_script.py`: script de Python que imprime el autor, el sistema operativo del runner y la fecha/hora.
- `README.md`: este archivo, con las respuestas a las preguntas del taller.

## Ejecución exitosa del workflow

🔗 Enlace a la ejecución exitosa: https://github.com/valri2104/entregable-1-cicd-/actions/runs/42436497839

En los logs del job `imprimir_info` se ven el saludo ("Hola, soy Valeria Cardona Urrea y este es mi primer workflow!"), la fecha/hora del runner y la salida del script (`Autor: Valeria Cardona Urrea`, `Sistema Operativo: Linux ...` y la fecha/hora desde Python).

---

## Respuestas a las preguntas

### 1. ¿Qué eventos configuraste para disparar tu workflow y por qué?

Configuré dos eventos dentro de `on`:

- **`push`** (filtrado a la rama `main`): el workflow se ejecuta automáticamente cada vez que se suben cambios a `main`. Así cada cambio en la rama principal queda verificado sin que tenga que hacer nada manualmente; es la base de la integración continua.
- **`workflow_dispatch`**: permite ejecutar el workflow manualmente desde la pestaña *Actions* con el botón **Run workflow**. Es útil para volver a correrlo sin tener que hacer un commit nuevo (por ejemplo, para probarlo o demostrar que funciona).

### 2. ¿Qué sistema operativo utiliza el runner `ubuntu-latest` y por qué puede ejecutar tu workflow aunque tu computadora sea Windows o macOS? ¿Qué relación tiene el runner con el shell de los pasos `run`?

`ubuntu-latest` es una máquina virtual con **Linux (Ubuntu)**, en su versión estable más reciente soportada por GitHub. En los logs, el script de Python lo confirma imprimiendo `Sistema Operativo: Linux ...`.

Puede ejecutar mi workflow sin importar el sistema operativo de mi computadora porque **los jobs no se ejecutan en mi equipo**, sino en servidores de GitHub. Mi computadora solo sirve para editar los archivos y hacer `push`; GitHub crea una máquina limpia con Ubuntu, clona el repositorio y ejecuta allí los pasos. Por eso tampoco necesito tener Ubuntu ni Python instalados localmente.

El **runner determina el shell por defecto** de los pasos `run`: en Ubuntu y macOS es **Bash**, y en Windows es **PowerShell**. Como los comandos dependen del shell (por ejemplo, `$(date)` es sintaxis de Bash), si se cambia el runner los comandos podrían dejar de funcionar. Por eso en el paso del mensaje fijé explícitamente `shell: bash`.

### 3. Tres acciones pre-construidas del Marketplace (no mencionadas en el material)

1. **`actions/setup-node`**: instala y configura una versión específica de Node.js en el runner (y opcionalmente el caché de npm/yarn/pnpm). Sirve para compilar, probar o empaquetar proyectos de JavaScript/TypeScript.
2. **`actions/cache`**: guarda y restaura carpetas entre ejecuciones (por ejemplo, dependencias de `pip`, `npm` o `maven`) usando una clave. Sirve para que los workflows sean más rápidos al no descargar todo de nuevo en cada ejecución.
3. **`docker/build-push-action`**: construye imágenes de Docker (con Buildx) y las publica en un registro como Docker Hub o GitHub Container Registry. Sirve para empaquetar una aplicación en un contenedor como parte de un pipeline de entrega.
4. **`github/codeql-action`** (extra): ejecuta el análisis de seguridad CodeQL sobre el código y reporta vulnerabilidades en la pestaña *Security*. Sirve para detectar fallos de seguridad automáticamente en cada push o pull request.

### 4. ¿Qué es un secreto en GitHub Actions y para qué se usa? ¿Cómo lo usarías en tu workflow?

Un **secreto** es un valor sensible (contraseña, token, API key, credenciales de la nube) que se guarda **cifrado en la configuración del repositorio** y no dentro del código. Se usa para que el workflow pueda autenticarse en servicios externos sin exponer esas credenciales en el repositorio público. GitHub intenta ocultarlos (`***`) en los logs, pero no se deben imprimir.

Para usarlo en mi workflow:

1. Lo crearía en **Settings > Secrets and variables > Actions > New repository secret**, por ejemplo con el nombre `MI_API_KEY`.
2. Lo referenciaría en un paso con la expresión `${{ secrets.MI_API_KEY }}`, normalmente pasándolo como variable de entorno:

```yaml
- name: Llamar a un servicio externo
  env:
    API_KEY: ${{ secrets.MI_API_KEY }}
  run: python mi_script.py
```

Y en Python lo leería con `os.environ["API_KEY"]`, sin imprimirlo nunca. (Este taller no requiere secretos, por eso no lo incluí en el workflow entregado).

### 5. Reflexión: ¿qué tareas automatizarías en tu flujo de trabajo diario y por qué?

GitHub Actions me parece muy útil para quitarme tareas repetitivas y evitar errores humanos. Automatizaría:

- **Ejecutar las pruebas y un linter en cada push o pull request** (por ejemplo `pytest` y `flake8`). Así detecto errores apenas los subo, antes de que lleguen a `main`, y no dependo de acordarme de correr las pruebas localmente. Esto es especialmente valioso cuando trabajo en equipo, porque nadie puede integrar código roto sin que se note.
- **Desplegar automáticamente** un proyecto (por ejemplo, una página en GitHub Pages o una app en la nube) cuando se hace merge a `main`. Esto evita pasos manuales que se olvidan o se hacen distinto cada vez, y hace que lo publicado siempre corresponda a lo que está en el repositorio.
- **Tareas programadas con `schedule`**, como revisar dependencias desactualizadas o generar un reporte semanal, porque son cosas que se olvidan fácilmente si dependen de hacerlas a mano.

Esta misma experiencia lo demuestra: aunque no tenía computador disponible, el workflow corre igual en los servidores de GitHub, porque la automatización no depende de mi máquina.
