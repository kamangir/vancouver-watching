import os

from bluer_objects import file, README
from bluer_options.help.functions import get_help

from vancouver_watching import NAME, VERSION, ICON, REPO_NAME
from vancouver_watching.discover.targets import list_of_targets
from vancouver_watching.help.functions import help_functions


items = README.Items(
    [
        {
            "name": target.title(),
            "marquee": f"https://github.com/kamangir/assets/blob/main/vanwatch-ingest-{target}/vanwatch-ingest-{target}.gif?raw=true",
            "url": f"./vancouver_watching/docs/{target}.md",
        }
        for target in list_of_targets()
    ]
    + [
        {
            "name": "time-series",
            "marquee": "https://github.com/kamangir/assets/blob/main/vanwatch/2024-01-06-20-39-46-73614-QGIS.gif?raw=true",
            "url": "https://github.com/kamangir/assets/blob/main/vanwatch/2024-01-06-20-39-46-73614-QGIS.gif",
        },
    ]
)


def build():
    return all(
        README.build(
            items=readme.get("items", []),
            path=os.path.join(file.path(__file__), readme["path"]),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
            help_function=lambda tokens: get_help(
                tokens,
                help_functions,
                mono=True,
            ),
        )
        for readme in [
            {"items": items, "path": ".."},
        ]
        + [{"path": f"./docs/{target}.md"} for target in list_of_targets()]
    )
