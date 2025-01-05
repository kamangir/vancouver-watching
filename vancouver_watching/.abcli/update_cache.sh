#! /usr/bin/env bash

function vancouver_watching_update_cache() {
    local options=$1
    local area=$(abcli_option "$options" area vancouver)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_overwrite=$(abcli_option_int "$options" overwrite 0)
    local do_process=$(abcli_option_int "$options" process 0)
    local do_publish=$(abcli_option_int "$options" publish $(abcli_not $do_dryrun))
    local do_refresh=$(abcli_option_int "$options" refresh 0)
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local object_name=$(abcli_mlflow_tags get \
        vancouver_watching \
        --tag cache)
    if [[ -z "$object_name" ]] || [[ "$do_refresh" == 1 ]]; then
        object_name=vanwatch-cache-$(abcli_string_timestamp)

        abcli_clone \
            - \
            vanwatch-QGIS-template-v5 \
            $object_name

        [[ "$do_dryrun" == 0 ]] &&
            abcli_mlflow_tags set \
                vancouver_watching \
                cache=$object_name
    fi
    abcli_log "cache: $object_name"

    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    mkdir -pv $object_path

    local published_object_name
    for published_object_name in $(abcli_mlflow_tags search \
        app=vancouver_watching,area=$area,stage=ingest,published \
        --log 0 \
        --delim space); do

        local local_filename=$object_path/$published_object_name.geojson
        abcli_log "🌀 $published_object_name"
        [[ -f "$local_filename" ]] && [[ "$do_overwrite" == 0 ]] && continue

        [[ "$do_dryrun" == 1 ]] && continue

        if [[ "$do_process" == 1 ]]; then
            vancouver_watching_process publish $published_object_name
        else
            abcli_download \
                filename=$area.geojson \
                $published_object_name
        fi

        cp -v \
            $ABCLI_OBJECT_ROOT/$published_object_name/$area.geojson \
            $local_filename
    done

    abcli_eval - \
        python3 -m vancouver_watching.cache \
        update \
        --object_name $object_name \
        "${@:2}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    [[ "$do_publish" == 1 ]] &&
        abcli_publish \
            ~download,tar \
            $object_name

    return $status
}