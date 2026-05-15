================================================================================
                    GEMINI MESH - Orquestación de Chatbots
================================================================================

¿Qué es esto?
-------------
Es un proyecto para la materia Estructura de Árboles. Simula un sistema que 
administra varios chatbots usando listas dobles, colas y pilas hechas a mano. 
Los bots se guardan en archivos JSON y también hay un registro de errores.

Estructura de carpetas (lo que importa)
---------------------------------------
- main.py                 -> menú principal
- chatbot_manager.py      -> la lógica de los bots
- models.py               -> las listas, colas, pilas, nodos
- persistence.py          -> guardar y cargar los datos
- utils.py                -> encriptación simple y log de errores
- data/                   -> aquí se crean los .json
    - config.json
    - chatbots.json
- README.txt              -> este texto

Cómo hacerlo funcionar
----------------------
1. Tener Python 3.8 o más nuevo.
2. Abrir una terminal en la carpeta donde está todo esto.
3. Escribir: python main.py
4. Seguir el menú que aparece.

¿Qué se puede hacer?
--------------------
- Crear, listar o eliminar bots (cada bot tiene ID, nombre, modelo, API key 
  ofuscada, instrucción de sistema y temperatura).
- Seleccionar un bot y "chatear" con él (la conversación se guarda en una cola 
  de máximo 10 mensajes, así se simula la ventana de contexto).
- Cambiar la instrucción de sistema o la temperatura; antes de cambiar se 
  guarda el estado anterior en una pila, y luego se puede deshacer el cambio.
- Guardar todo en archivos JSON y que al iniciar el programa se cargue 
  automáticamente.
- Ver un registro (log) de los errores o eventos importantes que ocurren 
  (fecha, código y descripción).
- Todo se controla desde un menú de texto que no se rompe si el usuario 
  escribe algo mal.

Datos de prueba
---------------
Si no hay archivos de datos, al arrancar el programa se crean dos bots de 
ejemplo: "Asistente Académico" y "Bot Creativo". Así se puede probar sin 
tener que crear nada desde cero.

Nota sobre la API de Gemini
---------------------------
En este código no se llama a la API real porque no quiero poner claves. 
Las respuestas del chatbot son simuladas (se eligen al azar de un conjunto 
fijo), pero la estructura para integrar Gemini real está lista (solo habría 
que cambiar la función _simulate_gemini_response).

Para la entrega
---------------
Se entregan todos los archivos .py, la carpeta data (con sus .json) y este 
README.txt. Eso cumple con lo que pide el parcial: código del proyecto y 
archivos de texto.

Cualquier duda, me avisan. Espero que funcione todo.

================================================================================
