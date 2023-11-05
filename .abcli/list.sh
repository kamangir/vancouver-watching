#! /usr/bin/env bash

function vancouver_watching_list() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="area=$(vancouver_watching_list_of_areas \|),discovery|ingest"
        abcli_show_usage "vancouver_watching list [$options]" \
            "list objects from area."
        abcli_show_usage "vancouver_watching list areas" \
            "list areas."
        return
    fi

    if [ $(abcli_option_int "$options" areas 0) == 1 ]; then
        abcli_log_list \
            "$(vancouver_watching_list_of_areas ,)" \
            , "area(s)"
        return
    fi

    local area=$(abcli_option "$options" area vancouver)
    local stage=$(abcli_option_choice "$options" discovery,ingest ingest)

    abcli_log "$area: $stage"
    abcli_tag search \
        $area,vancouver_watching,$stage \
        "${@:3}"
}

function vancouver_watching_list_of_areas() {
    python3 -m vancouver_watching.discover list_of_areas --delim ${1:-,}
}
