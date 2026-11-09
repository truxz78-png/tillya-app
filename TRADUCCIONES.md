# Traducciones de Tillya

## Dónde están
- `src/i18n/keys.txt`: los textos en inglés, uno por línea.
- `src/i18n/<idioma>.txt`: la traducción de cada idioma, **en la misma línea** que su texto en inglés
  (pt, fr, de, it, zh-CN, ja, ko, ru, ar, hi, id, tr).
- `src/fix_es.json`: el español de la página. `legal-tr.js`: el español de Privacidad y Términos.
- Los idiomas que no tienen archivo usan el traductor de Google automáticamente.

## Corregir una traducción (simple)
1. Abrir `src/i18n/<idioma>.txt` y cambiar SOLO esa línea (no borrar ni añadir líneas).
2. En Termux: `cd ~/tillya-app && python3 src/build.py`
3. Subir: `git add src index.html && git commit -m "Fix <idioma> translation" && git push`

## Añadir un texto nuevo a la página
Añadir el texto en inglés al final de `keys.txt` y su traducción al final de CADA archivo de idioma
(y en `src/fix_es.json`), luego `python3 src/build.py`.

## Añadir un idioma nuevo
Copiar `keys.txt` como `src/i18n/<código>.txt` y traducir cada línea. El código debe ser el del menú 🌐.

## El robot (Actions → "Translation check")
Corre en cada cambio y los lunes. Falla (y llega un correo) si:
- falta una traducción o está vacía,
- se perdió la flecha ↗, un número o las palabras de búsqueda,
- un idioma con otro alfabeto quedó en inglés,
- `index.html` no se reconstruyó después de cambiar `src/`.
