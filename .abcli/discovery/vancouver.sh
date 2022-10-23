#! /usr/bin/env bash

function vancouver_watching_discover_vancouver() {
    curl \
        https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/download/?format=geojson \
        > $abcli_object_path/vancouver.geojson

    python3 -m vancouver_watching.discover \
        digest_geojson \
        --filename $abcli_object_path/vancouver.geojson \
        --prefix https://trafficcams.vancouver.ca/ \
        $@
}