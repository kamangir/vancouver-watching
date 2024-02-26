#! /usr/bin/env bash

function vancouver_watching_conda() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_show_usage "vanwatch conda create_env [validate,~recreate]" \
            "create conda environment."
        abcli_show_usage "vanwatch conda validate" \
            "validate conda environment."
        return
    fi

    if [ "$task" == "create_env" ]; then
        local options=$2
        local do_recreate=$(abcli_option_int "$options" recreate 1)
        local do_validate=$(abcli_option_int "$options" validate 0)

        local environment_name=Vancouver-Watching

        if [[ "$do_recreate" == 0 ]] && [[ $(abcli_conda exists $environment_name) == 1 ]]; then
            abcli_eval - conda activate $environment_name
            return
        fi

        abcli_conda create_env name=$environment_name

        pip3 install -r requirements.txt

        if [ "$abcli_is_mac" == true ]; then
            pip3 install folium
            pip3 install boto3
        fi

        [[ "$do_validate" == 1 ]] && vancouver_watching_conda validate

        return
    fi

    if [ "$task" == validate ]; then
        return
    fi

    abcli_log_error "-vancouver_watching: conda: $task: command not found."
}
