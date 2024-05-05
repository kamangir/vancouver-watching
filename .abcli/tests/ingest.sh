#! /usr/bin/env bash

function test_vancouver_watching_ingest() {
    local options=$1

    abcli_eval ,$options \
        vanwatch ingest \
        area=vancouver,count=3,~batch,$2 \
        "${@:3}"
}
