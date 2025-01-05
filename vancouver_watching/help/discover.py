from typing import List

from blue_options.terminal import show_usage, xtra


def help_discover(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "".join(
        [
            "area=<area>",
            xtra(",dryrun,~upload", mono=mono),
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
        mono=mono,
    )
