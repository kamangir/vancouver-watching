#! /usr/bin/env bash

function vancouver_watching_ingest() {
    local task=$(abcli_unpack_keyword $1)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vanwatch ingest$ABCUL[web-cam-url-links]" \
            "ingest https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/information/."

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m vancouver_watching.ingest --help
        fi
        return
    fi

    local data_source=$(abcli_unpack_keyword $1 web-cam-url-links)

    if [ "$data_source" == "web-cam-url-links" ] ; then
        local format
        for format in json geojson ; do
            curl https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/download/?format=$format > web_cam_url_links.$format
        done

        python3 -m vancouver_watching.ingest \
            geojson \
            --filename $abcli_object_path/web_cam_url_links.geojson

        return
    fi

    abcli_log_error "-vancouver_watching: ingest: $data_source: source not found."
}