#! /usr/bin/env bash

function test_vancouver_watching_list() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    abcli_eval dryrun=$do_dryrun \
        vanwatch list area=vancouver,discovery,$2

    abcli_eval dryrun=$do_dryrun \
        vanwatch list area=vancouver,ingest,$3

    abcli_eval dryrun=$do_dryrun \
        vanwatch list areas \
        "${@:4}"
}
