"""Interfaz de línea de órdenes para extraer fotografías de PDF escaneados."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .processing import (
    ProcessingError,
    ProcessingOptions,
    build_background,
    discover_pdfs,
    process_pdf,
)


def build_parser() -> argparse.ArgumentParser:
    """Crea el analizador de argumentos de la aplicación."""
    parser = argparse.ArgumentParser(
        description=(
            "Extrae fotografías de PDF escaneados. Las páginas se renderizan directamente "
            "con PDFium y msaavedra/autocrop detecta, recorta y endereza las fotografías."
        )
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="PDF o directorios con PDF.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("fotos_extraidas"),
        help="Directorio raíz de salida (fotos_extraidas).",
    )
    parser.add_argument(
        "--background",
        type=Path,
        help=(
            "Imagen de un escaneo vacío para calibrar el fondo; si se omite se usa "
            "el fondo casi blanco predeterminado de autocrop."
        ),
    )
    parser.add_argument("--dpi", type=int, default=300, help="Resolución de renderizado (300).")
    parser.add_argument("--format", choices=("jpeg", "png"), default="jpeg")
    parser.add_argument("--jpeg-quality", type=int, default=95, metavar="1-100")
    parser.add_argument(
        "--max-photos",
        type=int,
        default=4,
        help="Máximo esperado de fotografías por página; solo genera avisos (4).",
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=50,
        help="Precisión de muestreo de autocrop (50).",
    )
    parser.add_argument(
        "--contrast",
        type=int,
        default=15,
        help="Tolerancia de contraste frente al fondo para autocrop (15).",
    )
    parser.add_argument(
        "--shrink",
        type=int,
        default=3,
        help="Píxeles adicionales que autocrop recorta tras enderezar (3).",
    )
    parser.add_argument(
        "--no-deskew",
        action="store_true",
        help="No corregir automáticamente el giro de las fotografías.",
    )
    parser.add_argument(
        "--keep-pages",
        action="store_true",
        help="Conserva en PNG las páginas renderizadas para revisión.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reemplaza la salida existente de cada documento.",
    )
    return parser


def cli(argv: Sequence[str] | None = None) -> int:
    """Ejecuta la aplicación y devuelve un código de salida."""
    args = build_parser().parse_args(argv)
    options = ProcessingOptions(
        dpi=args.dpi,
        image_format=args.format,
        jpeg_quality=args.jpeg_quality,
        max_photos=args.max_photos,
        precision=args.precision,
        contrast=args.contrast,
        shrink=args.shrink,
        deskew=not args.no_deskew,
        keep_pages=args.keep_pages,
        force=args.force,
    )

    try:
        pdfs = discover_pdfs(args.inputs)
        output_root = args.output.expanduser().resolve()
        output_root.mkdir(parents=True, exist_ok=True)
        background = build_background(args.background, options.dpi)

        total_pages = 0
        total_photos = 0
        for source in pdfs:
            print(f"Procesando: {source}")
            result = process_pdf(source, output_root, options, background)
            total_pages += result.pages
            total_photos += result.photos
            print(f"  {result.pages} página(s), {result.photos} fotografía(s).")
            for warning in result.warnings:
                print(f"  AVISO: {warning}", file=sys.stderr)

        print(
            f"Finalizado: {len(pdfs)} PDF, {total_pages} página(s), "
            f"{total_photos} fotografía(s)."
        )
        return 0
    except ProcessingError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


def main() -> int:
    """Punto de entrada convencional."""
    return cli()


if __name__ == "__main__":
    raise SystemExit(main())
