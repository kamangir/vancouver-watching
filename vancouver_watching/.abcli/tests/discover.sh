#! /usr/bin/env bash

function test_vancouver_watching_discover() {
    local options=$1

    local object_name=test_vancouver_watching_discover-$(bluer_ai_string_timestamp_short)

    bluer_ai_eval ,$options \
        vancouver_watching \
        discover \
        target=vancouver,count=3,~tag,~upload \
        $object_name
}
