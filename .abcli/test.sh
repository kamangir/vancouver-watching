#! /usr/bin/env bash

function vancouver_watching_test() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "vancouver_watching test [dryrun,~ingest,~list,~process,upload]" \
            "test vancouver_watching."
        return
    fi

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local test_ingest=$(abcli_option_int "$options" ingest 1)
    local test_list=$(abcli_option_int "$options" list 1)
    local test_process=$(abcli_option_int "$options" process 1)
    local do_upload=$(abcli_option_int "$options" upload 0)

    if [ "$test_ingest" == 1 ]; then
        abcli_eval dryrun=$dryrun \
            vanwatch ingest \
            area=vancouver,count=3,upload=$do_upload
    fi

    if [ "$test_list" == 1 ]; then
        abcli_eval dryrun=$dryrun \
            vanwatch list area=vancouver,discovery

        abcli_eval dryrun=$dryrun \
            vanwatch list area=vancouver,ingest

        abcli_eval dryrun=$dryrun \
            vanwatch list areas
    fi

    if [ "$test_process" == 1 ]; then
        local ingest_object_name=$(abcli_timestamp)

        abcli_eval dryrun=$dryrun \
            vanwatch ingest \
            area=vancouver,count=3,~process,upload=$do_upload \
            $ingest_object_name

        abcli_eval dryrun=$dryrun \
            vanwatch process \
            upload=$do_upload \
            $ingest_object_name
    fi
}
