#! /usr/bin/env bash

function vancouver_watching_discover_iran() {
    python3 -m iran_watching \
        discover_cameras_iran_style \
        --filename $abcli_object_path/iran.geojson \
        ${@:2}
}