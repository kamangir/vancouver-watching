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
        abcli_init vancouver_watching "${@:2}"
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
