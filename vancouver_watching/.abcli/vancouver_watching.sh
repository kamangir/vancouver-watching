#! /usr/bin/env bash

function vancouver_watching() {
    local task=$(abcli_unpack_keyword $1 version)

    abcli_generic_task \
        plugin=vancouver_watching,task=$task \
        "${@:2}"
}

abcli_source_caller_suffix_path /tests

abcli_env_dot_load \
    caller,ssm,plugin=vancouver_watching,suffix=/../..

abcli_env_dot_load \
    caller,filename=config.env,suffix=/..

abcli_log $(vancouver_watching version --show_icon 1)
