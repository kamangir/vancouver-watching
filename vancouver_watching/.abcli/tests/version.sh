#! /usr/bin/env bash

function test_vancouver_watching_version() {
    local options=$1

    abcli_eval ,$options \
        "vancouver_watching version ${@:2}"

    return 0
}
