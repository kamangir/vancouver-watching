#! /usr/bin/env bash

function test_vancouver_watching_process() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_upload=$(abcli_option_int "$options" upload 0)

    local ingest_object_name=$(abcli_string_timestamp)

    abcli_eval dryrun=$do_dryrun \
        vanwatch ingest \
        area=vancouver,count=3,~process,upload=$do_upload \
        $ingest_object_name

    abcli_eval dryrun=$do_dryrun \
        vanwatch process \
        upload=$do_upload \
        $ingest_object_name
}
