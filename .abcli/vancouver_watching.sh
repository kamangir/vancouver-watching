#! /usr/bin/env bash

function vanwatch() {
    vancouver_watching "$@"
}

function vancouver_watching() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        vancouver_watching version \\n

        vancouver_watching_conda "$@"
        vancouver_watching_discover "$@"
        vancouver_watching_ingest "$@"
        vancouver_watching_list "$@"
        vancouver_watching_process "$@"

        vancouver_watching update_QGIS "$@"

        vancouver_watching_test "$@"

        if [ "$(abcli_keyword_is $2 verbose)" == true ]; then
            python3 -m vancouver_watching --help
        fi
        return
    fi

    local function_name=vancouver_watching_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    if [ "$task" == "init" ]; then
        abcli_init Vancouver_Watching "${@:2}"
        conda activate Vancouver-Watching
        return
    fi

    if [ "$task" == "pytest" ]; then
        abcli_pytest plugin=Vancouver-Watching,$2 \
            "${@:3}"
        return
    fi

    if [ "$task" == "update_QGIS" ]; then
        local options=$2

        if [ $(abcli_option_int "$options" help 0) == 1 ]; then
            local options="area=<area>,process,push,rm"
            abcli_show_usage "vanwatch update_QGIS [$options]" \
                "update <area> in QGIS."
            return
        fi

        local area=$(abcli_option "$options" area vancouver)
        local do_rm=$(abcli_option_int "$options" rm 0)
        local do_process=$(abcli_option_int "$options" process 0)
        local do_push=$(abcli_option_int "$options" push 0)

        [[ "$do_rm" == 1 ]] &&
            rm -v $abcli_path_git/Vancouver-Watching/QGIS/*.geojson

        local object_name
        for object_name in $(abcli_tag search \
            ingest,published,$area,vancouver_watching \
            --log 0 \
            --delim space); do

            if [[ "$do_process" == 1 ]]; then
                vancouver_watching_process publish $object_name
            else
                abcli_download object $object_name $area.geojson
            fi

            cp -v \
                $abcli_object_root/$object_name/$area.geojson \
                $abcli_path_git/Vancouver-Watching/QGIS/$object_name.geojson
        done

        if [[ "$do_push" == 1 ]]; then
            abcli_git push \
                Vancouver-Watching \
                accept_no_issue \
                $(python3 -m vancouver_watching version)-$area
        else
            abcli_git Vancouver-Watching status
        fi

        return
    fi

    if [ "$task" == "version" ]; then
        abcli_log "🌈 $(python3 -m vancouver_watching version --show_description 1)${@:2}"
        return
    fi

    python3 -m vancouver_watching \
        "$task" \
        "${@:2}"
}
