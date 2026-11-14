# Agentes sin humo

Lo básico para trabajar con varios agentes de Claude Code a la vez, en la terminal. Sin interfaz gráfica, sin
paquetes de skills y sin frameworks: una pestaña por agente, uno que coordina y un repo git que guarda todo.

Es el paso uno de la serie *Agentes sin humo* de [carlostapia.cl](https://carlostapia.cl). Los comandos son de
Claude Code 2.1.325 (noviembre de 2026).

## 1. Una pestaña por agente, cada una con su nombre

Abre una pestaña de la terminal por agente y ponle nombre al abrir:

```bash
claude -n coordinador
claude -n revisor
claude -n editor
```

Si la sesión ya está abierta, adentro escribe `/rename revisor`. El nombre te dice en qué pestaña estás, y al
coordinador le dice a quién encargarle qué.

Empieza con dos o tres. Más agentes no es más trabajo hecho: cada uno hay que revisarlo.

## 2. Un repo aparte para el equipo

El trabajo del equipo vive en un repo git propio, separado del código. Ahí queda escrito qué se pidió, qué se
decidió y qué está hecho, aunque cierres todas las pestañas.

```bash
cp -r plantilla ~/equipo
cd ~/equipo && git init && git add -A && git commit -m "equipo"
```

```
equipo/
├── CLAUDE.md      las reglas que leen todos
├── tareas/        una tarea por archivo: tareas/revisor-001.md
├── decisiones/    lo que se decidió y por qué
└── hecho/         lo que cada uno terminó, con el commit o el archivo
```

Abre cada pestaña con acceso a ese repo además de tu proyecto:

```bash
claude -n revisor --add-dir ~/equipo
```

## 3. Le hablas a uno solo: el coordinador

Al coordinador le cuentas qué quieres. Él lo parte en tareas, escribe cada una en `tareas/` con el nombre del agente
y hace commit. Cuando un agente termina, deja su resumen en `hecho/` y el coordinador lo revisa.

Si tu Claude Code trae mensajes entre sesiones, el coordinador además les avisa por su nombre. Si no los trae, el repo
hace de buzón: cada agente mira `tareas/` cuando le dices «revisa tus tareas».

## 4. El contexto: autocompact

Cada mensaje y cada archivo llenan el contexto de la sesión. Al acercarse al límite, Claude Code resume la
conversación. Con `/autocompact` eliges qué tan lleno se pone antes de resumir. Lo importante no se pierde porque
está en el repo, no en la conversación.

## 5. Skills: de a una, cuando una tarea se repite

Al abrir, Claude Code carga solo la descripción de cada skill, y la skill entera cuando la usa. No instales un paquete
el primer día: cuando le expliques lo mismo a un agente por tercera vez, conviértelo en una skill.

```
.claude/skills/revisar-pr/SKILL.md
```

## 6. Desde el celular

¿Vas a salir? En la pestaña del coordinador escribe `/rc` (es `/remote-control`) y sigues esa sesión desde el
celular.

## Lo que no hace falta

- Una interfaz gráfica encima de la terminal.
- Un paquete de skills o de agentes que no escribiste tú.
- Diez agentes el primer día.

Licencia MIT.
