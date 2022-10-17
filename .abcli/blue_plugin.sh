#! /usr/bin/env bash

function bp() {
    blue-plugin $@
}

function blue_plugin() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ] ; then
        abcli_show_usage "abct task_1" \
            "run abct task_1."

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m blue_plugin --help
        fi

        return
    fi

    if [[ $(type -t blue_plugin_$task) == "function" ]] ; then
        blue_plugin_$task ${@:2}
    fi

    if [ "$task" == "task_1" ] ; then
        python3 -m blue_plugin \
            task_1 \
            ${@:2}
        return
    fi

    abcli_log_error "-blue_plugin: $task: command not found."
}