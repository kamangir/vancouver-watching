#! /usr/bin/env bash

function test_vancouver_watching_list() {
    local options=$1

    vancouver_watching list \
        area=vancouver,discovery,$2
    [[ $? -ne 0 ]] && return 1

    abcli_hr

    vancouver_watching list \
        area=vancouver,ingest,$3
    [[ $? -ne 0 ]] && return 1

    abcli_hr

    vancouver_watching list areas \
        "${@:4}"
}
