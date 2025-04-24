from typing import List

from bluer_ai.host import signature as bluer_ai_signature

from vancouver_watching import fullname


def signature() -> List[str]:
    return [
        fullname(),
    ] + bluer_ai_signature()
