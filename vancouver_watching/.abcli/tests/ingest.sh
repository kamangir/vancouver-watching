#! /usr/bin/env bash

function test_vancouver_watching_ingest() {
    local options=$1

    local object_name=test_vancouver_watching_ingest_$(abcli_string_timestamp_short)

    vancouver_watching ingest \
        area=vancouver,~batch,count=3,gif,$2 \
        $object_name \
        "${@:3}"
    [[ $? -ne 0 ]] && return 1

    (
        cd $ABCLI_OBJECT_ROOT/$object_name
        mv -v \
            $object_name.gif \
            animation.gif
    )

    abcli_publish \
        as=test_vancouver_watching_ingest,~download,suffix=.gif \
        $object_name
}
