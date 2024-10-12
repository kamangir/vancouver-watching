#! /usr/bin/env bash

function vancouver_watching() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        vancouver_watching_discover "$@"
        vancouver_watching_ingest "$@"
        vancouver_watching_list "$@"
        vancouver_watching_openai_commands_vision "$@"
        vancouver_watching_process "$@"
        vancouver_watching_update_cache "$@"
        return
    fi

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
