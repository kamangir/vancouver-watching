#! /usr/bin/env bash

function vancouver_watching_list() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="area=<area>,discovery|ingest,published"
        abcli_show_usage "vanwatch list [$options]$ABCUL$abcli_tag_search_args" \
            "list objects from area."

        abcli_log_list "$(vancouver_watching_list_of_areas)" , "area(s)"

        abcli_show_usage "vanwatch list areas" \
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
    local do_published=$(abcli_option_int "$options" published 0)

    local tags=$area,vancouver_watching,$stage
    [[ "$do_published" == 1 ]] && local tags="$tags,published"

    abcli_tag search $tags "${@:2}"
}

function vancouver_watching_list_of_areas() {
    python3 -m vancouver_watching.discover list_of_areas --delim ${1:-,}
}
