#! /usr/bin/env bash

function watching_vancouver_ingest() {
    local task=$(abcli_unpack_keyword $1)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vanwatch ingest$ABCUL[web-cam-url-links]" \
            "ingest https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/information/."

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m watching_vancouver.ingest --help
        fi
        return
    fi

    local data_source=$(abcli_unpack_keyword $1 web-cam-url-links)

    if [ "$data_source" == "web-cam-url-links" ] ; then
        curl https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/download/?format=json > web_cam_url_links.json

        return
    fi

    abcli_log_error "-watching_vancouver: ingest: $data_source: source not found."
}