from tqdm import tqdm
import geopandas as gpd
from shapely.geometry import Point

from blueness import module
from bluer_objects import objects
from bluer_objects.file import load_json
from bluer_objects.metadata import post_to_object
from bluer_geo.file import save_geojson

from vancouver_watching import NAME
from vancouver_watching.QGIS import label_of_camera
from vancouver_watching.logger import logger

NAME = module.name(__file__, NAME)


# https://511on.ca/help/endpoint/cameras
def toronto(
    object_name: str,
    prefix: str,
    count: int = -1,
) -> bool:
    logger.info(
        "{}.discover({}{}) -> {}".format(
            NAME,
            prefix,
            "" if count == -1 else f"count={count}",
            object_name,
        )
    )

    success, list_of_cameras_raw = load_json(
        objects.path_of(
            object_name=object_name,
            filename="detections.json",
        )
    )
    if not success:
        return False

    camera_count = 0
    records = []
    for row in tqdm(list_of_cameras_raw):
        list_of_cameras_ = [view["Url"] for view in row["Views"]]
        camera_count += len(list_of_cameras_)

        records.append(
            {
                "cameras": ",".join(list_of_cameras_),
                "geometry": Point(row["Longitude"], row["Latitude"]),
                "label": label_of_camera(
                    "#",
                    row["Location"],
                    list_of_cameras_,
                ),
                "mapid": row["SourceId"],
            }
        )

        if count != -1 and len(records) >= count:
            break

    gdf = gpd.GeoDataFrame(
        records,
        geometry="geometry",
        crs="EPSG:4326",
    )

    logger.info(
        "found {} camera(s) in {} location(s).".format(
            camera_count,
            len(gdf),
        )
    )

    if not save_geojson(
        objects.path_of(
            object_name=object_name,
            filename="detections.geojson",
        ),
        gdf,
    ):
        return False

    return post_to_object(
        object_name,
        "discovery",
        {
            "target": "toronto",
            "cameras": camera_count,
            "locations": len(gdf),
        },
    )
