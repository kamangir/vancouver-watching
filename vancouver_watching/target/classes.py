from tqdm import tqdm

from blue_objects import file, path
from blue_geo.file import load_geodataframe, save_geojson

from vancouver_watching.logger import logger


class Target:
    def __init__(
        self,
        map_filename: str,
        do_dryrun: bool = False,
        verbose: bool = False,
    ):
        self.map_filename = map_filename  # geojson file

        self.object_path = file.path(self.map_filename)
        self.object_name = path.name(self.object_path)
        success, self.gdf = load_geodataframe(self.map_filename)
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
                    "Invalid target: {} not found in {}.".format(
                        column, self.map_filename
                    )
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
            self.metadata_filename,
            ignore_error=True,
        )
        if not success:
            logger.info("generating metadata: {}".format(self.metadata_filename))

            for _, row in tqdm(self.gdf.iterrows()):
                cameras = {}
                for url in row["cameras"].split(","):
                    filename = file.name_and_extension(url)

                    if file.extension(filename) not in "jpg,jpeg,png".split(","):
                        logger.error("bad url: {}.".format(url))
                        continue

                    cameras[filename] = {"url": url}

                self.metadata[row["mapid"]] = {"cameras": cameras}

            self.save_metadata()

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
        return save_geojson(
            self.map_filename,
            self.gdf,
            log=True,
        )

    def save_metadata(self) -> bool:
        return file.save_json(
            self.metadata_filename,
            self.metadata,
            log=True,
        )
