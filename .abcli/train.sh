#! /usr/bin/env bash

function vancouver_watching_train() {
    local task=$(abcli_unpack_keyword $1)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vancouver_watching train$ABCUL[dryrun,epochs=10,gpu_count=2,size=$YOLOV5_MODEL_SIZES,~upload]" \
            "train a model."
        return
    fi

    local options=$1

    local options=$(abcli_option_default "$options" classes person+bicycle+car+motorcycle+bus+train+truck+bird)
    yolov5_train \
        coco128 \
        "$options" \
        ${@:2}

    abcli_tag set \
        $abcli_object_name \
        vancouver_watching
}