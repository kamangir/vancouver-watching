#! /usr/bin/env bash

function test_vancouver_watching_README() {
    local options=$1

    abcli_eval ,$options \
        vancouver_watching build_README
}
