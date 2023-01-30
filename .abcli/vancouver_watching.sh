#! /usr/bin/env bash

function vanwatch() {
    vancouver_watching $@
}

function vancouver_watching() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ] ; then
        vancouver_watching_discover $@
        vancouver_watching_ingest $@
        vancouver_watching_list $@
        vancouver_watching_train $@

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m vancouver_watching --help
        fi
        return
    fi

    local function_name=vancouver_watching_$task
    if [[ $(type -t $function_name) == "function" ]] ; then
        $function_name "${@:2}"
        return
    fi

    abcli_log_error "-vancouver_watching: $task: command not found."
}