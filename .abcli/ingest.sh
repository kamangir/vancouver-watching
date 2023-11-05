#! /usr/bin/env bash

# https://hub.ultralytics.com/models/R6nMlK6kQjSsQ76MPqQM?tab=preview
export vancouver_watching_default_model="R6nMlK6kQjSsQ76MPqQM"

function vancouver_watching_ingest() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="area=$(vancouver_watching_list_of_areas \|),count=<-1>,detect,dryrun,model=<$vancouver_watching_default_model>,~upload"
        local args="<args>"
        abcli_show_usage "vancouver_watching ingest$ABCUL[$options]$ABCUL[-|<object-name>]$ABCUL$args" \
            "ingest <area> -> <object-name>."

        if [ "$(abcli_keyword_is $2 verbose)" == true ]; then
            python3 -m vancouver_watching.ingest --help
        fi
        return
    fi

    local area=$(abcli_option "$options" area vancouver)
    local count=$(abcli_option_int "$options" count -1)
    local do_detect=$(abcli_option_int "$options" detect 0)
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))
    local model_id=$(abcli_option "$options" model $vancouver_watching_default_model)

    local object_name=$(abcli_clarify_object $2 $(abcli_string_timestamp))
    local object_path=$abcli_object_root/$object_name

    local discovery_object=$(
        abcli_tag search \
            $area,vancouver_watching,discovery \
            --count 1 \
            --log 0
    )
    if [ -z "$discovery_object" ]; then
        abcli_log_error "-vancouver_watching: ingest: $area: area not found."
        return 1
    fi

    abcli_download object $discovery_object

    cp -v \
        $abcli_object_root/$discovery_object/$area.geojson \
        $object_path/

    python3 -m vancouver_watching.ingest \
        from_cameras \
        --count $count \
        --do_dryrun $do_dryrun \
        --filename $object_path/$area.geojson \
        "${@:3}"

    [[ "$do_detect" == 1 ]] &&
        python3 -m vancouver_watching.ai \
            infer \
            --do_dryrun $do_dryrun \
            --model_id $model_id \
            --filename $object_path/$area.json \
            "${@:3}"

    abcli_tag set \
        $object_name \
        $area,vancouver_watching,ingest

    [[ "$do_upload" == 1 ]] &&
        abcli_upload object $object_name
}
