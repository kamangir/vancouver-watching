from typing import List

from blue_options.terminal import show_usage, xtra

from vancouver_watching.discover.functions import get_list_of_areas

area_details = {
    "area: {}".format(" | ".join(get_list_of_areas())): [],
}


def help_discover(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "area=<area>",
            xtra(",count=<-1>,dryrun,~tag,~upload", mono=mono),
        ]
    )

    return show_usage(
        [
            "vanwatch",
            "discover",
            f"[{options}]",
            "[-|<object-name>]",
            "[<args>]",
        ],
        "discover area -> <object-name>.",
        area_details,
        mono=mono,
    )
