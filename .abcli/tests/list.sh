#! /usr/bin/env bash

function test_vancouver_watching_list() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_upload=$(abcli_option_int "$options" upload 0)

    abcli_eval dryrun=$do_dryrun \
        vanwatch list area=vancouver,discovery

    abcli_eval dryrun=$do_dryrun \
        vanwatch list area=vancouver,ingest

    abcli_eval dryrun=$do_dryrun \
        vanwatch list areas
}
