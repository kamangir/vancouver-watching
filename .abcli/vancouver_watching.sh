#! /usr/bin/env bash

function vanwatch() {
    vancouver_watching $@
}

function vancouver_watching() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ] ; then
        vancouver_watching_ingest $@

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m vancouver_watching --help
        fi
        return
    fi

    if [[ $(type -t vancouver_watching_$task) == "function" ]] ; then
        vancouver_watching_$task ${@:2}
        return
    fi

    abcli_log_error "-vancouver_watching: $task: command not found."
}