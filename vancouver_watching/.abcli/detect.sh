#! /usr/bin/env bash

function vancouver_watching_detect() {
    local options=$1
    local count=$(bluer_ai_option "$options" count -1)
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_download=$(bluer_ai_option_int "$options" download $(bluer_ai_not $do_dryrun))
    local do_upload=$(bluer_ai_option_int "$options" upload $(bluer_ai_not $do_dryrun))
    local model_id=$(bluer_ai_option "$options" model $VANWATCH_DEFAULT_MODEL)

    local object_name=$(bluer_ai_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        bluer_objects_download - $object_name

    local target=$(bluer_objects_mlflow_tags get \
        $object_name \
        --tag target)
    if [[ -z "$target" ]]; then
        bluer_ai_log_error "vancouver_watching: detect: $object_name: target not found."
        return 1
    fi

    bluer_ai_eval - \
        python3 -m vancouver_watching.target \
        detect \
        --do_dryrun $do_dryrun \
        --animated_gif $(bluer_ai_option_int "$options" gif 0) \
        --count $count \
        --model_id $model_id \
        --geojson $ABCLI_OBJECT_ROOT/$object_name/detections.geojson \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    return $status
}
