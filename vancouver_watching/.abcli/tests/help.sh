#! /usr/bin/env bash

function test_vancouver_watching_help() {
    local options=$1

    local module
    for module in \
        "vancouver_watching" \
        "vancouver_watching discover" \
        "vancouver_watching ingest" \
        "vancouver_watching list" \
        "vancouver_watching vision" \
        "vancouver_watching process" \
        "vancouver_watching update" \
        "vancouver_watching update_cache"; do
        abcli_eval ,$options \
            $module help
        [[ $? -ne 0 ]] && return 1
    done

    return 0
}
