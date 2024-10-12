#! /usr/bin/env bash

function vancouver_watching_discover() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="area=<area>,~upload"
        abcli_show_usage "vanwatch discover$ABCUL[$options]$ABCUL[-|<object-name>]$ABCUL[<args>]" \
            "discover area -> <object-name>."
        return
    fi

    local area=$(abcli_option "$options" area vancouver)
    local do_upload=$(abcli_option_int "$options" upload 1)

    local object_name=$(abcli_clarify_object $2 $(abcli_string_timestamp))

    local function_name=vancouver_watching_discover_$area
    if [[ $(type -t $function_name) != "function" ]]; then
        abcli_log_error "-vancouver_watching: discover: $area: area not found."
        return
    fi

    abcli_log "discovering $area -> $object_name"
    $function_name \
        $ABCLI_OBJECT_ROOT/$object_name \
        "${@:3}"

    [[ "$do_upload" == 0 ]] && return

    abcli_tags set \
        $object_name \
        $area,vancouver_watching,discovery

    abcli_upload - $object_name
}

abcli_source_caller_suffix_path /discovery
