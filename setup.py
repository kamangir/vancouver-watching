from vancouver_watching import NAME, VERSION, DESCRIPTION
from blueness.pypi import setup

setup(
    filename=__file__,
    repo_name="Vancouver-Watching",
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    packages=[NAME],
    package_data={
        NAME: ["config.env"],
    },
)
