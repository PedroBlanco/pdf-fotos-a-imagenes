from PIL import Image

from autocrop import Background, MultiPartImage


def test_autocrop_deskew_accepts_rotated_photo_on_python3() -> None:
    page = Image.new("RGB", (600, 600), "white")
    photo = Image.new("RGB", (280, 200), (35, 70, 105))
    rotated = photo.rotate(7, expand=True, fillcolor="white")
    try:
        page.paste(rotated, (140, 170))
        scan = MultiPartImage(
            page,
            Background(),
            dpi=72,
            precision=12,
            deskew=True,
            contrast=15,
            shrink=0,
        )
        extracted = list(scan)
        try:
            assert len(extracted) == 1
            assert extracted[0].width > 150
            assert extracted[0].height > 100
        finally:
            for image in extracted:
                image.close()
    finally:
        rotated.close()
        photo.close()
        page.close()
