"""Procesamiento de PDF escaneados sin utilidades PDF externas."""

from __future__ import annotations

import shutil
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pypdfium2 as pdfium
from PIL import Image

from autocrop import Background, MultiPartImage


class ProcessingError(RuntimeError):
    """Error controlado durante el procesamiento de un documento."""


@dataclass(frozen=True)
class ProcessingOptions:
    """Parámetros del renderizado y de la detección de fotografías."""

    dpi: int = 300
    image_format: str = "jpeg"
    jpeg_quality: int = 95
    max_photos: int = 4
    precision: int = 50
    contrast: int = 15
    shrink: int = 3
    deskew: bool = True
    keep_pages: bool = False
    force: bool = False


@dataclass(frozen=True)
class ProcessingResult:
    """Resumen del procesamiento de un PDF."""

    source: Path
    pages: int
    photos: int
    warnings: tuple[str, ...]


def discover_pdfs(inputs: Sequence[Path]) -> list[Path]:
    """Devuelve PDF únicos a partir de archivos y directorios de entrada."""
    result: list[Path] = []
    seen: set[Path] = set()

    for item in inputs:
        expanded = item.expanduser()
        if expanded.is_dir():
            candidates: Iterable[Path] = sorted(
                (
                    path
                    for path in expanded.rglob("*")
                    if path.is_file() and path.suffix.lower() == ".pdf"
                ),
                key=lambda path: str(path).casefold(),
            )
        elif expanded.is_file() and expanded.suffix.lower() == ".pdf":
            candidates = [expanded]
        else:
            raise ProcessingError(f"No existe o no es un PDF/directorio válido: {item}")

        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                result.append(resolved)

    if not result:
        raise ProcessingError("No se encontraron documentos PDF para procesar.")
    return result


def validate_options(options: ProcessingOptions) -> None:
    """Valida los parámetros antes de abrir documentos."""
    if options.dpi < 72:
        raise ProcessingError("La resolución debe ser de al menos 72 dpi.")
    if options.image_format not in {"jpeg", "png"}:
        raise ProcessingError("El formato de salida debe ser 'jpeg' o 'png'.")
    if not 1 <= options.jpeg_quality <= 100:
        raise ProcessingError("La calidad JPEG debe estar entre 1 y 100.")
    if options.max_photos < 1:
        raise ProcessingError("El máximo esperado de fotografías debe ser al menos 1.")
    if options.precision < 1:
        raise ProcessingError("La precisión de autocrop debe ser al menos 1.")
    if options.contrast < 1:
        raise ProcessingError("El contraste de autocrop debe ser al menos 1.")
    if options.shrink < 0:
        raise ProcessingError("El recorte adicional de autocrop no puede ser negativo.")


def build_background(background_path: Path | None, dpi: int) -> Background:
    """Crea el modelo de fondo blanco o lo calibra con un escaneo vacío."""
    background = Background()
    if background_path is None:
        return background

    path = background_path.expanduser()
    if not path.is_file():
        raise ProcessingError(f"No existe la imagen de fondo: {background_path}")

    try:
        with Image.open(path) as image:
            background.load_from_image(image.convert("RGB"), dpi=dpi)
    except Exception as exc:
        raise ProcessingError(f"No se pudo analizar la imagen de fondo {path}: {exc}") from exc
    return background


def render_page(document: pdfium.PdfDocument, page_index: int, dpi: int) -> Image.Image:
    """Rasteriza una página PDF directamente en memoria y devuelve RGB."""
    page = document[page_index]
    bitmap = None
    try:
        bitmap = page.render(scale=dpi / 72.0)
        pil_image = cast(Image.Image, bitmap.to_pil())
        return pil_image.convert("RGB")
    except Exception as exc:
        raise ProcessingError(f"No se pudo rasterizar la página {page_index + 1}: {exc}") from exc
    finally:
        if bitmap is not None:
            bitmap.close()
        page.close()


def detect_photos(
    page_image: Image.Image,
    background: Background,
    options: ProcessingOptions,
) -> list[Image.Image]:
    """Detecta, recorta y opcionalmente endereza las fotografías de una página."""
    try:
        scan = MultiPartImage(
            page_image,
            background,
            dpi=options.dpi,
            precision=options.precision,
            deskew=options.deskew,
            contrast=options.contrast,
            shrink=options.shrink,
        )
        return [photo.convert("RGB") for photo in scan]
    except Exception as exc:
        raise ProcessingError(f"autocrop no pudo analizar la página: {exc}") from exc


def _save_photo(photo: Image.Image, target: Path, options: ProcessingOptions) -> None:
    if options.image_format == "jpeg":
        photo.save(
            target,
            "JPEG",
            quality=options.jpeg_quality,
            subsampling=0,
            optimize=True,
        )
    else:
        photo.save(target, "PNG", optimize=True)


def _prepare_document_output(source: Path, output_root: Path, force: bool) -> Path:
    target = output_root / source.stem
    if target.exists() and any(target.iterdir()):
        if not force:
            raise ProcessingError(
                f"El directorio de salida ya contiene datos: {target}. Use --force para reemplazarlo."
            )
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    return target


def process_pdf(
    source: Path,
    output_root: Path,
    options: ProcessingOptions,
    background: Background,
) -> ProcessingResult:
    """Renderiza y procesa todas las páginas de un PDF directamente con PDFium."""
    validate_options(options)
    document_output = _prepare_document_output(source, output_root, options.force)
    pages_output = document_output / "_paginas" if options.keep_pages else None
    if pages_output is not None:
        pages_output.mkdir(parents=True, exist_ok=True)

    warnings: list[str] = []
    total_photos = 0

    try:
        document = pdfium.PdfDocument(source)
    except Exception as exc:
        raise ProcessingError(f"No se pudo abrir {source}: {exc}") from exc

    try:
        page_count = len(document)
        if page_count == 0:
            raise ProcessingError(f"El PDF no contiene páginas: {source}")

        extension = "jpg" if options.image_format == "jpeg" else "png"
        for page_index in range(page_count):
            page_number = page_index + 1
            page_image = render_page(document, page_index, options.dpi)
            try:
                if pages_output is not None:
                    page_image.save(pages_output / f"p{page_number:04d}.png", "PNG")

                photos = detect_photos(page_image, background, options)
                count = len(photos)
                if count == 0:
                    warnings.append(f"Página {page_number}: no se detectaron fotografías.")
                elif count > options.max_photos:
                    warnings.append(
                        f"Página {page_number}: se detectaron {count} fotografías; "
                        f"se esperaban como máximo {options.max_photos}."
                    )

                for photo_number, photo in enumerate(photos, start=1):
                    try:
                        target = document_output / (
                            f"p{page_number:04d}_f{photo_number:02d}.{extension}"
                        )
                        _save_photo(photo, target, options)
                    finally:
                        photo.close()
                total_photos += count
            finally:
                page_image.close()
    finally:
        document.close()

    return ProcessingResult(
        source=source,
        pages=page_count,
        photos=total_photos,
        warnings=tuple(warnings),
    )
