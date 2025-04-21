#! /usr/bin/env bash

function vancouver_watching_ingest() {
    local options=$1
    local target=$(bluer_ai_option "$options" target vancouver)
    local count=$(bluer_ai_option_int "$options" count -1)
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_download=$(bluer_ai_option_int "$options" download $(bluer_ai_not $do_dryrun))
    local do_upload=$(bluer_ai_option_int "$options" upload $(bluer_ai_not $do_dryrun))

    local object_name=$(bluer_ai_clarify_object $2 $target-ingest-$(bluer_ai_string_timestamp_short))
    local object_path=$ABCLI_OBJECT_ROOT/$object_name
    mkdir -pv $object_path

    local discovery_object=$(bluer_objects_mlflow_tags search \
        app=vancouver_watching,target=$target,stage=discovery \
        --count 1 \
        --log 0)
    if [ -z "$discovery_object" ]; then
        bluer_ai_log_error "vancouver_watching: ingest: $target: target not found."
        return 1
    fi

    [[ "$do_download" == 1 ]] &&
        bluer_objects_download - $discovery_object

    bluer_objects_clone \
        ~relate,~tags \
        $VANWATCH_QGIS_TEMPLATE \
        $object_name

    cp -v \
        $ABCLI_OBJECT_ROOT/$discovery_object/detections.geojson \
        $object_path/

    bluer_ai_eval - \
        python3 -m vancouver_watching.target \
        ingest \
        --count $count \
        --do_dryrun $do_dryrun \
        --geojson $object_path/detections.geojson
    local status="$?"

    bluer_objects_mlflow_tags set \
        $object_name \
        app=vancouver_watching,target=$target,stage=ingest

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    [[ "$status" -ne 0 ]] && return $status

    local detection_options=$3
    local do_detect=$(bluer_ai_option_int "$detection_options" detect 1)
    [[ "$do_detect" == 0 ]] && return $status

    vancouver_watching_detect \
        ~download,upload=$do_upload,$detection_options \
        $object_name \
        "${@:4}"
}
