#! /usr/bin/env bash

function vancouver_watching_discover_vancouver() {
    local options=$1
    local object_path=$2

    curl \
        https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/download/?format=geojson \
        >$object_path/detections.geojson

    local count=$(abcli_option_int "$options" count -1)

    abcli_eval ,$options \
        python3 -m vancouver_watching.discover \
        discover_cameras_vancouver_style \
        --filename $object_path/detections.geojson \
        --prefix https://trafficcams.vancouver.ca/ \
        --count $count \
        "${@:3}"
}
