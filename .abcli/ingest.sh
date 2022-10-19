#! /usr/bin/env bash

function vancouver_watching_ingest() {
    local task=$(abcli_unpack_keyword $1)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vanwatch ingest$ABCUL[web_cam_url_links]$ABCUL[~clone_geojson,+download_geojson,~upload]" \
            "ingest https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/information/."

        if [ "$(abcli_keyword_is $2 verbose)" == true ] ; then
            python3 -m vancouver_watching.ingest --help
        fi
        return
    fi

    local data_source=$(abcli_clarify_input $1 web_cam_url_links)

    local options=$2
    local do_upload=$(abcli_option_int "$options" upload 1)
    
    if [ "$data_source" == "web_cam_url_links" ] ; then
        local do_download_geojson=$(abcli_option_int "$options" download_geojson 0)
        local do_clone_geojson=$(abcli_option_int "$options" clone_geojson 1)

        if [ "$do_download_geojson" == 1 ] ; then
            curl https://opendata.vancouver.ca/explore/dataset/web-cam-url-links/download/?format=geojson > web_cam_url_links.geojson
        elif [ "$do_clone_geojson" == 1 ] ; then
            local previous_object=$(abcli_tag \
                search \
                web_cam_url_links,vanwatch,ingest \
                --count 1 \
                --log 0)
            abcli_log "vancouver_watching: ingest: from $previous_object"

            abcli_download object \
                $previous_object \
                web_cam_url_links.geojson

            cp -v \
                ../$previous_object/web_cam_url_links.geojson \
                ./
        fi

        python3 -m vancouver_watching.ingest \
            from_cameras \
            --filename $abcli_object_path/web_cam_url_links.geojson

        abcli_tag set \
            $abcli_object_name \
            web_cam_url_links,vanwatch,ingest

        if [ "$do_upload" == 1 ] ; then
            abcli_upload
        fi

        return
    fi

    abcli_log_error "-vancouver_watching: ingest: $data_source: source not found."
}