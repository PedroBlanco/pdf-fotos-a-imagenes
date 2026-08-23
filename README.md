# pdf-fotos-a-imagenes

Herramienta FOSS en Python para extraer fotografías individuales de documentos PDF escaneados.
Está pensada especialmente para páginas con fondo blanco, entre una y cuatro fotografías separadas,
márgenes visibles y posibles giros producidos al colocarlas manualmente en el escáner.

## Funcionamiento

El procesamiento se realiza íntegramente desde Python:

1. `pypdfium2` abre el PDF multipágina y renderiza cada página directamente en memoria.
2. `msaavedra/autocrop`, integrado en `src/autocrop`, localiza las fotografías dentro de la página.
3. `autocrop` recorta cada fotografía y, de forma predeterminada, corrige su inclinación.
4. Las fotografías se guardan como JPEG o PNG.

No se necesita PDFtk, Poppler, ImageMagick, Ghostscript ni ningún otro ejecutable PDF externo.

## Requisitos

- Python 3.11 o posterior.
- Dependencias Python declaradas en `pyproject.toml`:
  - `pypdfium2` para renderizar PDF mediante PDFium.
  - Pillow para las imágenes.
  - NumPy, requerido por `autocrop`.

`pypdfium2` publica wheels para las plataformas habituales, por lo que el mismo código está pensado
para Windows, Linux y macOS.

`pyproject.toml` es la fuente de verdad de las dependencias. `requirements.txt` contiene `.` para
permitir también la instalación convencional con `pip -r` sin duplicar versiones.

## Instalación

Desde una copia del repositorio:

```bash
python -m venv .venv
```

Activación en Linux/macOS:

```bash
source .venv/bin/activate
```

Activación en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalación recomendada:

```bash
python -m pip install .
```

Instalación equivalente mediante `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Para desarrollo:

```bash
python -m pip install -e ".[dev]"
```

## Uso básico

Un PDF:

```bash
pdf-fotos-a-imagenes album.pdf
```

Varios PDF:

```bash
pdf-fotos-a-imagenes album1.pdf album2.pdf
```

Todos los PDF de uno o varios directorios, incluyendo subdirectorios:

```bash
pdf-fotos-a-imagenes escaneos/ otros-escaneos/
```

Directorio de salida personalizado:

```bash
pdf-fotos-a-imagenes escaneos/ -o fotos
```

La salida usa una carpeta por PDF:

```text
fotos_extraidas/
└── album/
    ├── p0001_f01.jpg
    ├── p0001_f02.jpg
    ├── p0002_f01.jpg
    └── p0002_f02.jpg
```

## Ajustes útiles

Los valores predeterminados están orientados al caso de fotografías separadas sobre fondo blanco:

```text
--dpi 300
--max-photos 4
--precision 50
--contrast 15
--shrink 3
```

Opciones principales:

- `--format jpeg|png`: formato de las fotografías extraídas.
- `--jpeg-quality 1-100`: calidad JPEG; valor predeterminado 95.
- `--background imagen.png`: usa un escaneo vacío para calibrar el fondo real del escáner.
- `--no-deskew`: desactiva la corrección automática del giro.
- `--keep-pages`: conserva las páginas renderizadas como PNG para facilitar la revisión.
- `--force`: reemplaza la salida existente de ese documento.
- `--precision`, `--contrast` y `--shrink`: permiten ajustar la detección de `autocrop`.

Ayuda completa:

```bash
pdf-fotos-a-imagenes --help
```

## Calidad de imagen

El PDF se renderiza directamente con PDFium a la resolución indicada por `--dpi`. No existe una
conversión previa a PDF de una página ni un JPEG temporal. Las páginas solo se guardan si se solicita
`--keep-pages`, y en ese caso se conservan como PNG.

Si el PDF original contiene una imagen del escáner a una resolución concreta, conviene utilizar un
`--dpi` acorde con la resolución de digitalización para evitar un remuestreo innecesariamente grande.

## `msaavedra/autocrop`

El paquete `autocrop` incluido en `src/autocrop` deriva de:

- https://github.com/msaavedra/autocrop
- commit `87992d775133109ad57c01d31e417df539e04dd8`

Se han aplicado adaptaciones mínimas para Python 3/Pillow moderno y se ha eliminado el dibujo de
marcas de depuración sobre la imagen fuente. La procedencia y modificaciones se indican en los
archivos afectados y en `THIRD_PARTY_NOTICES.md`.

## Comprobaciones

Linux/macOS:

```bash
./scripts/check.sh
./scripts/security.sh
```

PowerShell:

```powershell
./scripts/check.ps1
./scripts/security.ps1
```

Las pruebas incluyen un PDF multipágina sintético que recorre el flujo completo de renderizado y
extracción, además de una prueba específica de corrección de giro.

## Licencia

Este proyecto se distribuye bajo **GNU GPL v3, exclusivamente (`GPL-3.0-only`)**, de forma coherente
con la integración de `msaavedra/autocrop`, que también está publicado bajo GPLv3.

Consulte `LICENSE` y `THIRD_PARTY_NOTICES.md`.
