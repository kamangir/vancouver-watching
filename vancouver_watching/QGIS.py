import os
import numpy as np
from datetime import datetime
from tqdm import tqdm
from typing import Tuple
import matplotlib.pyplot as plt
import pandas as pd
import glob

from blueness import module
from blue_options import fullname
from blue_objects import file, objects
from blue_objects.metadata import post_to_object

from vancouver_watching import NAME, VERSION
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)


def label_of_camera(
    location_url,
    location_name,
    list_of_cameras,
):
    return '<a href="{}">{}</a><br/> {}'.format(
        location_url,
        location_name,
        f'<img src="{list_of_cameras[0]}">' if list_of_cameras else "camera not found.",
    )
