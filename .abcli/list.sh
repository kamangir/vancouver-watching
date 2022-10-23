#! /usr/bin/env bash

function vancouver_watching_list() {
    local task=$(abcli_unpack_keyword $1 areas)

    if [ $task == "help" ] ; then
        abcli_show_usage "vancouver_watching list areas" \
            "list areas."
        abcli_show_usage "vancouver_watching list area$ABCUL<area>$ABCUL<discovery|ingest>" \
            "list <area>."
        return
    fi

    if [ "$task" == "area" ] ; then
        local area=$(abcli_clarify_input $2)
        local stage=$(abcli_clarify_input $3 ingest)

        abcli_tag search \
            $area,vancouver_watching,$stage \
            ${@:3}

        return
    fi

    if [ "$task" == "areas" ] ; then
        pushd $abcli_path_git/Vancouver-Watching/.abcli/discovery > /dev/null
        local filename
        for filename in *.sh ; do
            abcli_log ${filename%.*}
        done
        popd > /dev/null
        return
    fi

    abcli_log_error "-vancouver_watching: $task: command not found."
}