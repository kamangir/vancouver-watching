#! /usr/bin/env bash

function vancouver_watching_list() {
    local task=$(abcli_unpack_keyword $1 areas)

    if [ $task == "help" ] ; then
        abcli_show_usage "vancouver_watching list <area>$ABCUL<discovery|ingest>" \
            "list <area>."
        abcli_show_usage "vancouver_watching list areas" \
            "list areas."
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

    local area=$(abcli_clarify_input $1)
    local stage=$(abcli_clarify_input $2 ingest)

    abcli_tag search \
        $area,vancouver_watching,$stage \
        ${@:3}

    return
}