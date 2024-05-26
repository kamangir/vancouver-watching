#! /usr/bin/env bash

function vancouver_watching_vision() {
    vancouver_watching_openai_commands_vision "$@"
}

function vancouver_watching_openai_commands_vision() {
    local prompt=$1

    if [ "$prompt" == "help" ]; then
        local options="area=<area>,offset=<1>,$openai_commands_vision_options"
        local args="[--verbose 1]"
        abcli_show_usage "vanwatch vision \"prompt\"$ABCUL[$options]${ABCUL}Davie,Bute$ABCUL$args" \
            "openai_commands vision: prompt @ <area>/intersection."
        return
    fi

    local options=$2
    local area=$(abcli_option "$options" area vancouver)
    local offset=$(abcli_option_int "$options" offset 0)

    local intersection=$3

    openai_commands_vision \
        "$prompt" \
        "$options" \
        $intersection,.jpg \
        $(vancouver_watching_list area=$area,ingest,published \
            --log 0 \
            --count 1 \
            --offset $offset) \
        --max_count 10 \
        "${@:4}"
}
