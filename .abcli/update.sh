#! /usr/bin/env bash

function vancouver_watching_update() {
    vancouver_watching_update_cache "$@"
}

function vancouver_watching_update_cache() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="area=<area>,process,push,rm"
        abcli_show_usage "vanwatch update|update_cache [$options]" \
            "update QGIS cache."
        return
    fi

    local area=$(abcli_option "$options" area vancouver)
    local do_rm=$(abcli_option_int "$options" rm 0)
    local do_process=$(abcli_option_int "$options" process 0)
    local do_push=$(abcli_option_int "$options" push 0)

    [[ "$do_rm" == 1 ]] &&
        rm -v $abcli_path_git/Vancouver-Watching/QGIS/*.geojson

    local object_name
    for object_name in $(abcli_tag search \
        ingest,published,$area,vancouver_watching \
        --log 0 \
        --delim space); do

        if [[ "$do_process" == 1 ]]; then
            vancouver_watching_process publish $object_name
        else
            abcli_download \
                filename=$area.geojson \
                $object_name
        fi

        cp -v \
            $abcli_object_root/$object_name/$area.geojson \
            $abcli_path_git/Vancouver-Watching/QGIS/$object_name.geojson
    done

    abcli_eval - \
        python3 -m vancouver_watching.ingest \
        update_cache

    if [[ "$do_push" == 1 ]]; then
        abcli_git push \
            Vancouver-Watching \
            accept_no_issue \
            $(python3 -m vancouver_watching version)-$area
    else
        abcli_git Vancouver-Watching status
    fi
}
