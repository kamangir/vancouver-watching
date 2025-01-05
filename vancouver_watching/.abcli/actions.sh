#! /usr/bin/env bash

function vancouver_watching_action_git_before_push() {
    vancouver_watching build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    vancouver_watching pypi build
}
