from typing import List

from blue_options.terminal import show_usage, xtra


args = [
    "[--detect_objects 0]",
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


def help_process(
    tokens: List[str],
    mono: bool,
) -> str:
    return show_usage(
        [
            "vanwatch",
            "process",
            f"[{options(mono)}]",
            "[.|<object-name>]",
        ]
        + args,
        "process <object-name>.",
        mono=mono,
    )
