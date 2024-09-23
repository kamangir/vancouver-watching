#! /usr/bin/env bash

function vancouver_watching_ingest() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="area=<vancouver>,~batch,count=<-1>$EOP,dryrun,gif,model=<model-id>,~process$EOPE,publish$EOP,~upload$EOPE"
        abcli_show_usage "vanwatch ingest$ABCUL$options$EOP$ABCUL-|<object-name>$EARGS" \
            "ingest <area> -> <object-name>."

        if [ "$(abcli_keyword_is $2 verbose)" == true ]; then
            python3 -m vancouver_watching.ingest --help
        fi
        return
    fi

    local on_batch=$(abcli_option_int "$options" batch 1)

    local object_name=$(abcli_clarify_object $2 $(abcli_string_timestamp))

    if [[ "$on_batch" == 1 ]]; then
        abcli_aws_batch eval name=$object_name \
            vancouver_watching_ingest \
            ",$options,~batch" \
            $object_name \
            "${@:3}"
        return
    fi

    local area=$(abcli_option "$options" area vancouver)
    local count=$(abcli_option_int "$options" count -1)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_process=$(abcli_option_int "$options" process 1)
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local object_path=$ABCLI_OBJECT_ROOT/$object_name

    local discovery_object=$(
        abcli_tags search \
            area=$area,discovery,vancouver_watching \
            --count 1 \
            --log 0
    )
    if [ -z "$discovery_object" ]; then
        abcli_log_error "-vancouver_watching: ingest: $area: area not found."
        return 1
    fi

    abcli_download - $discovery_object

    cp -v \
        $ABCLI_OBJECT_ROOT/$discovery_object/$area.geojson \
        $object_path/

    python3 -m vancouver_watching.ingest \
        --count $count \
        --do_dryrun $do_dryrun \
        --geojson $object_path/$area.geojson \
        "${@:3}"

    abcli_tags set \
        $object_name \
        area=$area,ingest,vancouver_watching

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $object_name

    [[ "$do_process" == 1 ]] &&
        vancouver_watching_process \
            "$options" \
            "$object_name" \
            "${@:3}"

    return 0
}
