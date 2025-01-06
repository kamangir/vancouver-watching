#! /usr/bin/env bash

function test_vancouver_watching_help() {
    local options=$1

    local module
    for module in \
        "vancouver_watching detect" \
        "vancouver_watching discover" \
        "vancouver_watching ingest" \
        "vancouver_watching"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1
    done

    return 0
}
