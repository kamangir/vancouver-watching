#! /usr/bin/env bash

function vancouver_watching_discover() {
    local options=$1
    local target=$(abcli_option "$options" target vancouver)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_tag=$(abcli_option_int "$options" tag $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local object_name=$(abcli_clarify_object $2 $target-discover-$(abcli_string_timestamp_short))

    local function_name=vancouver_watching_discover_$target
    if [[ $(type -t $function_name) != "function" ]]; then
        abcli_log_error "vancouver_watching: discover: $target: target not found."
        return 1
    fi

    abcli_clone \
        ~relate,~tags \
        $VANWATCH_QGIS_TEMPLATE \
        $object_name

    abcli_log "discovering $target -> $object_name"
    abcli_eval ,$options \
        $function_name \
        ,$options \
        $ABCLI_OBJECT_ROOT/$object_name \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    [[ "$status" -ne 0 ]] && return $status

    [[ "$do_tag" == 1 ]] &&
        abcli_mlflow_tags set \
            $object_name \
            app=vancouver_watching,target=$target,stage=discovery

    return $status
}

abcli_source_caller_suffix_path /discovery
