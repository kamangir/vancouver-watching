#! /usr/bin/env bash

function test_vancouver_watching_discover() {
    local options=$1

    local list_of_targets=$(vancouver_watching_list_targets)
    list_of_targets=$(bluer_ai_option "$options" target $list_of_targets)

    local target
    for target in $(echo "$list_of_targets" | tr + " "); do
        bluer_ai_log "🎯 target: $target..."

        local object_name=test_vancouver_watching_discover-$target-$(bluer_ai_string_timestamp_short)

        bluer_ai_eval ,$options \
            vancouver_watching \
            discover \
            target=$target,count=3,~upload \
            $object_name
        [[ $? -ne 0 ]] && return 1

        bluer_ai_eval ,$options \
            python3 -m vancouver_watching.discover \
            test \
            --object_name $object_name
        [[ $? -ne 0 ]] && return 1

        bluer_ai_hr
    done
    return 0
}
