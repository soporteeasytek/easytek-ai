# Linear API Setup

Este documento describe cómo configurar el acceso a la API de Linear.app para el skill `linear` de OpenClaw.

## 1. Obtener tu API Key Personal

1.  Ve a tu cuenta de Linear.app en el navegador.
2.  Haz clic en tu **Avatar** (esquina inferior izquierda).
3.  Selecciona **Settings**.
4.  En el menú lateral, ve a **API**.
5.  Haz clic en **Personal API Keys**.
6.  Haz clic en **Generate new API key**.
7.  Copia la clave generada.

**¡Importante!** Guarda esta clave en un lugar seguro. No la compartas con nadie y trátala como una contraseña.

## 2. Guardar el API Key en 1Password

Para máxima seguridad, el API Key de Linear se debe guardar en 1Password.

1.  Abre 1Password.
2.  Crea un nuevo item de tipo **Contraseña** o **API Credential**.
3.  Asigna un nombre claro, por ejemplo: `Linear.app API Key - EasyTEK`.
4.  En el campo de `contraseña` o `credential`, pega el API Key que generaste.
5.  Guarda el item en tu vault `Personal` (o el que Isaac indique).

## 3. Configurar el archivo `.linear.env`

Para que OpenClaw pueda acceder al API Key, debes guardarlo en un archivo `.env` local. Este archivo **no debe ser versionado en git**.

1.  En el directorio `/Users/isaacmora/.openclaw/workspace/`, crea un archivo llamado `.linear.env` (si no existe).
2.  Abre `.linear.env` con un editor de texto.
3.  Añade la siguiente línea, reemplazando `TU_API_KEY_DE_LINEAR` con el valor real que obtuviste de 1Password:
    ```
    LINEAR_API_KEY=TU_API_KEY_DE_LINEAR
    ```

    **Ejemplo (no usar este valor):**
    ```
    LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxxxxxxxx
    ```

4.  Guarda el archivo.

Ahora, el script `linear.py` podrá leer el `LINEAR_API_KEY` desde este archivo `.linear.env` o desde una variable de entorno `LINEAR_API_KEY`.

## 4. Obtener IDs de Equipos, Estados y Tipos de Issue

Linear utiliza IDs internos para equipos, estados de flujo de trabajo y tipos de issues. Para facilitar la operación, este skill intentará resolverlos por nombre, pero es útil conocerlos directamente.

Puedes usar el propio script `linear.py` para listar esta información. Por ejemplo:

**Listar equipos:**
```bash
python3 skills/linear/scripts/linear.py list-teams
```

**Listar estados de workflow:**
```bash
python3 skills/linear/scripts/linear.py list-workflow-states
```

**Listar tipos de issue:**
```bash
python3 skills/linear/scripts/linear.py list-issue-types
```

Estos comandos te darán los IDs y nombres exactos que puedes usar en los argumentos del skill.
