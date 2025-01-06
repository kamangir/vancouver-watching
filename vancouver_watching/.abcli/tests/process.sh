#! /usr/bin/env bash

function test_vancouver_watching_process() {
    local options=$1

    local object_name=test_vancouver_watching_process-$(abcli_string_timestamp_short)

    vancouver_watching ingest \
        target=vancouver,count=3,~upload,$2 \
        $object_name \
        ~process,$3
    [[ $? -ne 0 ]] && return 1

    vancouver_watching process \
        ~download,~upload,$4 \
        $object_name \
        "${@:5}"
}
