#! /usr/bin/env bash

function vancouver_watching_discover_iran() {
    local object_path=$1

    python3 -m iran_watching \
        discover_cameras_iran_style \
        --filename $object_path/iran.geojson \
        "$@"
}
