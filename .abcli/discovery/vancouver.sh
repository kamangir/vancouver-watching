#! /usr/bin/env bash

function vancouver_watching_discover_vancouver() {
    local object_path=$1

    curl \
        https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/download/?format=geojson \
        >$object_path/vancouver.geojson

    python3 -m vancouver_watching.discover \
        discover_cameras_vancouver_style \
        --filename $object_path/vancouver.geojson \
        --prefix https://trafficcams.vancouver.ca/ \
        "$@"
}
