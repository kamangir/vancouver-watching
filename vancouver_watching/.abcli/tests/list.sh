#! /usr/bin/env bash

function test_vancouver_watching_list() {
    local options=$1

    abcli_eval ,$options \
        vanwatch list area=vancouver,discovery,$2

    abcli_hr
    abcli_eval ,$options \
        vanwatch list area=vancouver,ingest,$3

    abcli_hr
    abcli_eval ,$options \
        vanwatch list areas \
        "${@:4}"
}
