#! /usr/bin/env bash

function vancouver_watching_train() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        abcli_show_usage "vancouver_watching train$ABCUL[-]" \
            "train a model."
        return
    fi

    local options=$1

    local options=$(abcli_option_default "$options" classes person+bicycle+car+motorcycle+bus+train+truck+bird)
    yolov5_train \
        coco128 \
        "$options" \
        ${@:2}
}