from typing import List

from blue_options.terminal import show_usage, xtra


args = [
    "[--overwrite 1]",
    "[--verbose 1]",
]


def options(mono: bool):
    return "".join(
        [
            xtra("count=<-1>,~download,dryrun,", mono=mono),
            "gif",
            xtra(",model=<model-id>,", mono=mono),
            "publish",
            xtra(",~upload", mono=mono),
        ]
    )


def help_detect(
    tokens: List[str],
    mono: bool,
) -> str:
    return show_usage(
        [
            "vanwatch",
            "detect",
            f"[{options(mono)}]",
            "[.|<object-name>]",
        ]
        + args,
        "detect objects in <object-name>.",
        mono=mono,
    )
