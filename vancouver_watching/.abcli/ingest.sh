#! /usr/bin/env bash

function vancouver_watching_ingest() {
    local options=$1
    local area=$(abcli_option "$options" area vancouver)
    local count=$(abcli_option_int "$options" count -1)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local object_name=$(abcli_clarify_object $2 $area-ingest-$(abcli_string_timestamp_short))
    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    mkdir -pv $object_path

    local discovery_object=$(abcli_mlflow_tags search \
        app=vancouver_watching,area=$area,stage=discovery \
        --count 1 \
        --log 0)
    if [ -z "$discovery_object" ]; then
        abcli_log_error "vancouver_watching: ingest: $area: area not found."
        return 1
    fi

    [[ "$do_download" == 1 ]] &&
        abcli_download - $discovery_object

    abcli_clone \
        ~relate,~tags \
        $VANWATCH_QGIS_TEMPLATE \
        $object_name

    cp -v \
        $ABCLI_OBJECT_ROOT/$discovery_object/detections.geojson \
        $object_path/

    abcli_eval - \
        python3 -m vancouver_watching.ingest \
        --count $count \
        --do_dryrun $do_dryrun \
        --geojson $object_path/detections.geojson
    local status="$?"

    abcli_mlflow_tags set \
        $object_name \
        app=vancouver_watching,area=$area,stage=ingest

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    [[ "$status" -ne 0 ]] && return $status

    local process_options=$3
    local do_process=$(abcli_option_int "$process_options" process 1)
    [[ "$do_process" == 0 ]] && return $status

    vancouver_watching_process \
        ~download,upload=$do_upload,$process_options \
        $object_name \
        "${@:4}"
}
