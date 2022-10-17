#! /usr/bin/env bash

function vanwatch() {
    watching_vancouver $@
}

function watching_vancouver() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ] ; then
        watching_vancouver_ingest $@

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m watching_vancouver --help
        fi
        return
    fi

    if [[ $(type -t watching_vancouver_$task) == "function" ]] ; then
        watching_vancouver_$task ${@:2}
        return
    fi

    abcli_log_error "-watching_vancouver: $task: command not found."
}