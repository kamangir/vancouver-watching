#! /usr/bin/env bash

function vancouver_watching_discover() {
    local options=$1
    local area=$(abcli_option "$options" area vancouver)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_tag=$(abcli_option_int "$options" tag $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local object_name=$(abcli_clarify_object $2 $area-discover-$(abcli_string_timestamp_short))

    local function_name=vancouver_watching_discover_$area
    if [[ $(type -t $function_name) != "function" ]]; then
        abcli_log_error "vancouver_watching: discover: $area: area not found."
        return 1
    fi

    abcli_log "discovering $area -> $object_name"
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
            app=vancouver_watching,area=$area,stage=discovery

    return $status
}

abcli_source_caller_suffix_path /discovery
