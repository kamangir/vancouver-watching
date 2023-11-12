import os
import os.path
import re
from collections import Counter
from tqdm import tqdm
from vancouver_watching.ai.classes import Ultralytics_API
from abcli import file, path
from abcli import logging
import logging

logger = logging.getLogger(__name__)


class Area(object):
    def __init__(
        self,
        map_filename: str,
        do_dryrun: bool = False,
        verbose: bool = False,
    ):
        import geopandas

        self.map_filename = map_filename  # geojson file

        self.object_path = file.path(self.map_filename)
        self.object_name = path.name(self.object_path)
        self.gdf = geopandas.read_file(self.map_filename)

        self.do_dryrun = do_dryrun
        self.verbose = verbose

        self.metadata_filename = file.set_extension(self.map_filename, "json")
        self.metadata = {}

        self.valid = True
        for column in "cameras,mapid".split(","):
            if column not in self.gdf.columns:
                self.valid = False
                logger.info(
                    "Invaid Area, missing {}: {}.".format(column, self.map_filename)
                )
                return

        logger.info(
            "{}: {} mapid(s) from {}.".format(
                self.__class__.__name__,
                len(self.gdf),
                self.map_filename,
            )
        )

        success, self.metadata = file.load_json(self.metadata_filename, civilized=True)
        if not success:
            logger.info("generating metadata: {}".format(self.metadata_filename))

            p = re.compile(
                "https?:\/\/([0-9.]+).\:([0-9.]+)\/webcapture.jpg.*.channel=([0-9.]+).*"
            )
            for _, row in tqdm(self.gdf.iterrows()):
                cameras = {}
                for url in row["cameras"].split(","):
                    matches = p.match(url)
                    if matches:
                        filename = (
                            f"{matches[1]}-{matches[2]}-{matches[3]}".replace(".", "-")
                            + ".jpg"
                        )
                    else:
                        filename = file.name_and_extension(url)

                    if file.extension(filename) not in "jpg,jpeg,png".split(","):
                        logger.error("bad url: {}.".format(url))
                        continue

                    cameras[filename] = {"url": url}

                self.metadata[row["mapid"]] = {"cameras": cameras}

            self.save_metadata()

    def detect_objects(
        self,
        model_id: str,
        overwrite: bool = False,
    ) -> bool:
        ultralytics_api = Ultralytics_API(
            model_id,
            self.do_dryrun,
            self.verbose,
        )

        for mapid in tqdm(self.metadata):
            for filename, metadata in self.metadata[mapid]["cameras"].items():
                full_filename = os.path.join(self.object_path, filename)
                if not file.exist(full_filename):
                    continue

                if self.do_dryrun:
                    logger.info(full_filename)
                    continue

                if not overwrite and "inference" in metadata:
                    continue

                success, metadata["inference"] = ultralytics_api.infer(full_filename)
                if not success:
                    break

        return self.save_metadata()

    def ingest(
        self,
        count: int,
    ) -> bool:
        logger.info("{}.ingest({})".format(self.__class__.__name__, count))
        counter = 0
        for mapid in tqdm(self.metadata):
            for filename, metadata in self.metadata[mapid]["cameras"].items():
                url = metadata["url"]

                if self.do_dryrun:
                    logger.info(url)
                elif not file.download(url, os.path.join(self.object_path, filename)):
                    logger.error("bad url: {}.".format(url))

                counter += 1
                if counter >= count and count != -1:
                    break
            if counter >= count and count != -1:
                break

        return True

    def on_map(
        self,
        zoom_start: int = 12,
    ):
        import folium

        if self.gdf.empty:
            return

        output = folium.Map(
            location=self.gdf.unary_union.centroid.coords[0][::-1],
            zoom_start=zoom_start,
        )
        folium.GeoJson(self.gdf).add_to(output)

        return output

    def save_gdf(self):
        return file.save_geojson(self.map_filename, self.gdf, log=True)

    def save_metadata(self):
        return file.save_json(self.metadata_filename, self.metadata, log=True)

    def summarize(self):
        all_things = {}
        for mapid in tqdm(self.metadata):
            detections = {}
            for metadata in self.metadata[mapid]["cameras"].values():
                if not "inference" in metadata:
                    continue

                for thing, count in Counter(
                    [thing["name"] for thing in metadata["inference"].get("data", {})]
                ).items():
                    detections[thing] = detections.get(thing, 0) + count

            for thing, count in detections.items():
                all_things[thing] = all_things.get(thing, 0) + count

                if thing not in self.gdf.columns:
                    self.gdf[thing] = 0
                    logger.info("+= {}".format(thing))

                self.gdf.loc[self.gdf["mapid"] == mapid, thing] += count

        logger.info(
            ", ".join(
                ["{}: {}".format(thing, count) for thing, count in all_things.items()]
            )
        )

        return self.save_gdf()
