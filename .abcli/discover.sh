#! /usr/bin/env bash

function vancouver_watching_discover() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vanwatch discover$ABCUL<area>$ABCUL[push]" \
            "discover <area>."

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m vancouver_watching.discover --help
        fi
        return
    fi

    local area=$1

    local options=$2
    local do_push=$(abcli_option_int "$options" push 0)

    local function_name=vancouver_watching_discover_$area
    if [[ $(type -t $function_name) != "function" ]] ; then
        abcli_log_error "-vancouver_watching: discover: $area: area not found."
        return
    fi

    abcli_log "discovering $area [$options]"

    abcli_select
    $function_name ${@:2}

    cp -v \
        $abcli_object_path/$area.geojson \
        $abcli_path_git/Vancouver-Watching/areas/

    if [ "$do_push" == 1 ] ; then
        abcli_git push \
            Vancouver-Watching \
            accept_no_issue
    fi
}

abcli_source_path \
    $abcli_path_git/Vancouver-Watching/.abcli/discovery \
    log