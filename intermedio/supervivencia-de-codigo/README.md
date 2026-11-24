# ¿Cuánto tiempo sobrevive el código de tus agentes?

`survival.py` mide qué parte de lo que se escribe cada semana en un repositorio sigue viva con el paso de las
semanas. Lo explico en [carlostapia.cl](https://carlostapia.cl/es/notas/supervivencia-de-codigo-por-semana/).

Probado con Python 3.10 y git 2.45 (noviembre de 2026). No necesita nada más.

## Cómo funciona

Es una tabla de supervivencia: lo escrito cada semana es una **tanda**, y cada tanda se mira a distintas edades.

1. Una foto por semana: el último commit de cada domingo en la rama donde se integra el trabajo.
2. En cada foto, `git blame` dice qué commit escribió cada línea que sigue ahí.
3. `git log --numstat` dice cuántas líneas agregó cada commit.
4. Para cada tanda y cada foto: líneas vivas dividido por líneas agregadas.

Cada commit cuenta en la semana de su fecha de autor.

## Uso

```bash
python3 survival.py <repo> <rama> <desde AAAA-MM-DD> [--with-tests] [--exclude REGEX]
```

Antes de correrlo revisa tres cosas:

- **La rama.** La que recibe el trabajo día a día (`develop`, por ejemplo), no la que solo recibe releases. Si tu
  copia local está atrasada, haz `git fetch` y usa `origin/develop`.
- **Las extensiones** de `CODE`: agrega las de tu lenguaje si no están.
- **Qué es un test** en `TEST`: por defecto, carpetas `test/`, `tests/`, `__tests__/`, `spec/` y archivos
  `_test.`, `.test.`, `.spec.` o `Test.php`. Quedan fuera salvo que pases `--with-tests`.
- **Los archivos generados.** Un volcado de esquema o un cliente generado se reescriben enteros en cada cambio y
  hacen caer la supervivencia sin que nadie haya rehecho nada. Busca los archivos con más líneas agregadas
  (`git log --numstat`) y sácalos con `--exclude`, por ejemplo `--exclude 'database/schema/'`.

Con trece semanas y unos mil archivos tarda menos de tres minutos.

## Cómo leer la salida

Un CSV con una fila por semana:

```
week,lines,wk1,wk2,wk3,...
2026-08-24,5183,98.3%,95.4%,94.7%,...
```

- `week`: el lunes de la semana en que se escribió.
- `lines`: las líneas que agregó esa semana (en la última foto).
- `wk1`: qué parte seguía viva al cerrar esa semana; `wk2`, una semana después, y así hasta hoy.

Para comparar tandas, compáralas a la misma edad (todas en `wk4`, por ejemplo), no en la última columna: las
tandas recientes todavía no tuvieron tiempo de reescribirse.

## Lo que hay que saber antes de sacar conclusiones

- **Un solo porcentaje engaña.** Si sumas todo, el número sube cada vez que entra código nuevo.
- **La rama cambia el número.** La rama principal no cuenta lo que todavía no llega a un release.
- **Los tests pesan.** En mi caso fueron el 57% de las líneas agregadas. Mídelos aparte.
- **El autor de git** solo sirve para separar por agente si cada agente firma sus commits.
- **Una rama que se integra tarde** agrega líneas a una tanda vieja, así que la última tanda puede seguir creciendo.
- La supervivencia cuenta lo que nadie tuvo que reescribir. La calidad del código se mide aparte.

## Mi medición

En [`my-run/`](my-run/) está la salida del script sobre un repositorio de producción que escriben agentes,
rama de integración, del 24-ago al 22-nov-2026:

- `code.csv`: solo código, sin tests (`survival.py <repo> develop 2026-08-24`).
- `with-tests.csv`: lo mismo con `--with-tests`.

Lo que me dio: a las cuatro semanas, lo escrito en agosto y septiembre tenía entre 70% y 93% vivo, y lo escrito
desde octubre, entre 93% y 99%. Casi todo lo que se reescribe se reescribe en el primer mes. Si lo corres en tu
repositorio, me interesa comparar.
