#! /usr/bin/env bash

function vancouver_watching() {
    local task=$1

    bluer_ai_generic_task \
        plugin=vancouver_watching,task=$task \
        "${@:2}"
}

bluer_ai_source_caller_suffix_path /tests

bluer_ai_env_dot_load \
    caller,plugin=vancouver_watching,suffix=/../..

bluer_ai_env_dot_load \
    caller,filename=config.env,suffix=/..

bluer_ai_log $(vancouver_watching version --show_icon 1)
