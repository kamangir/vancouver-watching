#! /usr/bin/env bash

function test_vancouver_watching_process() {
    local options=$1

    local object_name=test_vancouver_watching_process-$(abcli_string_timestamp_short)

    vancouver_watching ingest \
        area=vancouver,~batch,count=3,~process,$2 \
        $object_name
    [[ $? -ne 0 ]] && return 1

    vancouver_watching process \
        ,$3 \
        $object_name \
        "${@:4}"
}
