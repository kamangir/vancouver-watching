#! /usr/bin/env bash

function vancouver_watching_discover_vancouver() {
    local options=$1
    local object_name=$2

    local object_path=$ABCLI_OBJECT_ROOT/$object_name

    curl \
        https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/download/?format=geojson \
        >$object_path/detections.geojson

    local count=$(bluer_ai_option_int "$options" count -1)

    bluer_ai_eval ,$options \
        python3 -m vancouver_watching.discover \
        vancouver \
        --object_name $object_name \
        --prefix https://trafficcams.vancouver.ca/ \
        --count $count \
        "${@:3}"
}
