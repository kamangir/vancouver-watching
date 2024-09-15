import os
import os.path
from typing import List
import re
from collections import Counter
from tqdm import tqdm

from blue_objects import file, path
from blue_objects.graphics.gif import generate_animated_gif

from vancouver_watching.ai.classes import Ultralytics_API
from vancouver_watching.logger import logger


class Area:
    def __init__(
        self,
        map_filename: str,
        do_dryrun: bool = False,
        verbose: bool = False,
    ):
        self.map_filename = map_filename  # geojson file

        self.object_path = file.path(self.map_filename)
        self.object_name = path.name(self.object_path)
        success, self.gdf = file.load_geodataframe(self.map_filename)
        assert success

        self.do_dryrun = do_dryrun
        self.verbose = verbose

        self.metadata_filename = file.add_extension(self.map_filename, "json")
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

        success, self.metadata = file.load_json(
            self.metadata_filename, ignore_error=True
        )
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
        animated_gif: bool = False,
        count: int = -1,
        overwrite: bool = False,
    ) -> bool:
        logger.info(
            "{}.detect_objects({},model_id{},count={}{})".format(
                self.__class__.__name__,
                model_id,
                ",animated_gif" if animated_gif else "",
                count,
                ",overwrite" if overwrite else "",
            )
        )

        ultralytics_api = Ultralytics_API(
            model_id,
            self.do_dryrun,
            self.verbose,
        )

        list_of_images: List[str] = []
        counter: int = 0
        for mapid in tqdm(self.metadata):
            for filename, metadata in self.metadata[mapid]["cameras"].items():
                full_filename = os.path.join(self.object_path, filename)
                if not file.exists(full_filename):
                    continue

                if self.do_dryrun:
                    logger.info(full_filename)
                    continue

                if not overwrite and "inference" in metadata:
                    continue

                success, inference = ultralytics_api.infer(full_filename)
                if success:
                    metadata["inference"] = inference
                    list_of_images += [inference.get("render_filename", "")]

                    counter += 1
                    if count != -1 and counter >= count:
                        break
            if count != -1 and counter >= count:
                break

        if not self.save_metadata():
            return False

        return not animated_gif or generate_animated_gif(
            [filename for filename in list_of_images if filename],
            os.path.join(self.object_path, f"{self.object_name}.gif"),
            frame_duration=500,
        )

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
            return None

        output = folium.Map(
            location=self.gdf.unary_union.centroid.coords[0][::-1],
            zoom_start=zoom_start,
        )
        folium.GeoJson(self.gdf).add_to(output)

        return output

    def save_gdf(self) -> bool:
        return file.save_geojson(self.map_filename, self.gdf, log=True)

    def save_metadata(self) -> bool:
        return file.save_json(self.metadata_filename, self.metadata, log=True)

    def summarize(self) -> bool:
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
