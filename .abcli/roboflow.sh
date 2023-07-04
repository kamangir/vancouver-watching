#! /usr/bin/env bash

function vancouver_watching_roboflow() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vancouver_watching roboflow export$ABCUL[project=<project-name>]$ABCUL<object-name>" \
            "<project-name> -> <object-name>."
        abcli_show_usage "vancouver_watching roboflow import$ABCUL[project=<project-name>]$ABCUL<object-name>" \
            "<object-name> -> <project-name>."
        abcli_show_usage "vancouver_watching roboflow install$ABCUL" \
            "install roboflow."
        return
    fi

    if [ "$task" == "export " ] ; then
        abcli_log "wip"
        return
    fi

    if [ "$task" == "import " ] ; then
        abcli_log "wip"
        return
    fi

    if [ "$task" == "install" ] ; then
        pip3 install roboflow
        return
    fi

    abcli_log_error "-vancouver_watching: roboflow: $task: command not found."
    return 1
}