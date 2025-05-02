#! /usr/bin/env bash

function vancouver_watching_list_targets() {
    python3 -m vancouver_watching.discover \
        list_targets \
        "$@"
}
