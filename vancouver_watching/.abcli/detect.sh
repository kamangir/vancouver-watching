#! /usr/bin/env bash

function vancouver_watching_detect() {
    local options=$1
    local count=$(abcli_option "$options" count -1)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))
    local do_publish=$(abcli_option_int "$options" publish 0)
    local model_id=$(abcli_option "$options" model $VANWATCH_DEFAULT_MODEL)

    local object_name=$(abcli_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download - $object_name

    local target=$(abcli_mlflow_tags get \
        $object_name \
        --tag target)
    if [[ -z "$target" ]]; then
        abcli_log_error "vancouver_watching: detect: $object_name: target not found."
        return 1
    fi

    abcli_eval - \
        python3 -m vancouver_watching.target \
        detect \
        --do_dryrun $do_dryrun \
        --animated_gif $(abcli_option_int "$options" gif 0) \
        --count $count \
        --model_id $model_id \
        --geojson $ABCLI_OBJECT_ROOT/$object_name/detections.geojson \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    [[ "$do_publish" == 1 ]] &&
        abcli_publish - $object_name

    return $status
}
