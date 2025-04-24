#! /usr/bin/env bash

function test_vancouver_watching_discover_ingest_and_detect() {
    local options=$1

    local object_name=test_vancouver_watching_discover-$(bluer_ai_string_timestamp_short)

    bluer_ai_eval ,$options \
        vancouver_watching \
        discover \
        target=vancouver,count=3,~upload \
        $object_name
    [[ $? -ne 0 ]] && return 1

    local object_name=test_vancouver_watching_discover_ingest_and_detect-$(bluer_ai_string_timestamp_short)

    vancouver_watching ingest \
        target=vancouver,count=3,~upload,$2 \
        $object_name \
        detect,gif,~download,$3 \
        "${@:4}"
}
