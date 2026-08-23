from pathlib import Path

from pdf_fotos_a_imagenes.main import build_parser


def test_parser_uses_python_only_defaults() -> None:
    args = build_parser().parse_args(["entrada.pdf"])

    assert args.inputs == [Path("entrada.pdf")]
    assert args.dpi == 300
    assert args.format == "jpeg"
    assert args.max_photos == 4
    assert args.no_deskew is False
