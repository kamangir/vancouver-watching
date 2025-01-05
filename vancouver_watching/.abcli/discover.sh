#! /usr/bin/env bash

function vancouver_watching_discover() {
    local options=$1
    local area=$(abcli_option "$options" area vancouver)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local object_name=$(abcli_clarify_object $2 $(abcli_string_timestamp))

    local function_name=vancouver_watching_discover_$area
    if [[ $(type -t $function_name) != "function" ]]; then
        abcli_log_error "vancouver_watching: discover: $area: area not found."
        return 1
    fi

    abcli_log "discovering $area -> $object_name"
    abcli_eval ,$options \
        $function_name \
        $ABCLI_OBJECT_ROOT/$object_name \
        "${@:3}"
    local status="$?"

    [[ "$do_upload" == 0 ]] && return

    abcli_mlflow_tags set \
        $object_name \
        app=vancouver_watching,area=$area,stage=discovery

    abcli_upload - $object_name

    return $status
}

abcli_source_caller_suffix_path /discovery
