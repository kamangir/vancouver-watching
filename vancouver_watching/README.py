import os

from bluer_objects import file, README

from vancouver_watching import NAME, VERSION, ICON, REPO_NAME


items = README.Items(
    [
        {
            "name": "example output",
            "marquee": "https://github.com/kamangir/assets/blob/main/vanwatch/2023-11-12-14-42-23-96479.gif?raw=true",
        },
        {
            "name": "time-series",
            "marquee": "https://github.com/kamangir/assets/blob/main/vanwatch/2024-01-06-20-39-46-73614-QGIS.gif?raw=true",
        },
    ]
)


def build():
    return README.build(
        items=items,
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
