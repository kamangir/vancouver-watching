import os
from typing import List

from bluer_objects import file


def list_of_targets() -> List[str]:
    return sorted(
        [
            file.name(filename)
            for filename in file.list_of(
                os.path.join(
                    file.path(__file__),
                    "../.abcli/discovery/*.sh",
                )
            )
        ]
    )
