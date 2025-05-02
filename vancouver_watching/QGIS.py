from typing import List


def label_of_camera(
    location_url: str,
    location_name: str,
    list_of_cameras: List[str],
) -> str:
    return '<a href="{}">{}</a><br/> {}'.format(
        location_url,
        location_name,
        f'<img src="{list_of_cameras[0]}">' if list_of_cameras else "camera not found.",
    )
