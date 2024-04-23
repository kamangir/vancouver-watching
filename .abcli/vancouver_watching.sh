#! /usr/bin/env bash

function vanwatch() {
    vancouver_watching "$@"
}

function vancouver_watching() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        vancouver_watching_discover "$@"
        vancouver_watching_ingest "$@"
        vancouver_watching_list "$@"
        vancouver_watching_openai_cli_vision "$@"
        vancouver_watching_process "$@"

        local task
        for task in pylint pytest test; do
            vancouver_watching $task "$@"
        done

        vancouver_watching_update_cache "$@"

        $(abcli_keyword_is $2 verbose) &&
            python3 -m vancouver_watching --help
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

    if [[ "|pylint|pytest|test|" == *"|$task|"* ]]; then
        abcli_${task} plugin=vancouver_watching,$2 \
            "${@:3}"
        return
    fi

    if [ "$task" == "version" ]; then
        python3 -m vancouver_watching version "${@:2}"
        return
    fi

    python3 -m vancouver_watching \
        "$task" \
        "${@:2}"
}

abcli_source_path \
    $abcli_path_git/Vancouver-Watching/.abcli/tests

abcli_env dot load \
    plugin=Vancouver-Watching
abcli_env dot load \
    filename=vancouver_watching/config.env,plugin=Vancouver-Watching
