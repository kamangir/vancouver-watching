#! /usr/bin/env bash

function vancouver_watching_ingest() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vancouver_watching ingest$ABCUL<area>$ABCUL[upload]" \
            "ingest <area>."

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m vancouver_watching.ingest --help
        fi
        return
    fi
    local area=$1

    local options=$2
    local do_upload=$(abcli_option_int "$options" upload 0)

    local discovery_object=$(\
        abcli_tag search \
        $area,vancouver_watching,discovery \
        --count 1 \
        --log 0)
    if [ -z "$discovery_object" ] ; then
        abcli_log_error "-vancouver_watching: ingest: $area: area not found."
        return
    fi

    abcli_download $discovery_object

    abcli_select

    cp -v \
        $abcli_object_root/$discovery_object/$area.geojson \
        $abcli_object_path/
    
    python3 -m vancouver_watching.ingest \
        from_cameras \
        --filename $abcli_object_path/$area.geojson

    abcli_tag set \
        $abcli_object_name \
        $area,vancouver_watching,ingest

    if [ "$do_upload" == 1 ] ; then
        abcli_upload
    fi
}