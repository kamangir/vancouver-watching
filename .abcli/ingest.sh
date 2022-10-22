#! /usr/bin/env bash

function vancouver_watching_ingest() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vanwatch ingest$ABCUL<area>$ABCUL[upload]" \
            "ingest <area>."

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m vancouver_watching.ingest --help
        fi
        return
    fi
    local area=$1

    local geojson=$abcli_path_git/Vancouver-Watching/data/$area.json
    if [ ! -f "$geojson" ] ; then
        abcli_log_error "-vancouver_watching: ingest: $area: area not found."
        return
    fi

    local options=$2
    local do_upload=$(abcli_option_int "$options" upload 0)

    cp -v \
        $geojson \
        $abcli_object_path/$area.geojson
    
    python3 -m vancouver_watching.ingest \
        from_cameras \
        --filename $abcli_object_path/$area.geojson

    abcli_tag set \
        $abcli_object_name \
        $area,vanwatch,ingest

    if [ "$do_upload" == 1 ] ; then
        abcli_upload
    fi
}