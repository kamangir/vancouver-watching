#! /usr/bin/env bash

function test_vancouver_watching_discover() {
    local options=$1

    local object_name=test_vancouver_watching_discover-$(abcli_string_timestamp_short)

    abcli_eval ,$options \
        vancouver_watching \
        discover \
        target=vancouver,count=3,~tag,~upload \
        $object_name
}
