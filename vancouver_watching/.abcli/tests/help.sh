#! /usr/bin/env bash

function test_vancouver_watching_help() {
    local options=$1

    local module
    for module in \
        "vanwatch detect" \
        "vanwatch discover" \
        "vanwatch ingest" \
        "vanwatch list_targets" \
        \
        "vanwatch"; do
        bluer_ai_eval ,$options \
            bluer_ai_help $module
        [[ $? -ne 0 ]] && return 1
    done

    return 0
}
