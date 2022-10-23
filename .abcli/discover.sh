#! /usr/bin/env bash

function vancouver_watching_discover() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vancouver_watching discover$ABCUL<area>$ABCUL[~upload]$ABCUL[--validate 1]" \
            "discover <area>."
        return
    fi

    local area=$1

    local function_name=vancouver_watching_discover_$area
    if [[ $(type -t $function_name) != "function" ]] ; then
        abcli_log_error "-vancouver_watching: discover: $area: area not found."
        return
    fi

    local options=$2
    local do_upload=$(abcli_option_int "$options" upload 1)

    abcli_log "discovering $area [$options]"

    abcli_select
    $function_name ${@:2}

    if [ "$do_upload" == 0 ] ; then
        return
    fi

    abcli_upload

    abcli_tag set \
        $abcli_object_name \
        $area,vancouver_watching,discovery
}

abcli_source_path \
    $abcli_path_git/Vancouver-Watching/.abcli/discovery \
    log