from typing import List

from blue_options.terminal import show_usage

from vancouver_watching.help.discover import area_details


def help_update_cache(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "area=<area>,dryrun,overwrite,process,~publish,refresh,~upload"

    args = [
        "[--verbose 1]",
    ]

    return show_usage(
        [
            "vanwatch",
            "update_cache",
            f"[{options}]",
        ]
        + args,
        "update QGIS cache.",
        area_details,
        mono=mono,
    )
