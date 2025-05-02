#! /usr/bin/env bash

function test_vancouver_watching_list_targets() {
    local options=$1

    local list_of_targets=$(vancouver_watching_list_targets)

    bluer_ai_assert \
        "$list_of_targets" \
        - \
        non-empty
}
