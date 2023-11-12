#! /usr/bin/env bash

function vancouver_watching_conda() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ]; then
        abcli_show_usage "vanwatch conda create_env [validate]" \
            "create conda environmnt."
        abcli_show_usage "vanwatch conda validate" \
            "validate conda environmnt."
        return
    fi

    if [ "$task" == "create_env" ]; then
        local options=$2
        local do_validate=$(abcli_option_int "$options" validate 0)

        abcli_conda create_env name=Vancouver-Watching

        pip3 install pymysql==0.10.1
        pip3 install geojson
        pip3 install beautifulsoup4
        pip3 install geopandas
        pip3 install tqdm
        pip3 install requests
        pip3 install opencv-python
        pip3 install pytest

        if [ "$abcli_is_mac" == true ]; then
            pip3 install folium
            pip3 install boto3
        fi

        [[ "$do_validate" == 1 ]] && vancouver_watching_conda validate

        return
    fi

    if [ "$task" == validate ]; then
        echo "wip"
        return
    fi

    abcli_log_error "-vancouver_watching: conda: $task: command not found."
}
