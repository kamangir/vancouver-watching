from typing import List

from bluer_options.terminal import show_usage


def help_list_targets(
    tokens: List[str],
    mono: bool,
) -> str:
    args = [
        "[--delim +]",
    ]

    return show_usage(
        [
            "vanwatch",
            "list_targets",
        ]
        + args,
        "list targets.",
        mono=mono,
    )
