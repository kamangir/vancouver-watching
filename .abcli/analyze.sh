#! /usr/bin/env bash

function vancouver_watching_analyze() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="~download,~upload"
        abcli_show_usage "vanwatch analyze$ABCUL[$options]$ABCUL[.|<object-name>]$ABCUL[<args>]" \
            "analyze <object-name>."
        return
    fi

    local do_download=$(abcli_option_int "$options" download 1)
    local do_upload=$(abcli_option_int "$options" upload 1)

    local object_name=$(abcli_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download object $object_name

    python3 -m vancouver_watching.analysis \
        analyze \
        --object_path $abcli_object_root/$object_name \
        "${@:3}"

    [[ "$do_upload" == 1 ]] &&
        abcli_upload object $object_name
}
