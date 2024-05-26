#! /usr/bin/env bash

function test_vancouver_watching_process() {
    local options=$1

    local ingest_object_name=ingest-$(abcli_string_timestamp)

    abcli_eval ,$options \
        vanwatch ingest \
        area=vancouver,~batch,count=3,~process,$2 \
        $ingest_object_name

    abcli_eval ,$options \
        vanwatch process \
        ,$3 \
        $ingest_object_name \
        "${@:4}"
}
