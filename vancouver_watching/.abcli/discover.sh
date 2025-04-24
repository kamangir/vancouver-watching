#! /usr/bin/env bash

function vancouver_watching_discover() {
    local options=$1
    local target=$(bluer_ai_option "$options" target vancouver)
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_tag=$(bluer_ai_option_int "$options" tag $(bluer_ai_not $do_dryrun))
    local do_upload=$(bluer_ai_option_int "$options" upload $(bluer_ai_not $do_dryrun))

    local object_name=$(bluer_ai_clarify_object $2 $target-discover-$(bluer_ai_string_timestamp_short))

    local function_name=vancouver_watching_discover_$target
    if [[ $(type -t $function_name) != "function" ]]; then
        bluer_ai_log_error "vancouver_watching: discover: $target: target not found."
        return 1
    fi

    bluer_objects_clone \
        ~relate,~tags \
        $VANWATCH_QGIS_TEMPLATE \
        $object_name

    bluer_ai_log "discovering $target -> $object_name"
    bluer_ai_eval ,$options \
        $function_name \
        ,$options \
        $object_name \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        bluer_objects_upload - $object_name

    [[ "$status" -ne 0 ]] && return $status

    [[ "$do_tag" == 1 ]] &&
        bluer_objects_mlflow_tags set \
            $object_name \
            app=vancouver_watching,target=$target,stage=discovery

    return $status
}

bluer_ai_source_caller_suffix_path /discovery
