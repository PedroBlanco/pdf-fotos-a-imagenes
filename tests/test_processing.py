from pathlib import Path

from PIL import Image, ImageDraw

from pdf_fotos_a_imagenes.processing import (
    ProcessingOptions,
    build_background,
    discover_pdfs,
    process_pdf,
)


def _page(rectangles: list[tuple[int, int, int, int]]) -> Image.Image:
    image = Image.new("RGB", (600, 800), "white")
    draw = ImageDraw.Draw(image)
    for rectangle in rectangles:
        draw.rectangle(rectangle, fill=(40, 60, 80))
    return image


def _write_test_pdf(path: Path) -> None:
    first = _page([(50, 60, 250, 260), (330, 350, 550, 600)])
    second = _page([(120, 150, 470, 550)])
    try:
        first.save(path, "PDF", save_all=True, append_images=[second], resolution=72.0)
    finally:
        first.close()
        second.close()


def test_discover_pdfs_accepts_files_and_directories(tmp_path: Path) -> None:
    first = tmp_path / "a.pdf"
    nested = tmp_path / "sub" / "b.PDF"
    nested.parent.mkdir()
    first.write_bytes(b"%PDF-placeholder")
    nested.write_bytes(b"%PDF-placeholder")

    result = discover_pdfs([tmp_path, first])

    assert result == [first.resolve(), nested.resolve()]


def test_process_pdf_renders_and_extracts_photos_in_memory(tmp_path: Path) -> None:
    source = tmp_path / "album.pdf"
    output = tmp_path / "salida"
    _write_test_pdf(source)

    options = ProcessingOptions(
        dpi=72,
        image_format="png",
        max_photos=4,
        precision=12,
        contrast=15,
        shrink=0,
        deskew=False,
        keep_pages=True,
    )
    background = build_background(None, options.dpi)

    result = process_pdf(source, output, options, background)

    assert result.pages == 2
    assert result.photos == 3
    assert result.warnings == ()
    assert (output / "album" / "p0001_f01.png").is_file()
    assert (output / "album" / "p0001_f02.png").is_file()
    assert (output / "album" / "p0002_f01.png").is_file()
    assert (output / "album" / "_paginas" / "p0001.png").is_file()
    assert (output / "album" / "_paginas" / "p0002.png").is_file()
