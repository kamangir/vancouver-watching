#! /usr/bin/env bash

function vancouver_watching_discover_vancouver() {
    curl https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/download/?format=geojson > vancouver.geojson

    python3 -m vancouver_watching.discover \
        discover_cameras \
        --filename $abcli_object_path/vancouver.geojson
}