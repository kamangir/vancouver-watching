#! /usr/bin/env bash

function vancouver_watching_discover_toronto() {
    local options=$1
    local object_name=$2

    local object_path=$ABCLI_OBJECT_ROOT/$object_name

    curl \
        https://511on.ca/api/v2/get/cameras \
        >$object_path/detections.json

    local count=$(bluer_ai_option_int "$options" count -1)

    bluer_ai_eval ,$options \
        python3 -m vancouver_watching.discover \
        toronto \
        --object_name $object_name \
        --prefix https://511on.ca/map/Cctv/ \
        --count $count \
        "${@:3}"
}
